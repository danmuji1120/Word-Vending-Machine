from PyQt5.QtWidgets import *
import components
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import events
import ui
import ui.pages.training
from ui.styles.styles import BUTTON_STYLE, TITLE_STYLE, STATE_BOX_STYLE, STATE_LABEL_STYLE
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
from matplotlib import font_manager, rc
from dword.word_manager import WordManager
from dword.recordManager import Record
from dword.analysis import Analysis
def set_training_main_page(stack: QStackedLayout, section_name="commons"):
    print(f"선택된 세션: {section_name}")
    train_main_page = TrainingMainPage(stack, section_name)
    train_main_page.set_page()

class TrainingMainPage:
    def __init__(self, stack, section_name="commons") -> None:
        self.stack = stack
        self.section_name = section_name
        self.widget = QWidget()
        self.hbox = QHBoxLayout()  # 메인 레이아웃을 수평으로 변경
        self.vbox = QVBoxLayout()  # 기존 버튼용 레이아웃
        self.stats_vbox = QVBoxLayout()  # 통계 차트용 레이아웃
        self.scroll_area = QScrollArea()  # 스크롤 영역 추가
        self.scroll_area.setWidgetResizable(True)  # 위젯 크기 조정 가능
        self.scroll_content = QWidget()  # 스크롤 영역의 콘텐츠를 위한 위젯
        self.scroll_content.setLayout(self.stats_vbox)  # 레이아웃을 콘텐츠 위젯에 설정
        self.scroll_area.setWidget(self.scroll_content)  # 스크롤 영역에 콘텐츠 설정
        # self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 세로 스크롤바 항상 표시
        # self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 가로 스크롤바 비활성화
        self.word_manager = WordManager(self.section_name)
        self.record_manager = Record(self.section_name)
        self.analysis = Analysis(self.word_manager, self.record_manager)
        
        # 폰트 설정
        font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"  # Mac의 경우
        font = font_manager.FontProperties(fname=font_path).get_name()
        rc('font', family=font)
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
        
        # 통계 정보를 표시할 QLabel 추가
        self.states_label_box = QHBoxLayout()
        self.stats_label = QLabel()
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 10px; border-radius: 5px; }")

        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 5), constrained_layout=True)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setFixedHeight(400)  # 캔버스 세로 길이 고정
        # self.canvas.setFixedSize(400, 400)  # 기존 코드 주석 처리

        self.init_stats()
        self.set_state_info()
        self.init_ui()
        self.setup_layout()
        self.refresh_page()
        
    def init_stats(self):
        # 초기화
        # self.states_label_box = QHBoxLayout()
        
        # 두 개의 서브플롯 생성
        # self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 5))
        # self.canvas = FigureCanvas(self.fig)
        
        try:
            daily_counts = self.analysis.get_daily_memorized_word_count()
            print(daily_counts)
            if daily_counts:  # dict가 비어있지 않은 경우
                # dict를 데이터프레임으로 변환
                df = pd.DataFrame.from_dict(daily_counts, orient='index', columns=['count'])
                df.index = pd.to_datetime(df.index)
                
                # 그래프 그리기
                df['count'].plot(kind='bar', ax=self.ax1, color='black')
                self.ax1.set_title('날짜별 암기된 단어 수')
                
                
                # x축 날짜 표시 수정
                dates = df.index
                x_ticks = range(len(dates))
                self.ax1.set_xticks(x_ticks)
                
                # 날짜 레이블 생성
                x_labels = []
                prev_year = prev_month = None
                for date in dates:
                    if prev_year != date.year:
                        x_labels.append(str(date.year))
                        prev_year = date.year
                        prev_month = date.month
                    elif prev_month != date.month:
                        x_labels.append(str(date.month))
                        prev_month = date.month
                    else:
                        x_labels.append('')
                self.ax1.set_xticklabels(x_labels, rotation=45)
            
            cumulative_counts = self.analysis.get_cumulative_daily_memorized_word_count()
            if cumulative_counts:  # dict가 비어있지 않은 경우
                # dict를 데이터프레임으로 변환
                df = pd.DataFrame.from_dict(cumulative_counts, orient='index', columns=['count'])
                df.index = pd.to_datetime(df.index)
                
                # 그래프 그리기 (라인 차트로 변경)
                df['count'].plot(kind='line', ax=self.ax2, color='black')
                self.ax2.set_title('날짜별 누적 암기 단어 수')
                
                
                # 디버깅 정보 추가
                print(f"Cumulative Counts: {cumulative_counts}")  # 데이터 확인
                print(f"DataFrame for Cumulative Counts:\n{df}")  # 데이터프레임 확인
            
            
            # self.stats_label.setText(
            #     f'전체 단어: {total_words}개 '
            #     f'외운 단어: {memorized_words}개 '
            #     f'학습 필요 단어: {remaining_words}개'
            #     f'복습이 필요한 단어: {review_words}개'
            # )
            # self.stats_label.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 10px; border-radius: 5px; font-size: 16px; }")
            
            plt.tight_layout()  # 그래프 간격 자동 조정
            
        except Exception as e:
            print(f"통계 로드 실패: {e}")
    def set_state_info(self):
        while self.states_label_box.count():
            item = self.states_label_box.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # 통계 정보를 QLabel에 표시
        remaining_words = self.analysis.get_number_of_not_memorized_words()
        total_words = len(self.analysis.word_manager.get_word_list())
        memorized_words = self.analysis.get_number_of_memorized_words()
        review_words = self.analysis.get_number_of_review_words()

        self.state_all_container = QWidget()
        self.state_label_all_box = QHBoxLayout()
        self.state_all_lable = QLabel(f"전체: {memorized_words}/{total_words}")
        self.state_all_lable.setStyleSheet(STATE_LABEL_STYLE)
        self.state_label_all_box.addWidget(self.state_all_lable)
        self.state_all_container.setLayout(self.state_label_all_box)
        self.state_all_container.setStyleSheet(STATE_BOX_STYLE)
        self.states_label_box.addWidget(self.state_all_container)

        self.state_review_container = QWidget()
        self.state_label_review_box = QHBoxLayout()
        self.state_review_lable = QLabel(f"복습: {review_words}")
        self.state_review_lable.setStyleSheet(STATE_LABEL_STYLE)
        self.state_label_review_box.addWidget(self.state_review_lable)
        self.state_review_container.setLayout(self.state_label_review_box)
        self.state_review_container.setStyleSheet(STATE_BOX_STYLE)
    
        self.states_label_box.addWidget(self.state_review_container)

    def init_ui(self):
        # 타이틀 설정
        self.title_label = components.set_title_label("Training")
        self.title_label.setStyleSheet(TITLE_STYLE)
        
        # 버튼 설정
        self.buttons = [
            ("Start", lambda: ui.pages.training.set_training_start_page(self.stack, self.section_name)),
            ("Record", lambda: ui.pages.training.set_training_record_page(self.stack, self.section_name)),
            ("Add", lambda: ui.pages.training.set_training_add_page(self.stack, self.section_name)),
            ("Delete", lambda: ui.pages.training.set_training_delete_page(self.stack, self.section_name)),
            ("List", None),
            ("Refresh", self.refresh_page),  # 새로고침 버튼 추가
            ("Back", lambda: events.back_page(self.stack))
        ]
        
        self.widget_list = [self.title_label]
        
        for text, callback in self.buttons:
            btn = components.set_default_btn(text)
            btn.setStyleSheet(BUTTON_STYLE)
            if callback:
                btn.clicked.connect(callback)
            self.widget_list.append(btn)
        
        # Back 버튼 단축키 설정
        self.widget_list[-1].setShortcut(QKeySequence('x'))
        self.widget_list[-2].setShortcut(QKeySequence('Ctrl+R'))
        
        
    def setup_layout(self):
        # 통계 레이아웃 설정
        # self.stats_vbox.addWidget(self.stats_label)  # 통계 라벨 추가
        self.stats_vbox.addLayout(self.states_label_box)
        self.stats_vbox.addWidget(self.canvas)
        
        # 기존 버튼 이아웃 설정
        self.vbox.addStretch(1)
        for widget in self.widget_list:
            if isinstance(widget, QLabel):
                self.vbox.addWidget(widget)
            elif isinstance(widget, QLineEdit):
                hbox = QHBoxLayout()
                hbox.addStretch(1)
                hbox.addWidget(widget)
                hbox.addStretch(1)
                self.vbox.addLayout(hbox)
            elif isinstance(widget, QPushButton):
                widget.setMinimumSize(100, 30)
                hbox = QHBoxLayout()
                hbox.addStretch(1)
                hbox.addWidget(widget)
                hbox.addStretch(1)
                self.vbox.addLayout(hbox)
        self.vbox.addStretch(1)
        
        # 메인 레이아웃에 통계와 버튼 배치
        # self.hbox.addLayout(self.stats_vbox, stretch=2)
        self.hbox.addWidget(self.scroll_area, stretch=2)
        self.hbox.addLayout(self.vbox, stretch=1)
        
        self.widget.setLayout(self.hbox)
        
    def set_page(self):
        self.stack.addWidget(self.widget)
        self.stack.setCurrentIndex(self.stack.count() - 1)

    def refresh_page(self):
        # 기존 그래프 초기화
        self.ax1.clear()
        self.ax2.clear()
        
        # 통계 데이터 새로고침
        self.init_stats()
        
        # 캔버스 업데이트
        self.canvas.draw()

