from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import components
import events
import dword
from ui.styles.styles import INPUT_STYLE, BUTTON_STYLE, TITLE_STYLE

def set_training_start_page(stack: QStackedLayout):
    train_start_page = TrainingStartPage(stack)
    train_start_page.set_page()

class TrainingStartPage:
    def __init__(self, stack) -> None:
        self.stack = stack
        self.widget = QWidget()
        self.game = dword.Game()
        self.info_data = self.game.get_info()
        self.count = 0
        self.correct_count = 0
        self.processing = False

        self.init_ui()
        self.setup_layout()

    def init_ui(self):
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
        self.state_label = components.set_default_label("")
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

    def set_correct(self): # 강제 정답 처리
        word = self.game.get_question()
        score_result = self.game.set_score(word, 1)
        if score_result == dword.State.SUCCESS:
            self.correct_count += 1
            self.state_label.setText(f"{word}: 정답 처리")
            self.state_label.setStyleSheet("color: green;")
        elif score_result == dword.State.NO_EXIST:
            self.state_label.setText(f"{word}: 정답 실패")
            self.state_label.setStyleSheet("color: red;")
           
    def handle_submit(self):
        if self.game.is_start():
            if self.processing == True:
                self.process_answer()
            elif self.processing == False:
                self.next()
                self.state_label.setText("")
                self.state_label.setStyleSheet("color: black;")
        else:
            self.start_game()
    def next(self):
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
        answer = self.answer_input.text()
        answer_result = self.game.answer(answer)
        if answer_result == dword.State.CORRECT:
            self.correct_count += 1
            self.update_state_label(
                f"✓ {self.game.get_answer()}\n\n{self.info_data[self.game.get_question()]}", 
                "green"
            )
        elif answer_result == dword.State.WRONG:
            self.update_state_label(
                f"✗ {self.game.get_answer()}\n\n{self.info_data[self.game.get_question()]}", 
                "red"
            )
        self.answer_input.setText("")
        self.processing = False
        
        
    def start_game(self):
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
        self.game.save_scores()
        percentage = round((self.correct_count / self.count) * 100)
        end_message = f"정답률: {percentage}% ({self.correct_count}/{self.count})\nEnter Again"
        self.title_label.setText(end_message)
        self.processing = False
        self.correct_btn.setDisabled(True)
        self.progress_label.setText("")  # 진행 상황 라벨 초기화

    def update_state_label(self, text, color):
        self.state_label.setText(text)
        self.state_label.setStyleSheet(f"color: {color};")


