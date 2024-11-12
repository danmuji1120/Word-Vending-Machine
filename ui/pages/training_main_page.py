from PyQt5.QtWidgets import *
import components
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import events
import ui
import ui.pages
import dword
def set_training_main_page(stack: QStackedLayout):
  game = dword.Game()
  title_label = components.set_title_label("Training")
  start_btn = components.set_default_btn("Start")
  start_btn.clicked.connect(lambda: ui.pages.set_training_start_page(stack))
  add_btn = components.set_default_btn("Add")
  add_btn.clicked.connect(lambda: ui.pages.set_training_add_page(stack, game))
  delete_btn = components.set_default_btn("Delete")
  delete_btn.clicked.connect(lambda: ui.pages.set_training_delete_page(stack, game))
  list_btn = components.set_default_btn("List")
  # btn2 = components.set_default_btn("testB")
  # btn3 = components.set_default_btn("testC")
  back_btn = components.set_default_btn('back')
  back_btn.setShortcut(QKeySequence('x'))
  back_btn.clicked.connect(lambda: events.back_page(stack))


  widget_list = [title_label, start_btn, add_btn, delete_btn, list_btn, back_btn]
  # setting page as default
  components.set_default_page(widget_list, stack)

  # change page to current page
  stack.setCurrentIndex(stack.count() - 1)

