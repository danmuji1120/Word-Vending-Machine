from PyQt5.QtWidgets import *
def set_default_page(widgetlist: list, stack: QStackedLayout):
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        for i in widgetlist:
            print(i)
            if isinstance(i, QLabel):
                vbox.addWidget(i)
            elif isinstance(i, QLineEdit):
                vbox.addWidget(i)
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
            
        #vbox.addWidget(title_label)
        #vbox.addLayout(hbox_btn)
        vbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        
        inside_widget = QWidget()
        inside_widget.setLayout(hbox)

        stack.addWidget(inside_widget)