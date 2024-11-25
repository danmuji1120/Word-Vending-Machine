from typing import List
from .word_manager import WordManager
from .recordManager import Record
from .state import State
from queue import Queue
import random
import logging
from .analysis import Analysis

DAYS = 10
COUNT = 5
MAX_COUNT = 20
MAX_RATE = 80

class Game:
  def __init__(self, section_name: str = "commons", question_tag: str = "단어", answer_tag: str = "뜻") -> None:
    self.processing = False
    self.section_name = section_name
    self.queue = Queue()
    self.question_answer_dict = {}
    self.scores = {}
    self.current_question = ""
    self.question_tag = question_tag
    self.answer_tag = answer_tag
    self.word_manager = WordManager(self.section_name)
    self.record = Record(self.section_name)
    self.analysis = Analysis(self.word_manager, self.record)
    self.format = (question_tag, answer_tag)
    self.question_list = []
    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.INFO)
    
    # 기존 핸들러가 있는지 확인하고 제거
    if self.logger.handlers:
        self.logger.handlers.clear()
        
    # 새 핸들러 추가
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    self.logger.addHandler(handler)

  # === 게임 상태 관리 ===
  def is_start(self):
    """게임이 진행 중인지 확인"""
    return self.processing

  def get_remain_question(self):
    """남은 문제 수 반환"""
    return self.queue.qsize()

  def set_question(self) -> State:
    """정답률이 낮은 단어들로 문제 목록 생성"""
    unmemorized_words = self.analysis.get_not_memorized_words()
    review_words = self.analysis.get_words_for_review()
    self.logger.info(f"unmemorized_words: {unmemorized_words}")
    self.logger.info(f"review_words: {review_words}")

    selected_unmemorized_count = 0
    selected_review_count = 0
    for i in range(max(len(unmemorized_words), len(review_words))):
        if i < len(unmemorized_words):
            selected_unmemorized_count += 1
            self.question_list.append(unmemorized_words[i])
        if len(self.question_list) >= MAX_COUNT:
          break
        if i < len(review_words):
            selected_review_count += 1
            self.question_list.append(review_words[i])
        if len(self.question_list) >= MAX_COUNT:
            break
        
    all_words = self.word_manager.get_word_list()
    random.shuffle(all_words)
    selected_memorized_count = 0
    for word in all_words:
        if len(self.question_list) >= MAX_COUNT:
            break
        if word not in self.question_list:
           self.question_list.append(word)
           selected_memorized_count += 1
    memorized_count = self.analysis.get_number_of_memorized_words()
    unmemorized_count = self.analysis.get_number_of_not_memorized_words()
    review_count = self.analysis.get_number_of_review_words()
    
    self.logger.info(f"암기된 단어 중 선택된 단어 수: {selected_memorized_count}/{memorized_count}")
    self.logger.info(f"암기되지 않은 단어 중 선택된 단어 수: {selected_unmemorized_count}/{unmemorized_count}")
    self.logger.info(f"복습이 필요한 단어 중 선택된 단어 수: {selected_review_count}/{review_count}")
    
    if not self.question_list:
        return State.NO_DATA
    
    self.logger.info(f"문제 목록: {self.question_list}")
    
    # 문제 목록을 랜덤하게 섞기
    random.shuffle(self.question_list)
    self.logger.info(f"섞은 문제 목록: {self.question_list}")
        
    for word in self.question_list:
        self.queue.put(word)
    return State.SUCCESS

  def get_question(self):
    """현재 문제 반환"""
    if self.processing:
      return self.current_question
    else:
      return State.NO_PROCESS

  def get_answer(self):
    """현재 문제의 정답 반환"""
    if self.processing:
      return self.question_answer_dict[self.current_question]
    else:
      return State.NO_PROCESS

  def answer(self, user_answer: str) -> State:
    """사용자 답변 검증"""
    if not self.processing:
        self.logger.warning("게임이 시작되지 않았습니다.")
        return State.NO_PROCESS

    correct_answers = [answer.strip() for answer in self.question_answer_dict[self.current_question].split(',')]
    user_answer = user_answer.replace(" ", "")
    
    # 여러 정답 중 하나라도 일치하면 정답 처리
    is_correct = any(answer.replace(" ", "") == user_answer for answer in correct_answers)
    self.scores[self.current_question] = 1 if is_correct else 0
    
    if is_correct:
        self.logger.info(f"정답입니다! 문제: {self.current_question}")
    else:
        self.logger.info(f"오답입니다. 문제: {self.current_question}, 정답: {self.question_answer_dict[self.current_question]}")
    
    return State.CORRECT if is_correct else State.WRONG

  # === 게임 진행 제어 ===
  def start(self) -> State:
    """게임 시작"""
    if self.processing:
      self.logger.warning("게임이 이미 진행 중입니다.")
      return State.ALREADY
    
    self.question_answer_dict = self.word_manager.get_list()
    if not self.question_answer_dict:
      self.logger.error("사용 가능한 단어가 없습니다.")
      return State.NO_DATA

    result = self.set_question()
    if result != State.SUCCESS:
      return result

    self.processing = True
    self.scores = {}
    self.current_question = self.queue.get()
    self.logger.info(f"게임이 시작되었습니다. 총 {len(self.question_list)}개의 문제가 준비되었습니다.")
    return State.SUCCESS

  def next(self):
    """다음 문제로 이동"""
    if not self.processing:
      return State.NO_PROCESS
    else:
      if self.queue.empty():
        self.processing = False
        return State.END
      else:
        self.current_question = self.queue.get()
        return State.SUCCESS

  # === 점수 및 기록 관리 ===
  def get_rate_base(self, rate_func) -> dict:
    """정답률 계산 기본 로직"""
    self.question_answer_dict = self.word_manager.get_list()
    keys = self.question_answer_dict.keys()
    result = {key: 0 for key in keys}
    added_data = rate_func()
    result.update({k: v for k, v in added_data.items() if k in keys})
    return result

  def get_rate_all(self) -> dict:
    """전체 정답률 조회"""
    return self.get_rate_base(self.record.get_rate_all)

  def get_rate(self, days: int = DAYS, count: int = COUNT) -> dict:
    """기간별 정답률 조회"""
    return self.get_rate_base(lambda: self.record.get_rate(days=days, count=count))

  def set_score(self, word:str, value:int):
    """특정 단어의 점수 설정"""
    if word in self.scores.keys():
      self.scores[word] = value
      return State.SUCCESS
    else:
      return State.NO_EXIST

  def save_scores(self):
    """현재 게임의 점수 저장"""
    self.record.add(self.scores)

  # === 단어 관리 ===
  def get_available_word_count(self) -> int:
    """추가 가능한 단어 수 확인"""
    unmemorized_count = self.analysis.get_number_of_not_memorized_words()
    review_count = self.analysis.get_number_of_review_words()
    return max(0, MAX_COUNT - unmemorized_count - review_count)
  
  def get_unmemorized_word_count(self) -> int:
    """암기되지 않은 단어 수 확인"""
    correct_rate_data = self.get_rate()
    low_score_count = sum(1 for rate in correct_rate_data.values() if rate < MAX_RATE)
    return low_score_count

  def add(self, question: str, answers: str, info: str):
    """새 단어 추가"""
    if self.processing:
        self.logger.warning("게임 진행 중에는 단어를 추가할 수 없습니다.")
        return State.ALREADY
    else:
        if self.get_available_word_count() <= 0:
            return State.FULL
            
        if not self.word_manager.is_word(question):
            self.word_manager.add(question, answers, info)
            self.logger.info(f"새로운 단어가 추가되었습니다: {question}")
            return State.SUCCESS
        else:
            return State.DUPLICATION
  def add_answer(self, question: str, answer: str):
    """단어 답변 추가"""
    self.word_manager.add_answer(question, answer)
    return State.SUCCESS
  def delete(self, word:str):
    """단어 삭제"""
    if self.processing:
      return State.ALREADY
    else:
      if self.word_manager.is_word(word):
        self.word_manager.delete(word)
        return State.SUCCESS
      else:
        return State.NO_EXIST
      
  def get_list(self):
    """단어 목록 조회"""
    if self.processing:
      self.logger.warning("게임 진행 중에는 단어를 조회할 수 없습니다.")
      return State.ALREADY
    else:
      return self.word_manager.get_list()

  # === 기타 유틸리티 ===
  def get_info(self):
    """섹션 정보 조회"""
    if self.processing:
      self.logger.warning("게임 진행 중에는 섹션 정보를 조회할 수 없습니다.")
      return State.ALREADY
    else:
      return self.word_manager.get_info()

  def get_question_tag(self):
    """문제 태그 반환"""
    return self.format[0]

  def get_answer_tag(self):
    """답변 태그 반환"""
    return self.format[1]