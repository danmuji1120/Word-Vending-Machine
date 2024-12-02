from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
import components
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import events
import dword
from ui.styles.styles import TITLE_STYLE, BUTTON_STYLE
from dword.analysis import Analysis

class TrainingRecordPage:
  def __init__(self, stack, section_name="commons") -> None:
    self.stack = stack
    self.section_name = section_name
    self.widget = QWidget()
    self.game = dword.Game(self.section_name)
    # self.graph = dword.Graph(self.game.record.load_file())
    self.table = QTableWidget()
    self.init_ui()
  def init_ui(self):
    self.back_btn = components.set_default_btn('Back')
    self.back_btn.setShortcut(QKeySequence('x'))
    self.back_btn.setStyleSheet(BUTTON_STYLE)
    self.back_btn.clicked.connect(lambda: events.back_page(self.stack))

    # Analysis 객체 생성
    self.analysis = Analysis(self.game.word_manager, self.game.record)
    
    # 단어 기록 가져오기
    memory_history = self.analysis.get_word_memory_history()
    words = self.game.word_manager.get_word_list()
    
    # 날짜 범위 구하기
    dates = sorted(memory_history.keys())
    
    # 테이블 설정
    self.table.setRowCount(len(words))
    self.table.setColumnCount(len(dates) + 1)  # +1은 단어 열을 위함
    
    # 헤더 설정
    headers = ['단어'] + dates
    self.table.setHorizontalHeaderLabels(headers)
    self.table.setVerticalHeaderLabels([''] * len(words))

    self.word_added_date_dict = self.game.word_manager.get_date_dict()
    
    # 현재 외운 단어와 외우지 못한 단어 목록 가져오기
    memorized_words = self.analysis.get_memorized_words()
    not_memorized_words = self.analysis.get_not_memorized_words()
    
    # 단어 열 채우기
    for i, word in enumerate(words):
        item = QTableWidgetItem(word)
        if word in memorized_words:
            item.setBackground(QColor(144, 238, 144))  # 연한 초록색
        elif word in not_memorized_words:
            item.setBackground(QColor(255, 182, 193))  # 연한 빨간색
        self.table.setItem(i, 0, item)
        
        # 각 날짜별 상태 채우기
        for j, date in enumerate(dates, 1):
            item = QTableWidgetItem()
            added_date = self.word_added_date_dict[word][:10]
            if added_date == date:
               item.setText("추가")
            if word in memory_history[date]['memorized']:
                item.setBackground(QColor(144, 238, 144))  # 연한 초록색
            elif word in memory_history[date]['forgotten']:
                item.setBackground(QColor(255, 182, 193))  # 연한 빨간색
            
            # # 복습 여부 확인
            # df = self.game.record.load_file()
            # date_records = df[df['date'].str.startswith(date)]
            # if not date_records.empty and word in date_records.columns:
            #     word_records = date_records[word]
            #     if (word_records == 1).any():
            #         item.setBackground(QColor(173, 216, 230))  # 연한 파란색
            
            self.table.setItem(i, j, item)
    
    # 테이블 스타일 설정
    self.table.setStyleSheet("""
        QTableWidget {
            background-color: white;
            gridline-color: #d3d3d3;
        }
        QHeaderView::section {
            background-color: #f0f0f0;
            padding: 5px;
            border: 1px solid #d3d3d3;
        }
    """)
    
    # 테이블 크기 조정
    self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    self._setup_layout()

  def _setup_layout(self):
    widgetlist = [
        self.table,  # 테이블 추가
        self.back_btn
    ]

    vbox = QVBoxLayout()
    # vbox.addStretch(1)
    vbox.setSpacing(20)

    for widget in widgetlist:
        if isinstance(widget, QLabel):
            vbox.addWidget(widget, alignment=Qt.AlignCenter)
        elif isinstance(widget, QPushButton):
            widget.setMinimumSize(200, 40)
            hbox = QHBoxLayout()
            # hbox.addStretch(1)
            hbox.addWidget(widget)
            # hbox.addStretch(1)
            vbox.addLayout(hbox)
        elif isinstance(widget, QTableWidget):
            vbox.addWidget(widget)

    # vbox.addStretch(1)
    self.widget.setLayout(vbox)


  def set_page(self):
    self.stack.addWidget(self.widget)
    self.stack.setCurrentIndex(self.stack.count() - 1)


def set_training_record_page(stack: QStackedLayout, section_name="commons"):
   train_record_page = TrainingRecordPage(stack, section_name)
   train_record_page.set_page()