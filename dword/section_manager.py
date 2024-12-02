import csv
import os
import pandas as pd
from datetime import datetime
import logging
from typing import List
from dword.path import DATA_PATH, resource_path

class SectionManager:
    def __init__(self):
        # self.path = resource_path("data_test")
        self.path = DATA_PATH
        self.init()
    
    # 폴더가 존재하는지 확인
    def init(self):
        if self.path and not os.path.exists(self.path):
            os.makedirs(self.path)
            logging.info(f"{self.path} 경로가 생성되었습니다.")
        else:
            logging.info(f"{self.path} 경로 존재")
    
    def add_section(self, folder_name: str):
        # 폴더명이 될 수 없는 문자열인지 확인
        if not folder_name.isidentifier():
            logging.error(f"{folder_name}는 유효한 폴더명이 아닙니다.")
            return  # 에러 발생 시 함수 종료

        # 존재하지 않는 폴더 추가
        section_list = self.get_section_list()
        if folder_name not in section_list:
            os.makedirs(os.path.join(self.path, folder_name))
            logging.info(f"{folder_name} 폴더가 {self.path}에 추가되었습니다.")
        else:
            logging.info(f"{folder_name} 폴더는 이미 존재합니다.")
    
    def get_section_list(self):
        # self.path 경로에 존재하는 모든 폴더명을 반환
        return [name for name in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, name))]


