import pandas as pd

class Analysis:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def calculate_word_accuracy(self, ascending: bool = None):
        # 날짜 열을 제외한 모든 단어 열에 대해 정답률 계산
        accuracies = {}
        
        for column in self.df.columns[1:]:  # 첫 번째 열(날짜)을 제외
            valid_answers = self.df[column][self.df[column] != -1]
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

    def calculate_memorized_date(self) -> pd.DataFrame:
        memorized_dates = {}
        
        for word in self.df.columns[1:]:
            correct_count = 0
            consecutive_wrong = 0
            memorized = False
            
            for date, result in zip(self.df['date'], self.df[word]):
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

    def show_memorized_count_by_day(self):
        memorized_df = self.calculate_memorized_date()
        if memorized_df.empty:
            return pd.Series()
            
        date_range = pd.date_range(
            start=memorized_df['memorized_date'].min().date(),
            end=pd.Timestamp.today().date(),
            freq='D'
        )
        
        daily_counts = pd.Series(0, index=date_range)
        for date in memorized_df['memorized_date']:
            daily_counts[date.date():] += 1
            
        return daily_counts

    def show_memorized_count_by_month(self):
        daily_counts = self.show_memorized_count_by_day()
        if daily_counts.empty:
            return pd.Series()
            
        return daily_counts.resample('ME').last()

    def show_memorized_count_by_year(self):
        daily_counts = self.show_memorized_count_by_day()
        if daily_counts.empty:
            return pd.Series()
            
        return daily_counts.resample('YE').last()

if __name__ == "__main__":
    # CSV 파일 로드
    df = pd.read_csv('data/commons/records.csv')
    # Analysis 클래스 사용
    analysis = Analysis(df)
    result_df = analysis.calculate_word_accuracy()
    print(result_df)