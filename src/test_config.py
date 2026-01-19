import pandas as pd
import json
import logging

# 설정 파일 로드
with open('src/config.json', 'r') as config_file:
    config = json.load(config_file)

# 데이터 경로 설정
RAW_DATA_PATH = config['paths']['raw_data']
PROCESSED_DATA_PATH = config['paths']['processed_data']
LOGS_DATA_PATH = config['paths']['logs']

import os
print(os.path.exists(RAW_DATA_PATH + 'naver_shopping.txt'))

try:
    df = pd.read_csv(RAW_DATA_PATH + 'naver_shopping.txt', sep='\t', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(RAW_DATA_PATH + 'naver_shopping.txt', sep='\t', encoding='euc-kr')
    
with open(RAW_DATA_PATH + 'naver_shopping.txt', 'r', encoding='utf-8') as f:
    print(f.readline())  # 첫 줄의 구분자를 확인


df = pd.read_csv(RAW_DATA_PATH + 'naver_shopping.txt', sep='\t', header=None)
print(df.head())

df = pd.read_csv(RAW_DATA_PATH + 'naver_shopping.txt', sep='\t', encoding='utf-8')
print(df.isnull().sum())

with open(RAW_DATA_PATH + 'naver_shopping.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    print(len(content))
