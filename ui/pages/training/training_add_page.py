from PyQt5.QtWidgets import *
import components
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import events
import dword
from ui.styles.styles import INPUT_STYLE, BUTTON_STYLE, TITLE_STYLE
def set_training_add_page(stack: QStackedLayout, section_name="commons"):
  train_add_page = TrainingAddPage(stack, section_name)
  train_add_page.set_page()
class TrainingAddPage:
    def __init__(self, stack, section_name) -> None:
        self.stack = stack
        self.section_name = section_name
        self.widget = QWidget()
        # 스크롤 영역 초기화
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.container_widget = QWidget()
        self.layout = QHBoxLayout()
        self.word_info_layout = QVBoxLayout()
        self.word_rate_layout = QVBoxLayout()

        # 게임 데이터 초기화
        self.game = dword.Game(self.section_name)
        self.word_data = self.game.get_list()
        self.info_data = self.game.get_info()
        self.rate_data = self.game.get_rate()
        
        # UI 요소 초기화
        self.init_ui()
        self.setup_word_list()
        self.setup_layout()
        
    def init_ui(self):
        self.title_label = components.set_title_label("단어 추가")
        self.title_label.setStyleSheet(TITLE_STYLE)
        
        
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("단어를 입력하세요")
        self.question_input.setMinimumSize(250, 35)
        self.question_input.setStyleSheet(INPUT_STYLE)
        
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("뜻을 입력하세요")
        self.answer_input.setMinimumSize(250, 35)
        self.answer_input.setStyleSheet(INPUT_STYLE)
        
        self.info_input = QLineEdit()
        self.info_input.setPlaceholderText("추가 정보를 입력하세요")
        self.info_input.setMinimumSize(250, 35)
        self.info_input.setStyleSheet(INPUT_STYLE)
        
        # 버튼에 공통 스타일 적용
        self.add_btn = QPushButton("추가")
        self.add_btn.setStyleSheet(BUTTON_STYLE)
        self.add_btn.setMinimumSize(120, 40)
        self.add_btn.setShortcut(QKeySequence('return'))
        self.add_btn.clicked.connect(self.add_word)
        
        self.back_btn = QPushButton("뒤로")
        self.back_btn.setStyleSheet(BUTTON_STYLE)
        self.back_btn.setMinimumSize(120, 40)
        self.back_btn.setShortcut(QKeySequence('x'))
        self.back_btn.clicked.connect(lambda: events.back_page(self.stack))
        
        self.state_label = QLabel()
        self.state_label.setAlignment(Qt.AlignCenter)
        self.state_label.setStyleSheet("font-size: 14px; margin: 10px;")

    def setup_word_list(self):
        # 전체 단어 개수와 추가 가능한 단어 개수를 표시하는 레이아웃
        counts_layout = QHBoxLayout()
        
        total_words_label = QLabel(f"전체 단어 수: {len(self.word_data)}개")
        total_words_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
        """)
        
        available_words = self.game.get_available_word_count()
        available_label = QLabel(f"추가 가능한 단어 수: {available_words}개")
        available_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #27ae60;
            padding: 10px;
        """)
        
        counts_layout.addWidget(total_words_label)
        counts_layout.addWidget(available_label)
        counts_layout.addStretch()
        
        self.word_info_layout.addLayout(counts_layout)

        # 기존 코드
        for word, meaning in self.word_data.items():
            self.add_word_to_list(word, meaning, self.info_data[word], self.rate_data[word])
            
        self.word_info_layout.setAlignment(Qt.AlignTop)
        self.word_rate_layout.setAlignment(Qt.AlignTop)
        self.layout.addLayout(self.word_info_layout)
        self.layout.addLayout(self.word_rate_layout)
        
    def add_word_to_list(self, word, meaning, info, rate):
        # 단어 리스트 아이템 스타일 개선
        word_container = QWidget()
        word_layout = QHBoxLayout()
        
        word_info = QLabel(f"{word}: {meaning}")
        word_info.setStyleSheet("font-size: 14px; font-weight: bold;")
        
        info_label = QLabel(f"({info})")
        info_label.setStyleSheet("font-size: 12px; color: #666;")
        
        rate_label = QLabel(f"{int(rate)}%")
        rate_label.setMinimumWidth(50)
        
        if int(rate) >= 90:
            rate_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
        elif int(rate) >= 30:
            rate_label.setStyleSheet("color: #f39c12; font-weight: bold;")
        else:
            rate_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
            
        word_layout.addWidget(word_info)
        word_layout.addWidget(info_label)
        word_layout.addStretch()
        word_layout.addWidget(rate_label)
        
        word_container.setLayout(word_layout)
        word_container.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 5px;
                padding: 8px;
                margin: 2px;
            }
            QWidget:hover {
                background: #f8f9fa;
            }
        """)
        
        self.word_info_layout.addWidget(word_container)

    def setup_layout(self):
        # 입력 폼 레이아웃
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        
        widget_list = [
            self.title_label, self.question_input, self.answer_input, 
            self.info_input, self.add_btn, self.state_label, self.back_btn
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
                widget.setMinimumSize(100, 30)
                hbox = QHBoxLayout()
                hbox.addStretch(1)
                hbox.addWidget(widget)
                hbox.addStretch(1)
                vbox.addLayout(hbox)
                
        vbox.addStretch(1)
        
        # 메인 레이아웃
        self.container_widget.setLayout(self.layout)
        self.scroll_area.setWidget(self.container_widget)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.scroll_area)
        hbox.addLayout(vbox)
        
        self.widget.setLayout(hbox)
        self.stack.addWidget(self.widget)
        self.stack.setCurrentIndex(self.stack.count() - 1)

    def add_word(self):
        if self.game.get_available_word_count() <= 0:
            self.state_label.setText("더 이상 단어를 추가할 수 없습니다")
            self.state_label.setStyleSheet("color: red")
            return
        
        question = self.question_input.text().strip()
        answer = self.answer_input.text().strip()
        info = self.info_input.text().strip()
        
        if not question.replace(" ", "") or not answer.replace(" ", ""):
            self.state_label.setText("단어를 입력하세요")
            self.state_label.setStyleSheet("color: red")
            return
        print(f"question: {question}, answer: {answer}, info: {info}")
        add_result = self.game.add(question, answer, info)
        
        if add_result == dword.State.SUCCESS:
            self.add_word_to_list(question, answer, info, 0)
            # 단어 수 레이블들 업데이트
            counts_layout = self.word_info_layout.itemAt(0)
            total_label = counts_layout.itemAt(0).widget()
            available_label = counts_layout.itemAt(1).widget()
            
            total_label.setText(f"전체 단어 수: {len(self.word_data) + 1}개")
            available_label.setText(f"추가 가능한 단어 수: {self.game.get_available_word_count()}개")
            
            self.state_label.setText("추가되었습니다!")
            self.state_label.setStyleSheet("color: green")
            self.clear_inputs()
        elif add_result == dword.State.DUPLICATION:
            self.state_label.setText("이미 존재하는 단어입니다")
            self.state_label.setStyleSheet("color: red")
        elif add_result == dword.State.FULL:
            self.state_label.setText("더 이상 단어를 추가할 수 없습니다")
            self.state_label.setStyleSheet("color: red")
            
        self.question_input.setFocus()
        
    def clear_inputs(self):
        self.question_input.setText("")
        self.answer_input.setText("")
        self.info_input.setText("")
    def set_page(self):
        self.stack.addWidget(self.widget)
        self.stack.setCurrentIndex(self.stack.count() - 1)



