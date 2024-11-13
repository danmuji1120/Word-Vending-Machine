from .fileHandler import FileHandler
from .recordManager import Record
from .state import State
from queue import Queue
import random

DAYS = 10
COUNT = 5

class Game:
  def __init__(self, section_name="commons") -> None:
    self.processing = False
    self.section_name = section_name
    self.queue = Queue()
    self.data = {}
    self.scores = {}
    self.current_question = ""
    # self.format = ["단어", "뜻"]
    self.question_tag = "단어"
    self.answer_tag = "뜻"
    self.fileHandler = FileHandler(self.section_name)
    self.record = Record(self.section_name)
  def get_rate_all(self) -> dict: # 전체 수행에 대한 정답률
    self.data = self.fileHandler.get_list()
    keys = self.data.keys() # 모든 단어
    result = {} 
    for key in keys:
      result[key] = 0 # 모든 단어의 정답률 0 초기화
      added_data = self.record.get_rate_all() # 이전의 정답률 로드
    for key in added_data.keys():
      if key in keys: 
        result[key] = added_data[key] # 정답률 저장
    return result
  def get_rate(self, days:int=DAYS, count:int=COUNT) -> dict: # 최근 days일간 최대 count회 시행했을 때의 정답률을 반환
    self.data = self.fileHandler.get_list()
    keys = self.data.keys() # 모든 단어
    result = {} 
    for key in keys: 
      result[key] = 0 # 모든 단어의 정답률 0 초기화
      added_data = self.record.get_rate(days=days, count=count) # 이전의 정답률 로드
    for key in added_data.keys():
      if key in keys: 
        result[key] = added_data[key] # 정답률 저장
    return result

  def is_start(self):
    return self.processing
  def start(self):
    self.data = self.fileHandler.get_list()
    self.scores = {}
    self.current_question = ""
    self.queue = Queue()
    if self.processing: # 이미 게임이 실행중이면 실패
      return State.ALREADY
    elif len(self.data) == 0: # 단어 데이터가 없으면 실패
      return State.NO_DATA
    else:
      correct_rate_data = self.get_rate()
      keys = correct_rate_data.keys()
      tmp = []
      for key in keys:
        if correct_rate_data[key] < 80:
          if len(tmp) < 20:
            tmp.append(key)
          else:
            break
      shuffled_list = random.sample(tmp, len(tmp))
      for word in shuffled_list:
        self.queue.put(word)
      self.processing = True
      self.current_question = self.queue.get()
      return State.SUCCESS

  def get_question(self):
    if self.processing:
      return self.current_question
    else:
      return State.NO_PROCESS
  def next(self):
    if not self.processing:
      return State.NO_PROCESS
    else:
      if self.queue.empty():
        self.processing = False
        return State.END
      else:
        self.current_question = self.queue.get()
        return State.SUCCESS

  def get_answer(self):
    if self.processing:
      return self.data[self.current_question]
    else:
      return State.NO_PROCESS
  def get_remain_question(self):
    return self.queue.qsize()
  def set_score(self, word:str, value:int):
    if word in self.scores.keys():
      self.scores[word] = value
      return State.SUCCESS
    else:
      return State.NO_EXIST
  def answer(self, user_answer:str):
    if self.processing:
      correct = self.data[self.current_question]
      correct = correct.replace(" ", "")
      user_answer = user_answer.replace(" ", "")
      if correct == user_answer:
        self.scores[self.current_question] = 1
        return State.CORRECT
      else:
        self.scores[self.current_question] = 0
        return State.WRONG
    else:
      return State.NO_PROCESS
    print(self.scores)
  def add(self, word:list):
    if self.processing:
      return State.ALREADY
    else:
      if not self.fileHandler.is_word(word[0]):
        self.fileHandler.add(word)
        return State.SUCCESS
      else:
        return State.DUPLICATION
  # delete word
  def delete(self, word:str):
    if self.processing:
      return State.ALREADY
    else:
      if self.fileHandler.is_word(word):
        self.fileHandler.delete(word)
        return State.SUCCESS
      else:
        return State.NO_EXIST
      
  # get word list
  def get_list(self):
    if self.processing:
      return State.ALREADY
    else:
      return self.fileHandler.get_list()
  def get_info(self):
    if self.processing:
      return State.ALREADY
    else:
      return self.fileHandler.get_info()
  def save_scores(self):
    self.record.add(self.scores)
  def get_question_tag(self):
    return self.format[0]
  def get_answer_tag(self):
    return self.format[1]