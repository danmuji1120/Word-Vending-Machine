from enum import Enum

class State(Enum):
  SUCCESS = 1 # 성공
  DUPLICATION = 2 # 중복된 단어로 실패
  NO_EXIST = 3 # 존재하지 않아서 실패
  NO_DATA = 4 # 데이터가 존재하지 않아서 실패
  ALREADY = 5 # 이미 진행중이기 때문에 실패
  NO_PROCESS = 6 # 진행중이 아니기 때문에 실패
  CORRECT = 7 # 정답
  WRONG = 8 # 오답
  END = 9 # 게임 종료
  EMPTY = 10 # 비어있어서 실패
  # Already in progress