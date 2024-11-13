from PyQt5.QtWidgets import *
import components
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import events
import ui
import ui.pages
from ui.styles.styles import BUTTON_STYLE, TITLE_STYLE

def set_training_main_page(stack: QStackedLayout):
    # 타이틀 설정
    title_label = components.set_title_label("Training")
    title_label.setStyleSheet(TITLE_STYLE)
    
    # 버튼 생성 및 스타일 적용
    buttons = [
        ("Start", lambda: ui.pages.set_training_start_page(stack)),
        ("Record", lambda: ui.pages.set_training_record_page(stack)),
        ("Add", lambda: ui.pages.set_training_add_page(stack)),
        ("Delete", lambda: ui.pages.set_training_delete_page(stack)),
        ("List", None),
        ("Back", lambda: events.back_page(stack))
    ]
    
    widget_list = [title_label]
    
    for text, callback in buttons:
        btn = components.set_default_btn(text)
        btn.setStyleSheet(BUTTON_STYLE)
        if callback:
            btn.clicked.connect(callback)
        widget_list.append(btn)
    
    # Back 버튼 단축키 설정
    widget_list[-1].setShortcut(QKeySequence('x'))

    # 페이지 설정
    components.set_default_page(widget_list, stack)
    stack.setCurrentIndex(stack.count() - 1)

