import pandas as pd
import os
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

class Record:
  def __init__(self, section_name) -> None:
    self.section_name = section_name
    self.path = "data/" + self.section_name + "/records.csv"
    self.init()

  def init(self):
      dir_path = os.path.dirname(self.path)
      if dir_path and not os.path.exists(dir_path):
          os.makedirs(dir_path)
          logging.info(f"{dir_path} 경로가 생성되었습니다.")
      
      if not os.path.exists(self.path):
          data = {"date": []}
          df = pd.DataFrame(data)
          df.to_csv(self.path, index=None)
          logging.info(f"{self.path} 파일이 생성되었습니다.")
  # data format {"apple": 1, "banana": 0, "cat": 1}
  # 1: correct, 0: incorrect, -1: no test
  def get_rate(self, days:int=10, count:int=10):
      data = self.load_file()
      data['date'] = pd.to_datetime(data['date'], format="%Y-%m-%d-%H-%M-%S")

      current_date = datetime.now()
      ten_days_ago = current_date - timedelta(days=days)
      recent_data = data[data['date'] >= ten_days_ago]

      result = {}
      for column in recent_data.columns[1:]:
          correct_answers = (recent_data[column] == 1).sum()
          total_attempts = (recent_data[column] != -1).sum()
          if total_attempts < count:
              accuracy = correct_answers / count
          else:
              accuracy = (correct_answers / total_attempts) if total_attempts > 0 else 0
          result[column] = accuracy * 100
      return result

  def add(self, new_data):
    time = datetime.now()
    time = time.strftime("%Y-%m-%d-%H-%M-%S")
    original_data = self.load_file()
    data = [time] + [-1] * (len(original_data.columns) - 1)

    for key in new_data:
        if key in original_data.columns:
            # print(f"{key} 존재함")
            data[original_data.columns.get_loc(key)] = new_data[key]
        else:
            original_data[key] = -1
            data.append(new_data[key])
    original_data.loc[len(original_data)] = data
    original_data.to_csv(self.path, index=None)
    print(f"{self.path}에 데이터가 저장되었습니다.")

  
  def load_file(self):
        self.init()
        try:
            data = pd.read_csv(self.path)
            return data
        except Exception as e:
            logging.error(f"파일을 로드하는 중 오류 발생: {e}")
            raise
    