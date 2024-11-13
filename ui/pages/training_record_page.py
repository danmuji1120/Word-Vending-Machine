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

class TrainingRecordPage:
  def __init__(self, stack) -> None:
    self.stack = stack
    self.widget = QWidget()
    self.game = dword.Game()
    self.init_ui()

  def init_ui(self):
    self.title_label = components.set_title_label("Record")

    self.correct_rate_btn = components.set_default_btn("정답률")
    self.daily_count_btn = components.set_default_btn("하루별 개수")
    self.daily_count_btn.clicked.connect(lambda: dword.show_daily_count(self.game.record.get_rememeber_date()))
    self.month_count_btn = components.set_default_btn("월별 개수")
    self.back_btn = components.set_default_btn('Back')
    self.back_btn.setShortcut(QKeySequence('x'))
    self.back_btn.clicked.connect(lambda: events.back_page(self.stack))

    widgetlist = []
    widgetlist.append(self.title_label)
    widgetlist.append(self.correct_rate_btn)
    widgetlist.append(self.daily_count_btn)
    widgetlist.append(self.month_count_btn)
    widgetlist.append(self.back_btn)

    vbox = QVBoxLayout()
    vbox.addStretch(1)
    for i in widgetlist:
        print(i)
        if isinstance(i, QLabel):
            vbox.addWidget(i)
        elif isinstance(i, QLineEdit):
            hbox_line = QHBoxLayout()
            hbox_line.addStretch(1)
            hbox_line.addWidget(i)
            hbox_line.addStretch(1)
            vbox.addLayout(hbox_line)
        elif isinstance(i, QPushButton):
            i.setMinimumSize(100, 30)
            hbox_btn = QHBoxLayout()
            hbox_btn.addStretch(1)
            hbox_btn.addWidget(i)
            hbox_btn.addStretch(1)
            vbox.addLayout(hbox_btn)
        elif type(i) == list:
            hbox_list = QHBoxLayout()
            for j in i:
                hbox_list.addWidget(j)
            vbox.addLayout(hbox_list)
        else:
            print('추가 실패')

    # self.setLayout(layout)
    vbox.addStretch(1)
    self.widget.setLayout(vbox)
  def set_page(self):
    self.stack.addWidget(self.widget)
    self.stack.setCurrentIndex(self.stack.count() - 1)


def set_training_record_page(stack: QStackedLayout):
   train_record_page = TrainingRecordPage(stack)
   train_record_page.set_page()