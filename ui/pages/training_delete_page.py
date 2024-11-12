
from PyQt5.QtWidgets import *
import components
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import events
import dword
def set_training_delete_page(stack: QStackedLayout, game:dword.Game):
  word_data = game.get_list()
  scroll_area = QScrollArea()
  scroll_area.setWidgetResizable(True)
  container_widget = QWidget()
  layout = QVBoxLayout()
  for word, meaning in word_data.items():
    label = QLabel(f"{word}: {meaning}")
    layout.addWidget(label)
  layout.setAlignment(Qt.AlignTop)
  container_widget.setLayout(layout)
  scroll_area.setWidget(container_widget)


  title_label = components.set_title_label("Delete")
  # question_label = components.set_title_label(string="단어",sort="left")
  word_input = QLineEdit()
  word_input.setPlaceholderText("단어")
  word_input.setMaximumSize(200, 20)
  # answer_labe = components.set_title_label(string="뜻",sort="left")
  add_btn = components.set_default_btn("Add")
  add_btn.setShortcut(QKeySequence('return'))
  add_btn.clicked.connect(lambda: delete(word_input, state_label, layout, game))
  state_label = components.set_default_label("state")

  back_btn = components.set_default_btn('back')
  back_btn.setShortcut(QKeySequence('x'))
  back_btn.clicked.connect(lambda: events.back_page(stack))
  
  vbox = QVBoxLayout()
  vbox.addStretch(1)
  widget_list = [title_label, word_input, add_btn, state_label, back_btn]
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


def delete(word_input: QLineEdit, state_label: QLabel, word_list: QVBoxLayout, game:dword.Game):
  word = word_input.text()
  word = word.strip()
  if (word.replace(" ", "") == ""):
    state_label.setText("put the word")
    state_label.setStyleSheet("color: red")
  else:
    add_result = game.delete(word)
    if add_result == dword.State.SUCCESS:
      for i in range(word_list.count()):
        widget = word_list.itemAt(i).widget()
        if widget and isinstance(widget, QLabel):  # QLabel만 확인
            text = widget.text().split(":")[0]
            if word == text:  # 텍스트에 word가 포함되면
                widget.deleteLater()  # 해당 QLabel을 삭제
      # label = QLabel(f"{question}: {answer}")
      # word_list.addWidget(label)
      state_label.setText("Success!")
      state_label.setStyleSheet("color: green")
      word_input.setText("")
    elif add_result == dword.State.DUPLICATION:
      state_label.setText("No Exist Word")
      state_label.setStyleSheet("color: red")
  word_input.setFocus()



