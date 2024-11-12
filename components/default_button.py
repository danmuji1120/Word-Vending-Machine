from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

def set_default_btn(string='button', font='나눔스퀘어 ExtraBold', size=12, bold=False) -> QPushButton:
    btn = QPushButton(string)
    btn.setFont(QFont(font))
    title_font = btn.font()
    title_font.setPointSize(size)
    title_font.setBold(bold)
    btn.setFont(title_font)
    # btn.setMinimumSize(200, 0)
    btn.resize(10, 10)
    return btn
