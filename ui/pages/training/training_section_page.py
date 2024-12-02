from PyQt5.QtWidgets import *
import components
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import events
import ui
# import ui.pages.training
from ui.styles.styles import BUTTON_STYLE, TITLE_STYLE, STATE_BOX_STYLE, STATE_LABEL_STYLE
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
from matplotlib import font_manager, rc
from dword.word_manager import WordManager
from dword.recordManager import Record
from dword.analysis import Analysis
from dword.section_manager import SectionManager
from functools import partial  # functools 모듈에서 partial을 임포트

def set_training_section_page(stack: QStackedLayout):
    train_main_page = TrainingSectionPage(stack)
    train_main_page.set_page()

class TrainingSectionPage:
    def __init__(self, stack) -> None:
        self.stack = stack
        self.widget = QWidget()
        self.hbox = QHBoxLayout()  # 메인 레이아웃을 수평으로 변경
        self.vbox = QVBoxLayout()  # 기존 버튼용 레이아웃
        self.section_manager = SectionManager()
        
        self.init_ui()
        self.setup_layout()
        
    def init_ui(self):
        # 타이틀 설정
        self.title_label = components.set_title_label("Section")
        self.title_label.setStyleSheet(TITLE_STYLE)
        self.section_list = self.section_manager.get_section_list()
        # 버튼 설정
        self.buttons = []
        for section in self.section_list:
            self.buttons.append((section, partial(ui.pages.training.set_training_main_page, self.stack, section)))  # partial을 사용하여 section을 고정

        self.buttons.append(("+", lambda: self.open_add_section_popup()))
        self.buttons.append(("Back", lambda: events.back_page(self.stack)))
        self.widget_list = [self.title_label]
        
        for text, callback in self.buttons:
            btn = components.set_default_btn(text)
            btn.setStyleSheet(BUTTON_STYLE)
            if callback:
                btn.clicked.connect(callback)
            self.widget_list.append(btn)
        
        # Back 버튼 단축키 설정
        self.widget_list[-1].setShortcut(QKeySequence('x'))
        
        # 새로운 섹션 추가 버튼 설정
        
        
    def setup_layout(self):
        # 기존 버튼 이아웃 설정
        self.vbox.addStretch(1)
        for widget in self.widget_list:
            if isinstance(widget, QLabel):
                self.vbox.addWidget(widget)
            elif isinstance(widget, QLineEdit):
                hbox = QHBoxLayout()
                hbox.addStretch(1)
                hbox.addWidget(widget)
                hbox.addStretch(1)
                self.vbox.addLayout(hbox)
            elif isinstance(widget, QPushButton):
                widget.setMinimumSize(100, 30)
                hbox = QHBoxLayout()
                hbox.addStretch(1)
                hbox.addWidget(widget)
                hbox.addStretch(1)
                self.vbox.addLayout(hbox)
        self.vbox.addStretch(1)
        
        # 메인 레이아웃에 통계와 버튼 배치
        # self.hbox.addLayout(self.stats_vbox, stretch=2)
        self.hbox.addLayout(self.vbox, stretch=1)
        
        self.widget.setLayout(self.hbox)
        
    def set_page(self):
        self.stack.addWidget(self.widget)
        self.stack.setCurrentIndex(self.stack.count() - 1)

    def open_add_section_popup(self):
        text, ok = QInputDialog.getText(self.widget, 'Add Section', 'Enter section name:')
        if ok and text:
            self.section_manager.add_section(text)  # 섹션 추가 함수 호출
        self.refresh_page()

    def refresh_page(self):
        # 현재 페이지의 모든 요소를 제거
        self.widget.deleteLater()  # 위젯 삭제
        self.widget = QWidget()  # 새로운 위젯 생성
        self.hbox = QHBoxLayout()  # 새로운 수평 레이아웃 생성
        self.vbox = QVBoxLayout()  # 새로운 수직 레이아웃 생성
        self.section_manager = SectionManager()  # 섹션 관리자 재설정
        
        self.init_ui()  # UI 초기화
        self.setup_layout()  # 레이아웃 설정
        self.stack.addWidget(self.widget)  # 스택에 새로운 위젯 추가
        self.stack.setCurrentIndex(self.stack.count() - 1)  # 현재 인덱스 설정
