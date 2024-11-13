from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
import components
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import events
import ui
import ui.pages
import dword
from ui.styles.styles import TITLE_STYLE, BUTTON_STYLE

class TrainingRecordPage:
  def __init__(self, stack) -> None:
    self.stack = stack
    self.widget = QWidget()
    self.game = dword.Game()
    self.graph = dword.Graph(self.game.record.load_file())
    self.init_ui()
  def init_ui(self):
    self.title_label = components.set_title_label("Record")
    self.title_label.setStyleSheet(TITLE_STYLE)

    self.correct_rate_btn = components.set_default_btn("정답률")
    self.correct_rate_btn.setStyleSheet(BUTTON_STYLE)
    # self.correct_rate_btn.clicked.connect(self.show_correct_rate)
    self.daily_count_btn = components.set_default_btn("하루별 개수")
    self.daily_count_btn.setStyleSheet(BUTTON_STYLE)
    self.daily_count_btn.clicked.connect(self.graph.show_memorized_daily_graph)
    self.month_count_btn = components.set_default_btn("월별 개수")
    self.month_count_btn.setStyleSheet(BUTTON_STYLE)
    self.month_count_btn.clicked.connect(self.graph.show_memorized_monthly_graph)
    self.year_count_btn = components.set_default_btn("연도별 개수")
    self.year_count_btn.setStyleSheet(BUTTON_STYLE)
    self.year_count_btn.clicked.connect(self.graph.show_memorized_yearly_graph)
    self.back_btn = components.set_default_btn('Back')
    self.back_btn.setShortcut(QKeySequence('x'))
    self.back_btn.setStyleSheet(BUTTON_STYLE)
    self.back_btn.clicked.connect(lambda: events.back_page(self.stack))

    self._setup_layout()

  def _setup_layout(self):
    widgetlist = [
        self.title_label,
        self.correct_rate_btn,
        self.daily_count_btn,
        self.month_count_btn,
        self.year_count_btn,
        self.back_btn
    ]

    vbox = QVBoxLayout()
    vbox.addStretch(1)
    vbox.setSpacing(20)

    for widget in widgetlist:
        if isinstance(widget, QLabel):
            vbox.addWidget(widget, alignment=Qt.AlignCenter)
        elif isinstance(widget, QPushButton):
            widget.setMinimumSize(200, 40)
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


def set_training_record_page(stack: QStackedLayout):
   train_record_page = TrainingRecordPage(stack)
   train_record_page.set_page()