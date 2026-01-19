import json
import re
import pandas as pd
import numpy as np
import h5py
import logging
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import multiprocessing
import os
import tensorflow as tf

# TensorFlow 로그 억제 (경고 억제)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')

# M1 Mac 환경 호환을 위한 멀티프로세싱 설정
multiprocessing.set_start_method('spawn', force=True)

# ====== 1. 설정 파일 로드 =====
def load_config(config_path='src/config.json'):
    """ JSON 설정 파일 로드 """
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

config = load_config()

# ====== 2. 경로 설정 ======
RAW_DATA_PATH = config['paths']['raw_data']
PROCESSED_DATA_PATH = config['paths']['processed_data']
LOGS_DATA_PATH = config['paths']['logs']
MODEL_DATA_PATH = config['paths']['model']

# ====== 3. 로깅 설정 ======
logging.basicConfig(
    filename=f"{LOGS_DATA_PATH}preprocessing.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("==== 데이터 전처리 시작 ====")


# ====== 4. 불용어 로드 ======
def load_stopwords():
    """ 불용어(stopwords)를 로드하여 집합(set)으로 반환 """
    stopwords_path = os.path.join(RAW_DATA_PATH, config['files']['stopwords'])
    with open(stopwords_path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f.readlines())

# ====== 5. 데이터 로드 ======
def load_data():
    """ 전처리를 위한 학습 및 테스트 데이터 로드 """
    train_data = pd.read_csv(f"{PROCESSED_DATA_PATH}train_data.csv", encoding='utf-8', engine='pyarrow')
    test_data = pd.read_csv(f"{PROCESSED_DATA_PATH}test_data.csv", encoding='utf-8', engine='pyarrow')

    logging.info(f"훈련 데이터 {train_data.shape[0]}개 로드 완료.")
    logging.info(f"테스트 데이터 {test_data.shape[0]}개 로드 완료.")
    return train_data, test_data

# ====== 6. 텍스트 전처리 함수 ======
def preprocess_text(text, stopwords):
    """
    텍스트 전처리:
    - 특수 문자 제거
    - 형태소 분석 및 불용어 제거
    """
    okt = Okt()
    text = re.sub(r"[^가-힣0-9\s]", "", str(text))
    tokens = okt.morphs(text, stem=True)
    return [w for w in tokens if w not in stopwords]

def process_text_batch(data_chunk):
    """ 병렬 처리를 위한 함수 (각 프로세스 내에서 개별 호출) """
    stopwords = load_stopwords()  # 각 프로세스에서 불용어 로드
    return [preprocess_text(text, stopwords) for text in tqdm(data_chunk, desc="Processing")]

def parallel_process_texts(data):
    """ 병렬 처리를 이용한 텍스트 전처리 """
    cpu_count = max(1, multiprocessing.cpu_count() - 2)
    chunk_size = len(data) // cpu_count + 1

    logging.info(f"병렬 처리 CPU 개수: {cpu_count}개")

    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        data_chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        results = list(executor.map(process_text_batch, data_chunks))
    
    logging.info("텍스트 전처리 완료.")
    return [item for sublist in results for item in sublist]

if __name__ == "__main__":
    train_data, test_data = load_data()
    train_data['document'] = parallel_process_texts(train_data['document'].dropna().tolist())
    test_data['document'] = parallel_process_texts(test_data['document'].dropna().tolist())

    # ====== 7. 토큰화 및 패딩 ======
    def tokenize_and_pad(train_texts, test_texts, max_len=30):
        """ 텍스트를 토큰화하고 패딩 처리하여 시퀀스를 생성 """
        tokenizer = Tokenizer(oov_token="<OOV>")
        tokenizer.fit_on_texts(train_texts)

        logging.info(f"총 단어 개수: {len(tokenizer.word_index)}개")

        X_train = pad_sequences(tokenizer.texts_to_sequences(train_texts), maxlen=max_len, padding='post')
        X_test = pad_sequences(tokenizer.texts_to_sequences(test_texts), maxlen=max_len, padding='post')

        return X_train, X_test, tokenizer

    X_train, X_test, tokenizer = tokenize_and_pad(train_data['document'], test_data['document'])

    # ====== 8. 데이터 저장 ======
    def save_data(X_train, X_test, y_train, y_test, tokenizer):
        """ 전처리된 데이터를 HDF5 및 JSON 파일로 저장 """
        with h5py.File(f"{PROCESSED_DATA_PATH}data.h5", 'w') as f:
            f.create_dataset('X_train', data=X_train)
            f.create_dataset('X_test', data=X_test)
            f.create_dataset('y_train', data=np.array(y_train))
            f.create_dataset('y_test', data=np.array(y_test))
        logging.info("HDF5 데이터 저장 완료")

        with open(f"{MODEL_DATA_PATH}wordIndex.json", "w", encoding="utf-8") as f:
            json.dump(tokenizer.word_index, f, ensure_ascii=False)
        logging.info("단어 인덱스 저장 완료")

    save_data(X_train, X_test, train_data['label'], test_data['label'], tokenizer)

    # ====== 9. 작업 완료 로그 ======
    logging.info("==== 데이터 전처리 완료 및 저장 완료 ====")
    print("데이터 전처리 및 저장이 완료되었습니다.")