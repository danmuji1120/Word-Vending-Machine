from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def set_title_label(string='Title Label', font='나눔스퀘어 ExtraBold', size=40, bold=True, sort='center') -> QLabel:
    label = QLabel(string)
    label.setFont(QFont(font))
    if sort == 'center':
        label.setAlignment(Qt.AlignCenter)
    elif sort == 'left':    
        label.setAlignment(Qt.AlignLeft)
    elif sort == 'right':    
        label.setAlignment(Qt.AlignRight)
    title_font = label.font()
    title_font.setPointSize(size)
    title_font.setBold(bold)
    label.setFont(title_font)
    return label
