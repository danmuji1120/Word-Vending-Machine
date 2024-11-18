import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from .analysis import Analysis
class Graph:
    def __init__(self):
        # 한글 폰트 설정
        font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"  # Mac의 경우
        font = font_manager.FontProperties(fname=font_path).get_name()
        rc('font', family=font)
        plt.rcParams['axes.unicode_minus'] = False
        self.analysis = Analysis()

    def show_memorized_daily_graph(self, df: pd.DataFrame):
        daily_counts = self.analysis.get_memorized_count_by_day(df)
        if daily_counts.empty:
            return
            
        plt.figure(figsize=(12, 6))
        daily_counts.plot(kind='bar', color='skyblue')
        plt.title("누적 암기 단어 수 (일별)")
        plt.xlabel("날짜")
        plt.ylabel("암기된 단어 수")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def show_memorized_monthly_graph(self, df: pd.DataFrame):
        monthly_counts = self.analysis.get_memorized_count_by_month(df)
        if monthly_counts.empty:
            return
            
        plt.figure(figsize=(12, 6))
        monthly_counts.plot(kind='bar', color='green')
        plt.title("누적 암기 단어 수 (월별)")
        plt.xlabel("월")
        plt.ylabel("암기된 단어 수")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def show_memorized_yearly_graph(self, df: pd.DataFrame):
        yearly_counts = self.analysis.get_memorized_count_by_year(df)
        if yearly_counts.empty:
            return
            
        plt.figure(figsize=(12, 6))
        yearly_counts.plot(kind='bar', color='orange')
        plt.title("누적 암기 단어 수 (연도별)")
        plt.xlabel("연도")
        plt.ylabel("암기된 단어 수")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()