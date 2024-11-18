import pandas as pd
from dword.word_manager import WordManager
from dword.recordManager import Record

from datetime import datetime, timedelta

class Analysis:
    """
    단어 학습 분석을 위한 클래스
    
    주요 함수들:
    - get_word_memory_history() -> dict: 각 날짜별 단어들의 암기/망각 상태 기록을 반환
    - get_memorized_words() -> list[str]: 현재 암기된 단어들의 리스트 반환
    - get_number_of_memorized_words() -> int: 암기된 단어의 총 개수 반환
    - get_not_memorized_words() -> list[str]: 아직 암기되지 않은 단어들의 리스트 반환
    - get_number_of_not_memorized_words() -> int: 암기되지 않은 단어의 총 개수 반환
    - get_average_accuracy(days=None) -> pd.DataFrame: 지정된 기간 동안의 단어별 평균 정답률 반환
    - get_last_memorized_date() -> dict: 각 암기된 단어의 마지막 학습 날짜 반환
    - get_words_for_review() -> list[str]: 복습이 필요한 단어 리스트 반환 (2^n일 주기로 복습)
    - get_number_of_review_words() -> int: 복습이 필요한 단어의 총 개수 반환
    - get_cumulative_daily_memorized_word_count() -> dict: 처음 데이터부터 오늘까지 각 날짜별로 외운 단어의 누적 개수를 반환
    - get_daily_memorized_word_count() -> dict: 각 날짜별로 그날 새롭게 외운 단어의 개수를 반환
    """
    
    def __init__(self, word_manager: WordManager, record_manager: Record):
        self.word_manager = word_manager
        self.record_manager = record_manager

    # 단어들의 외운 날짜 및 상태를 반환
    def get_word_memory_history(self) -> dict:
        df = self.record_manager.load_file()

        # 날짜 범위 생성
        first_date = pd.to_datetime(df['date'].iloc[0], format='%Y-%m-%d-%H-%M-%S')
        today = pd.Timestamp.now()
        date_range = pd.date_range(start=first_date.date(), end=today.date(), freq='D')
        
        # 날짜별 딕셔너리 초기화
        memorized_dates = {date.strftime('%Y-%m-%d'): {'memorized': [], 'forgotten': []} for date in date_range}

        for word in df.columns[1:]:
            correct_count = 0
            consecutive_wrong = 0
            memorized = False
            for date, result in zip(df['date'], df[word]):
                date = pd.to_datetime(date, format='%Y-%m-%d-%H-%M-%S')
                if result == 1 and not memorized:
                    correct_count += 1
                    if correct_count >= 5:
                        memorized = True
                        memorized_dates[date.strftime('%Y-%m-%d')]['memorized'].append(word)
                elif result == 0:
                    consecutive_wrong += 1
                    if consecutive_wrong >= 2:
                        correct_count = 0
                        consecutive_wrong = 0
                        if memorized:
                            memorized = False
                            correct_count = 0
                            memorized_dates[date.strftime('%Y-%m-%d')]['forgotten'].append(word)

        return memorized_dates
        
    # 외운 단어들의 리스트를 반환
    def get_memorized_words(self) -> list[str]:
        history = self.get_word_memory_history()
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 모든 날짜에 대해 memorized와 forgotten 상태를 추적
        memorized_set = set()
        for date, status in history.items():
            memorized_set.update(status['memorized'])
            memorized_set.difference_update(status['forgotten'])
        return list(memorized_set)
    
    # 외운 단어의 수를 반환
    def get_number_of_memorized_words(self) -> int:
        """
        외운 단어의 수를 반환
        """
        return len(self.get_memorized_words())
    
    # 외우지 못한 단어들의 리스트를 반환
    def get_not_memorized_words(self) -> list[str]:
        """
        외우지 못한 단어들의 리스트를 반환
        """
        memorized_words = set(self.get_memorized_words())
        all_words = set(self.word_manager.get_word_list())
        return list(all_words - memorized_words)
    
    # 외우지 못한 단어의 수를 반
    def get_number_of_not_memorized_words(self) -> int:
        """
        외우지 못한 단어의 수를 반환
        """
        return len(self.get_not_memorized_words())

    # days가 주어지면 days일 내에서 학습한 단어의 평균 정답률을 반환
    # day가 주어지지 않으면 전체 데이터에서 평균 정답률을 반환
    def get_average_accuracy(self, days: int = None) -> pd.DataFrame:
        words = self.word_manager.get_word_list()
        records = self.record_manager.load_file()
        if days is not None:
            current_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            records['date'] = pd.to_datetime(records['date'], format='%Y-%m-%d-%H-%M-%S')
            cutoff_date = (pd.to_datetime(current_date, format='%Y-%m-%d-%H-%M-%S') - timedelta(days=days))
            records = records[records["date"] >= cutoff_date]
        result = {}
        for word in words:
            word_values = records[word][records[word] != -1]
            if len(word_values) > 0:
                accuracy = int(word_values.mean() * 100)
                result[word] = accuracy
            else:
                result[word] = 0
        return result
    
    # 외운 단어들의 마지막 학습 날짜를 반환
    def get_last_memorized_date(self) -> dict:
        """
        외운 단어들의 마지막 학습 날짜를 반환합니다.
        Returns:
            dict: {단어: 마지막_학습_날짜} 형태의 딕셔너리
        """
        df = self.record_manager.load_file()
        memorized_dates = self.get_word_memory_history()
        dates = list(memorized_dates.keys())
        memorized_words = set(self.get_memorized_words())
        last_memorized_date = {}
        for date in reversed(dates):
            memorized_words.difference_update(memorized_dates[date]['memorized'])
            for word in memorized_dates[date]['memorized']:
                if word not in last_memorized_date:
                    last_memorized_date[word] = date
            if len(memorized_words) == 0:
                break
        return last_memorized_date
    
    # 복습이 필요한 단어 리스트를 반환
    def get_words_for_review(self) -> list[str]:
        """
        복습이 필요한 단어 리스트를 반환합니다.
        복습 주기는 다음과 같이 증가합니다:
        - 1차 복습: 1일 후
        - 2차 복습: 2일 후
        - 3��� 복습: 4일 후
        - 4차 복습: 8일 후
        이런 식으로 2의 제곱으로 증가합니다.
        """
        df = self.record_manager.load_file()
        words_last_memorized_date = self.get_last_memorized_date()
  
        review_words = []
        for word, last_memorized_date in words_last_memorized_date.items():
            # 복습 횟수
            
            # 해당 단어의 테스트 기록 가져오기
            word_records = df[df[word] != -1][['date', word]]
            word_records = word_records[word_records['date'] > last_memorized_date]
            if len(word_records) == 0:
                continue

            date_records = {}
            # for date in word_records['date']:
            for date, result in zip(word_records['date'], word_records[word]):
                # date 형식: "%Y-%m-%d-%H-%M-%S"의 문자열을 "%Y-%m-%d"의 문자열로 변환
                new_date = date[:10]
                date_records[new_date] = result
            last_memorized_date = datetime.strptime(last_memorized_date, '%Y-%m-%d')
            last_review_date = last_memorized_date
            review_count = 0
            for date, result in date_records.items():
                if result == 1:
                    review_count += 1
                    last_review_date = date
            
            today = datetime.now()
            last_review_date = datetime.strptime(last_review_date, '%Y-%m-%d')
            review_date = last_review_date + timedelta(days=2 ** review_count)
            if review_date <= today:
                review_words.append(word)
        return review_words
    def get_number_of_review_words(self) -> int:
        """
        복습이 필요한 단어의 수를 반환합니다.
        """
        return len(self.get_words_for_review())
        
    def get_cumulative_daily_memorized_word_count(self) -> dict:
        """
        처음 데이터부터 오늘까지 각 날짜별로 외운 단어의 누적 개수를 반환합니다.
        Returns:
            dict: {날짜: 누적_외운_단어_수} 형태의 딕셔너리
        """
        df = self.record_manager.load_file()
        memory_history = self.get_word_memory_history()
        
        # 날짜 범위 생성
        first_date = pd.to_datetime(df['date'].iloc[0], format='%Y-%m-%d-%H-%M-%S')
        today = pd.Timestamp.now()
        date_range = pd.date_range(start=first_date.date(), end=today.date(), freq='D')
        
        # 날짜별 누적 외운 단어 수를 저장할 딕셔너리
        daily_count = {}
        memorized_words = set()
        
        for date in date_range:
            date_str = date.strftime('%Y-%m-%d')
            if date_str in memory_history:
                # 해당 날짜에 새로 외운 단어 추가
                memorized_words.update(memory_history[date_str]['memorized'])
                # 해당 날짜에 잊어버린 단어 제거
                memorized_words.difference_update(memory_history[date_str]['forgotten'])
            
            daily_count[date_str] = len(memorized_words)
            
        return daily_count
        
    def get_daily_memorized_word_count(self) -> dict:
        """
        각 날짜별로 그날 새롭게 외운 단어의 개수를 반환합니다.
        Returns:
            dict: {날짜: 그날_외운_단어_수} 형태의 딕셔너리
        """
        memory_history = self.get_word_memory_history()
        
        # 날짜별 새로 외운 단어 수를 저장할 딕셔너리
        daily_count = {}
        
        for date, status in memory_history.items():
            # 해당 날짜에 새로 외운 단어의 개수
            daily_count[date] = len(status['memorized'])
            
        return daily_count
        
        