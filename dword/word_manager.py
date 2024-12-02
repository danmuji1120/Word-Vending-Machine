import csv
import os
import pandas as pd
from datetime import datetime
import logging
from typing import List
from dword.path import resource_path

# 로깅 설정
logging.basicConfig(level=logging.INFO)

class WordManager:
    def __init__(self, section_name: str):
        self.section_name = section_name
        self.path = resource_path("data")
        self.path = os.path.join(self.path, self.section_name, "words.csv")
        # self.path = "data/" + self.section_name + "/words.csv"
        self.init()

    def init(self):
        dir_path = os.path.dirname(self.path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
            logging.info(f"{dir_path} 경로가 생성되었습니다.")
        
        if not os.path.exists(self.path):
            data = {"date": [],
                    "question": [],
                    "answer": [],
                    "info": []}
            # for i in self.format:
                # data[i] = []
            df = pd.DataFrame(data)
            df.to_csv(self.path, index=None)
            logging.info(f"{self.path} 파일이 생성되었습니다.")

    def add(self, word: List[str]):
        current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        word.insert(0, current_time)
        logging.debug(f"Adding word: {word}")
        
        data = self.load_file()
        if self.is_word(word[1]):
            logging.warning(f"'{word[1]}'은(는) 이미 존재합니다. 추가하지 않습니다.")
        else:
            data.loc[len(data)] = word
            data.to_csv(self.path, index=None)
            logging.info(f"'{word[1]}'이(가) 추가되었습니다.")
    def add(self, question: str, answers: str, info: str):
        current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        word = [current_time, question, answers, info]
        logging.debug(f"Adding word: {word}")
        
        data = self.load_file()
        if self.is_word(word[1]):
            logging.warning(f"'{word[1]}'은(는) 이미 존재합니다. 추가하지 않습니다.")
        else:
            data.loc[len(data)] = word
            data.to_csv(self.path, index=None)
            logging.info(f"'{word[1]}'이(가) 추가되었습니다.")
    def add_answer(self, question: str, answer: str):
        data = self.load_file()
        index = self.get_index(question)
        if index is not None:
            data.loc[index, "answer"] += f",{answer}"
            data.to_csv(self.path, index=None)
            logging.info(f"'{answer}' 답변이 '{question}'에 추가되었습니다.") 
    def delete(self, word: str):
        index = self.get_index(word)
        if index is not None:
            data = self.load_file()
            data = data.drop(index)
            data.to_csv(self.path, index=None)
            logging.info(f"'{word}' 단어가 삭제되었습니다.")
        else:
            logging.warning(f"'{word}' 단어가 파일에 없습니다.")

    def edit(self, word: str, new_data: List[str]):
        index = self.get_index(word)
        if index is not None:
            data = self.load_file()
            original_data = data.iloc[index]
            new_data.insert(0, original_data[0])  # 시간 유지
            data.iloc[index] = new_data
            data.to_csv(self.path, index=None)
            logging.info(f"'{word}' 단어의 데이터가 수정되었습니다.")
        else:
            logging.warning(f"'{word}' 단어가 파일에 없습니다.")

    def get_index(self, word: str):
        data = self.load_file()
        if len(data) == 0:
            return None
        else:
          if word in data.iloc[:, 1].values:
              return data[data.iloc[:, 1] == word].index[0]
          else:
              return None

    def is_word(self, word: str):
        data = self.load_file()
        if len(data) == 0:
            return False
        else:
          return word in data.iloc[:, 1].values
    
    # 모든 단어를 list로 반환
    def get_word_list(self) -> list:
        data = self.load_file()
        return data["question"].tolist()

    def get_answer_dict(self) -> dict:
        data = self.load_file()
        result = {}
        for i in range(len(data)):
            result[data["question"][i]] = data["answer"][i]
        return result
    #===============================================
    # get_answer_dict로 전환 후 삭제 예정
    def get_list(self):
        data = self.load_file()
        result = {}
        for i in range(len(data)):
            result[data["question"][i]] = data["answer"][i]
        return result
    #===============================================
    def get_date_dict(self) -> dict:
        data = self.load_file()
        result = {}
        for i in range(len(data)):
            result[data["question"][i]] = data["date"][i]
        return result
    def get_info_dict(self) -> dict:
        data = self.load_file()
        result = {}
        for i in range(len(data)):
            result[data["question"][i]] = data["info"][i]
        return result
    #===============================================
    # get_info_dict로 전환 후 삭제 예정
    def get_info(self):
        data = self.load_file()
        result = {}
        for i in range(len(data)):
            result[data["question"][i]] = data["info"][i]
        return result
    #===============================================
    def load_file(self):
        self.init()
        try:
            data = pd.read_csv(self.path)
            return data
        except Exception as e:
            logging.error(f"파일을 로드하는 중 오류 발생: {e}")
            raise
