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

class TrainingStartPage:
  def __init__(self, stack) -> None:
    self.stack = stack
    self.widget = QWidget()
    self.game = dword.Game()
    self.info_data = self.game.get_info()
    self.count = 0
    self.correct_count = 0

    self.init_ui()

  def init_ui(self):
    self.title_label = components.set_title_label("Enter Start.")

    self.answer_input = QLineEdit()
    self.answer_input.setPlaceholderText("Enter answer")
    self.answer_input.setMaximumSize(200, 20)

    self.state_label = components.set_default_label("")

    self.submit_btn = components.set_default_btn("Submit")
    self.submit_btn.setShortcut(QKeySequence("return"))
    self.submit_btn.clicked.connect(lambda: self.handle_submit())
    self.back_btn = components.set_default_btn('Back')
    self.back_btn.setShortcut(QKeySequence('x'))
    self.back_btn.clicked.connect(lambda: events.back_page(self.stack))

    # layout = QVBoxLayout()
    # layout.addWidget(self.title_label)
    # layout.addWidget(self.answer_input)
    # layout.addWidget(self.submit_btn)
    # layout.addWidget(self.back_btn)
    # layout.addWidget(self.state_label)
    widgetlist = []
    widgetlist.append(self.title_label)
    widgetlist.append(self.answer_input)
    widgetlist.append(self.state_label)
    widgetlist.append(self.submit_btn)
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

  def handle_submit(self):
    if self.game.is_start():
      self.process_answer()
    else:
      self.start_game()
  def process_answer(self):
    answer = self.answer_input.text()
    answer_result = self.game.answer(answer)
    
    if answer_result == dword.State.CORRECT:
      self.correct_count += 1
      self.update_state_label(f"Correct, The answer to {self.game.get_question()} is {self.game.get_answer()}.\ninfo: {self.info_data[self.game.get_question()]}", "green")
    elif answer_result == dword.State.WRONG:
      self.update_state_label(f"Incorrect, The answer to {self.game.get_question()} is {self.game.get_answer()}.\ninfo: {self.info_data[self.game.get_question()]}", "red")
    self.answer_input.setText("")
    
    next_result = self.game.next()
    if next_result == dword.State.SUCCESS:
      self.title_label.setText(self.game.get_question())
      self.count += 1
    elif next_result == dword.State.END:
      self.end_game()
  def start_game(self):
      
      game_result = self.game.start()
      if game_result == dword.State.ALREADY:
          self.title_label.setText("Already started")
      elif game_result == dword.State.NO_DATA:
          self.title_label.setText("No data available")
      elif game_result == dword.State.SUCCESS:
          self.count = 1
          self.correct_count = 0
          self.title_label.setText(self.game.get_question())

  def end_game(self):
      self.game.save_scores()
      self.title_label.setText(f"{self.correct_count}/{self.count} Enter Again")
      # self.answer_input.setDisabled(True)
      # self.submit_btn.setDisabled(True)

  def update_state_label(self, text, color):
      self.state_label.setText(text)
      self.state_label.setStyleSheet(f"color: {color};")


def set_training_start_page(stack: QStackedLayout):
   train_start_page = TrainingStartPage(stack)
   train_start_page.set_page()