import pandas as pd

class Analysis:
    def calculate_word_accuracy(self, df: pd.DataFrame, ascending: bool = None):
        # 날짜 열을 제외한 모든 단어 열에 대해 정답률 계산
        accuracies = {}
        
        for column in df.columns[1:]:  # 첫 번째 열(날짜)을 제외
            valid_answers = df[column][df[column] != -1]
            correct = (valid_answers == 1).sum()
            total_attempts = len(valid_answers)
            
            accuracy = (correct / total_attempts * 100) if total_attempts > 0 else 0
            accuracies[column] = accuracy
        
        result_df = pd.DataFrame({
            'word': accuracies.keys(),
            'accuracy': accuracies.values()
        })
        
        if ascending is True:
            return result_df.sort_values('accuracy', ascending=True)
        elif ascending is False:
            return result_df.sort_values('accuracy', ascending=False)
        return result_df

    def calculate_memorized_date(self, df: pd.DataFrame) -> pd.DataFrame:
        memorized_dates = {}
        
        for word in df.columns[1:]:
            correct_count = 0
            consecutive_wrong = 0
            memorized = False
            
            for date, result in zip(df['date'], df[word]):
                if result == 1:
                    correct_count += 1
                    consecutive_wrong = 0
                elif result == 0:
                    consecutive_wrong += 1
                    if consecutive_wrong >= 2:
                        correct_count = 0
                        consecutive_wrong = 0
                
                if correct_count >= 5 and not memorized:
                    memorized_dates[word] = pd.to_datetime(date, format='%Y-%m-%d-%H-%M-%S')
                    memorized = True
        return pd.DataFrame({
            'word': memorized_dates.keys(),
            'memorized_date': memorized_dates.values()
        })

    def get_memorized_count_by_day(self, df: pd.DataFrame):
        memorized_df = self.calculate_memorized_date(df)
        if memorized_df.empty:
            return pd.Series()
            
        # 날짜만 추출하여 Series 생성
        dates = memorized_df['memorized_date'].dt.date
        # value_counts()를 사용하여 각 날짜별 카운트 계산
        daily_counts = dates.value_counts().sort_index()
        
        # 전체 날짜 범위 생성
        date_range = pd.date_range(
            start=daily_counts.index.min(),
            end=pd.Timestamp.today().date(),
            freq='D'
        )
        
        # 전체 날짜 범위에 대해 Series 생성 (없는 날짜는 0으로 채움)
        result = pd.Series(0, index=date_range).add(daily_counts, fill_value=0)
        return result.astype(int)  # int형으로 변환

    def get_memorized_count_by_month(self, df: pd.DataFrame):
        daily_counts = self.get_memorized_count_by_day(df)
        if daily_counts.empty:
            return pd.Series()
            
        return daily_counts.resample('ME').last()

    def get_memorized_count_by_year(self, df: pd.DataFrame):
        daily_counts = self.get_memorized_count_by_day(df)
        if daily_counts.empty:
            return pd.Series()
            
        return daily_counts.resample('YE').last()

    def get_cumulative_memorized_count(self, df: pd.DataFrame):
        daily_counts = self.get_memorized_count_by_day(df)
        if daily_counts.empty:
            return pd.Series()
        
        # cumsum()을 사용하여 누적 합계 계산
        cumulative_counts = daily_counts.cumsum()
        return cumulative_counts

    def get_unmemorized_words(self, df: pd.DataFrame) -> list:
        # 외운 단어 목록 가져오기
        memorized_df = self.calculate_memorized_date(df)
        memorized_words = set(memorized_df['word'])
        
        # 전체 단어 목록 (날짜 열 제외)
        all_words = set(df.columns[1:])
        
        # 외우지 못한 단어 찾기
        unmemorized_words = all_words - memorized_words
        
        # 리스트로 변환하여 반환
        return list(unmemorized_words)

    def get_memorized_words(self, df: pd.DataFrame) -> list:
        # 외운 단어 목록 가져오기
        memorized_df = self.calculate_memorized_date(df)
        
        # 단어 리스트로 변환하여 반환
        return memorized_df['word'].tolist()

if __name__ == "__main__":
    # CSV 파일 로드
    df = pd.read_csv('data/commons/records.csv')
    # Analysis 클래스 사용
    analysis = Analysis()
    result_df = analysis.calculate_word_accuracy(df)
    print(result_df)