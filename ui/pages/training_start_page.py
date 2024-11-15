from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import components
import events
import dword
from ui.styles.styles import INPUT_STYLE, BUTTON_STYLE, TITLE_STYLE

def set_training_start_page(stack: QStackedLayout):
    # 훈련 시작 페이지를 스택에 추가하는 함수
    train_start_page = TrainingStartPage(stack)
    train_start_page.set_page()

class TrainingStartPage:
    def __init__(self, stack) -> None:
        # 클래스 초기화 및 기본 변수 설정
        self.stack = stack
        self.widget = QWidget()
        self.game = dword.Game()
        self.info_data = self.game.get_info()
        self.count = 0                  # 총 문제 수
        self.correct_count = 0          # 맞은 문제 수
        self.processing = False         # 현재 문제 처리 중인지 여부
        self.last_answer = None         # 마지막 답변 저장

        self.init_ui()
        self.setup_layout()

    def init_ui(self):
        # UI 컴포넌트 초기화 및 설정
        # 타이틀 설정
        self.title_label = components.set_title_label("Enter Start.")
        self.title_label.setStyleSheet(TITLE_STYLE)

        # 진행 상황 라벨 추가
        self.progress_label = components.set_default_label("")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("font-size: 14px; margin: 10px;")

        # 입력 필드 설정
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Enter answer")
        self.answer_input.setMinimumSize(250, 35)
        self.answer_input.setStyleSheet(INPUT_STYLE)

        # 상태 라벨 설정
        self.state_label = components.set_default_label("------")
        self.state_label.setAlignment(Qt.AlignCenter)
        self.state_label.setStyleSheet("font-size: 14px; margin: 10px;")

        # 버튼 설정
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setStyleSheet(BUTTON_STYLE)
        self.submit_btn.setMinimumSize(120, 40)
        self.submit_btn.setShortcut(QKeySequence("return"))
        self.submit_btn.clicked.connect(self.handle_submit)

        self.correct_btn = QPushButton("Correct")
        self.correct_btn.setStyleSheet(BUTTON_STYLE)
        self.correct_btn.setMinimumSize(120, 40)
        self.correct_btn.clicked.connect(self.set_correct)
        self.correct_btn.setDisabled(True)
        
        self.back_btn = QPushButton('Back')
        self.back_btn.setStyleSheet(BUTTON_STYLE)
        self.back_btn.setMinimumSize(120, 40)
        self.back_btn.setShortcut(QKeySequence('x'))
        self.back_btn.clicked.connect(lambda: events.back_page(self.stack))

    def setup_layout(self):
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        
        widget_list = [
            self.title_label,
            self.progress_label,  # 진행 상황 라벨 추가
            self.answer_input,
            self.state_label,
            self.submit_btn,
            self.correct_btn,
            self.back_btn
        ]
        
        for widget in widget_list:
            if isinstance(widget, QLabel):
                vbox.addWidget(widget)
            elif isinstance(widget, QLineEdit):
                hbox = QHBoxLayout()
                hbox.addStretch(1)
                hbox.addWidget(widget)
                hbox.addStretch(1)
                vbox.addLayout(hbox)
            elif isinstance(widget, QPushButton):
                hbox = QHBoxLayout()
                hbox.addStretch(1)
                hbox.addWidget(widget)
                hbox.addStretch(1)
                vbox.addLayout(hbox)
                
        vbox.addStretch(1)
        self.widget.setLayout(vbox)

    def set_page(self):
        self.stack.addWidget(self.widget)
        self.stack.setCurrentIndex(self.stack.count() - 1)

    def set_correct(self):
        # 수동으로 정답 처리하는 함수
        # 새로운 정답을 추가할 수 있는 다이얼로그 표시
        word = self.game.get_question()
        score_result = self.game.set_score(word, 1)
        
        if score_result == dword.State.SUCCESS:
            self.correct_count += 1
            
            if self.last_answer:
                # 이전 답변을 QLineEdit에 미리 입력
                dialog = QDialog(self.widget)
                dialog.setWindowTitle('정답 추가')
                
                layout = QVBoxLayout()
                
                label = QLabel(f'방금 입력한 "{self.last_answer}"를 정답으로 추가하시겠습니까?')
                layout.addWidget(label)
                
                answer_input = QLineEdit()
                answer_input.setText(self.last_answer)
                layout.addWidget(answer_input)
                
                button_box = QDialogButtonBox(
                    QDialogButtonBox.Ok | QDialogButtonBox.Cancel
                )
                button_box.accepted.connect(dialog.accept)
                button_box.rejected.connect(dialog.reject)
                layout.addWidget(button_box)
                
                dialog.setLayout(layout)
                
                if dialog.exec_() == QDialog.Accepted:
                    new_answer = answer_input.text().strip()
                    if new_answer:
                        self.game.add_answer(word, new_answer)
                        self.state_label.setText(f"{word}: 정답 처리 (새로운 정답 '{new_answer}' 추가됨)")
                        self.last_answer = None
                        return
            
            # 다른 정답 추가를 위한 QLineEdit 다이얼로그
            dialog = QDialog(self.widget)
            dialog.setWindowTitle('정답 추가')
            
            layout = QVBoxLayout()
            
            label = QLabel('이 단어에 대한 다른 정답을 추가하시겠습니까?')
            layout.addWidget(label)
            
            answer_input = QLineEdit()
            layout.addWidget(answer_input)
            
            button_box = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            )
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)
            
            dialog.setLayout(layout)
            
            if dialog.exec_() == QDialog.Accepted:
                new_answer = answer_input.text().strip()
                if new_answer:
                    self.game.add_answer(word, new_answer)
                    self.state_label.setText(f"{word}: 정답 처리 (새로운 정답 '{new_answer}' 추가됨)")
                    self.state_label.setStyleSheet("color: green;")
                else:
                    self.state_label.setText(f"{word}: 정답 처리")
                    self.state_label.setStyleSheet("color: green;")
            else:
                self.state_label.setText(f"{word}: 정답 처리")
                self.state_label.setStyleSheet("color: green;")
            
        elif score_result == dword.State.NO_EXIST:
            self.state_label.setText(f"{word}: 정답 실패")
            self.state_label.setStyleSheet("color: red;")
    def handle_submit(self):
        # 제출 버튼 클릭 시 동작 처리
        # 게임이 시작된 경우: 답변 처리 또는 다음 문제로 이동
        # 게임이 시작되지 않은 경우: 게임 시작
        if self.game.is_start():
            if self.processing == True:
                self.process_answer()
            elif self.processing == False:
                self.next()
                self.state_label.setText("------")
                self.state_label.setStyleSheet("color: black;")
        else:
            self.start_game()
    def next(self):
        # 다음 문제로 이동하는 함수
        # 문제 카운트 증가 및 진행 상황 업데이트
        next_result = self.game.next()
        if next_result == dword.State.SUCCESS:
            self.title_label.setText(self.game.get_question())
            self.count += 1
            self.processing = True
            # 진행 상황 업데이트
            remain = self.game.get_remain_question()
            self.progress_label.setText(f"진행: {self.count}문제 / 남은 문제: {remain}문제")
        elif next_result == dword.State.END:
            self.end_game()
            self.processing = False
    def process_answer(self):
        # 사용자의 답변을 처리하는 함수
        # 정답/오답 여부 확인 및 결과 표시
        answer = self.answer_input.text()
        self.last_answer = answer
        answer_result = self.game.answer(answer)
        if answer_result == dword.State.CORRECT:
            self.correct_count += 1
            self.update_state_label(
                f"✓ {self.game.get_answer()} ({self.info_data[self.game.get_question()]})", 
                "green"
            )
        elif answer_result == dword.State.WRONG:
            self.update_state_label(
                f"✗ {self.game.get_answer()} ({self.info_data[self.game.get_question()]})", 
                "red"
            )
        self.answer_input.setText("")
        self.processing = False
        
        
    def start_game(self):
        # 게임 시작 함수
        # 초기 상태 설정 및 첫 문제 표시
        game_result = self.game.start()
        if game_result == dword.State.ALREADY:
            self.title_label.setText("Already started")
        elif game_result == dword.State.NO_DATA:
            self.title_label.setText("No data available")
        elif game_result == dword.State.SUCCESS:
            self.correct_btn.setDisabled(False)
            self.count = 1
            self.correct_count = 0
            self.title_label.setText(self.game.get_question())
            # 초기 진행 상황 표시
            remain = self.game.get_remain_question()
            self.progress_label.setText(f"진행: {self.count}문제 / 남은 문제: {remain}문제")
            self.processing = True

    def end_game(self):
        # 게임 종료 함수
        # 최종 점수 계산 및 결과 표시
        self.game.save_scores()
        percentage = round((self.correct_count / self.count) * 100)
        end_message = f"정답률: {percentage}% ({self.correct_count}/{self.count})\nEnter Again"
        self.title_label.setText(end_message)
        self.processing = False
        self.correct_btn.setDisabled(True)
        self.progress_label.setText("")  # 진행 상황 라벨 초기화

    def update_state_label(self, text, color):
        # 상태 라벨 업데이트 함수
        # 텍스트와 색상 변경
        self.state_label.setText(text)
        self.state_label.setStyleSheet(f"color: {color};")


