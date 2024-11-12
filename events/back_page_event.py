from PyQt5.QtWidgets import *

# 뒤로가는 이벤트
def back_page(stack: QStackedLayout):
    widget_to_remove = stack.widget(stack.count() - 1)
    stack.removeWidget(widget_to_remove)   # 레이아웃에서 제거
    widget_to_remove.deleteLater()         # 메모리에서 삭제 요청
    stack.setCurrentIndex(stack.count() - 1)
    

# def back_page(stack: QStackedLayout):
  # stack.removeWidget(stack.widget(stack.count() -1))
  # stack.setCurrentIndex(stack.count() -1)
  # print(stack.count())