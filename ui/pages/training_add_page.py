
from PyQt5.QtWidgets import *
import components
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import events
import dword
def set_training_add_page(stack: QStackedLayout, game:dword.Game):
  word_data = game.get_list()
  info_data = game.get_info()
  rate_data = game.get_rate_all()
  scroll_area = QScrollArea()
  scroll_area.setWidgetResizable(True)
  container_widget = QWidget()
  layout = QHBoxLayout()
  # layout = QVBoxLayout()
  word_info_layout = QVBoxLayout()
  word_rate_layout = QVBoxLayout()
  for word, meaning in word_data.items():
    word_info = QLabel(f"{word}: {meaning} ({info_data[word]})")
    word_rate = QLabel(f"{int(rate_data[word])}%")
    if int(rate_data[word]) >= 90:
       word_rate.setStyleSheet("color: green;")
    elif int(rate_data[word]) >= 30:
       word_rate.setStyleSheet("color: orange;")
    else:
       word_rate.setStyleSheet("color: red;")
       
    word_info_layout.addWidget(word_info)
    word_rate_layout.addWidget(word_rate)
  word_info_layout.setAlignment(Qt.AlignTop)
  word_rate_layout.setAlignment(Qt.AlignTop)
  layout.addLayout(word_info_layout)
  layout.addLayout(word_rate_layout)
  container_widget.setLayout(layout)
  scroll_area.setWidget(container_widget)

  title_label = components.set_title_label("Add")
  # question_label = components.set_title_label(string="단어",sort="left")
  question_input = QLineEdit()
  question_input.setPlaceholderText("단어")
  question_input.setMaximumSize(200, 20)
  # answer_labe = components.set_title_label(string="뜻",sort="left")
  answer_input = QLineEdit()
  answer_input.setPlaceholderText("뜻")
  answer_input.setMaximumSize(200, 20)
  info_input = QLineEdit()
  info_input.setPlaceholderText("정보")
  info_input.setMaximumSize(200, 20)
  add_btn = components.set_default_btn("Add")
  add_btn.setShortcut(QKeySequence('return'))
  add_btn.clicked.connect(lambda: add(question_input, answer_input, info_input, state_label, word_info_layout, word_rate_layout, game))
  state_label = components.set_default_label("state")

  back_btn = components.set_default_btn('back')
  back_btn.setShortcut(QKeySequence('x'))
  back_btn.clicked.connect(lambda: events.back_page(stack))
  
  vbox = QVBoxLayout()
  vbox.addStretch(1)
  widget_list = [title_label, question_input, answer_input, info_input, add_btn, state_label, back_btn]
  for i in widget_list:
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
  vbox.addStretch(1)
  hbox = QHBoxLayout()
  hbox.addWidget(scroll_area)
  hbox.addLayout(vbox)
  # change page to current page
  main_widget = QWidget()
  main_widget.setLayout(hbox)
  stack.addWidget(main_widget)
  stack.setCurrentIndex(stack.count() - 1)


def add(question_input: QLineEdit, answer_input: QLineEdit, info_input: QLineEdit, state_label: QLabel, word_info_layout: QVBoxLayout, word_rate_layout: QVBoxLayout, game:dword.Game):
  question = question_input.text()
  answer = answer_input.text()
  info = info_input.text()

  question = question.strip()
  answer = answer.strip()
  info = info.strip()
  if (question.replace(" ", "") == "" or answer.replace(" ", "") == ""):
    state_label.setText("put the word")
    state_label.setStyleSheet("color: red")
  else:
    add_result = game.add([question, answer, info])
    if add_result == dword.State.SUCCESS:
      word_info = QLabel(f"{question}: {answer} ")
      word_rate = QLabel(f"0%")
      word_rate.setStyleSheet("color: red;")
      word_info_layout.addWidget(word_info)
      word_rate_layout.addWidget(word_rate)
      state_label.setText("Success!")
      state_label.setStyleSheet("color: green")
      question_input.setText("")
      answer_input.setText("")
      info_input.setText("")
    elif add_result == dword.State.DUPLICATION:
      state_label.setText("Exist word")
      state_label.setStyleSheet("color: red")
  question_input.setFocus()




