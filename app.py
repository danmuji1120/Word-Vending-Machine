## Ex 3-3. 창 닫기.
import ui
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QStackedLayout, QGridLayout, QScrollArea, QComboBox, QLineEdit, QCheckBox
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ui.MainWindow()
    sys.exit(app.exec_())