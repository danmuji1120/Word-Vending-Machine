# 인풋 스타일
INPUT_STYLE = """
    QLineEdit {
        padding: 8px;
        border: 2px solid #e0e0e0;
        border-radius: 5px;
        background: white;
        font-size: 14px;
    }
    QLineEdit:focus {
        border: 2px solid #000000;
    }
"""
# 버튼 스타일
BUTTON_STYLE = """
    QPushButton {
        background-color: white;
        border: 3px solid #2C2D26;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: 500;
        color: black;
        min-width: 150px;
    }
    QPushButton:hover {
        background-color: #2C2D26;
        color: white;
    }
    QPushButton:pressed {
        background-color: #333333;
    }
"""

# 타이틀 스타일
TITLE_STYLE = """
    QLabel {
        font-size: 36px;
        font-weight: bold;
        color: #000000;
        margin: 15px;
    }
""" 


BOX_STYLE = """
    QGroupBox {
        position: relative;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
"""
STATE_BOX_STYLE = """
    QWidget {
        background: white;
        border-radius: 5px;
        padding: 8px;
        margin: 2px;
    }
    QWidget:hover {
        background: #f8f9fa;
    }
"""

STATE_LABEL_STYLE = """
    QLabel {
        text-align: center;
        font-weight: bolder;
        font-size: 15px;
    }
"""