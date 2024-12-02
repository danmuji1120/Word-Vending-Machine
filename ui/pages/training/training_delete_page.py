from PyQt5.QtWidgets import *
import components
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import events
import dword
from ui.styles.styles import TITLE_STYLE, INPUT_STYLE, BUTTON_STYLE

def set_training_delete_page(stack: QStackedLayout, section_name="commons"):
    train_delete_page = TrainingDeletePage(stack, section_name)
    train_delete_page.set_page()

class TrainingDeletePage:
    def __init__(self, stack, section_name = "commons") -> None:
        self.stack = stack
        self.section_name = section_name
        self.game = dword.Game(section_name=self.section_name)
        self.widget = QWidget()
        
        # 스크롤 영역 초기화
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.container_widget = QWidget()
        self.layout = QHBoxLayout()
        self.word_info_layout = QVBoxLayout()
        self.word_rate_layout = QVBoxLayout()

        # 게임 데이터 초기화
        self.word_data = self.game.get_list()
        self.info_data = self.game.get_info()
        self.rate_data = self.game.get_rate_all()
        
        # UI 요소 초기화
        self.init_ui()
        self.setup_word_list()
        self.setup_layout()

    def init_ui(self):
        self.title_label = components.set_title_label("단어 삭제")
        self.title_label.setStyleSheet(TITLE_STYLE)
        
        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("삭제할 단어를 입력하세요")
        self.word_input.setMinimumSize(250, 35)
        self.word_input.setStyleSheet(INPUT_STYLE)
        
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.setStyleSheet(BUTTON_STYLE)
        self.delete_btn.setMinimumSize(120, 40)
        self.delete_btn.setShortcut(QKeySequence('return'))
        self.delete_btn.clicked.connect(self.delete_word)
        
        self.back_btn = QPushButton("뒤로")
        self.back_btn.setStyleSheet(BUTTON_STYLE)
        self.back_btn.setMinimumSize(120, 40)
        self.back_btn.setShortcut(QKeySequence('x'))
        self.back_btn.clicked.connect(lambda: events.back_page(self.stack))
        
        self.state_label = QLabel()
        self.state_label.setAlignment(Qt.AlignCenter)
        self.state_label.setStyleSheet("font-size: 14px; margin: 10px;")

    def setup_word_list(self):
        for word, meaning in self.word_data.items():
            self.add_word_to_list(word, meaning, self.info_data[word], self.rate_data[word])
            
        self.word_info_layout.setAlignment(Qt.AlignTop)
        self.word_rate_layout.setAlignment(Qt.AlignTop)
        self.layout.addLayout(self.word_info_layout)
        self.layout.addLayout(self.word_rate_layout)

    def add_word_to_list(self, word, meaning, info, rate):
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
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        
        widget_list = [
            self.title_label, self.word_input, 
            self.delete_btn, self.state_label, self.back_btn
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
        
        self.container_widget.setLayout(self.layout)
        self.scroll_area.setWidget(self.container_widget)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.scroll_area)
        hbox.addLayout(vbox)
        
        self.widget.setLayout(hbox)

    def delete_word(self):
        word = self.word_input.text().strip()
        
        if not word.replace(" ", ""):
            self.state_label.setText("단어를 입력하세요")
            self.state_label.setStyleSheet("color: red")
            return
            
        delete_result = self.game.delete(word)
        
        if delete_result == dword.State.SUCCESS:
            # 단어 목록에서 삭제된 단어 제거
            for i in reversed(range(self.word_info_layout.count())):
                widget = self.word_info_layout.itemAt(i).widget()
                if widget:
                    text = widget.findChild(QLabel).text().split(":")[0]
                    if word == text:
                        widget.deleteLater()
                        break
                        
            self.state_label.setText("삭제 성공!")
            self.state_label.setStyleSheet("color: green")
            self.word_input.setText("")
        else:
            self.state_label.setText("존재하지 않는 단어입니다")
            self.state_label.setStyleSheet("color: red")
            
        self.word_input.setFocus()

    def set_page(self):
        self.stack.addWidget(self.widget)
        self.stack.setCurrentIndex(self.stack.count() - 1)




