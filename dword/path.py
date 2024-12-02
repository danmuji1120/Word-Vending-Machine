import sys
import os
def resource_path(relative_path):
    """PyInstaller로 패키징된 환경에서 실행 파일 기준으로 경로를 반환"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller로 패키징된 경우
        base_path = sys._MEIPASS
    else:
        # 개발 환경에서 실행 중인 경우
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


DATA_PATH = resource_path("data")