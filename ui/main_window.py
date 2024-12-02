from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from PyQt5.QtGui import *
from ui.pages import *
import components

class MainWindow(QMainWindow):
    stack_layout = QStackedLayout()
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        set_main_page(self.stack_layout)
        main_widget = QWidget()
        main_widget.setLayout(self.stack_layout)
        self.setCentralWidget(main_widget)
        self.setGeometry(10, 10, 700, 500)
        self.show()
    
    def getStack(self) -> QStackedLayout:
        return self.stack_layout
