from PyQt5.QtWidgets import *
import components
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import ui
import ui.pages
def set_main_page(stack: QStackedLayout):
  title_label = components.set_title_label("Word Test")
  study_btn = components.set_default_btn("Study")
  exit_btn = components.set_default_btn("Exit")
  study_btn.clicked.connect(lambda: ui.pages.set_training_main_page(stack))
  exit_btn.clicked.connect(QCoreApplication.instance().quit)
  widget_list = [title_label, study_btn, exit_btn]
  components.set_default_page(widget_list, stack)