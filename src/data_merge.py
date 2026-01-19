import pandas as pd
import json
import logging
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import multiprocessing

# M1 Mac 호환을 위한 multiprocessing 설정
multiprocessing.set_start_method('spawn', force=True)

# ====== 1. 설정 파일 로드 ======
def load_config(config_path='src/config.json'):
    """ JSON 설정 파일 로드 """
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

config = load_config()

# ====== 2. 경로 설정 ======
RAW_DATA_PATH = config['paths']['raw_data']
PROCESSED_DATA_PATH = config['paths']['processed_data']
LOGS_DATA_PATH = config['paths']['logs']

# ====== 3. 로깅 설정 ======
logging.basicConfig(
    filename=f"{LOGS_DATA_PATH}data_merge.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ====== 4. 데이터 로드 및 전처리 함수 ======
def read_file(file_info):
    """
    단일 CSV 파일을 읽고, 전처리를 수행하는 함수

    Args:
        file_info (dict): 파일 정보 (이름, 구분자, 컬럼 등)

    Returns:
        DataFrame: 전처리된 데이터 프레임
    """
    try:
        file_path = f"{RAW_DATA_PATH}{file_info['name']}"
        df = pd.read_csv(
            file_path,
            sep=file_info['sep'],
            header=file_info['header'],
            names=file_info['cols'],
            encoding=file_info.get('encoding', 'utf-8'),
            engine='pyarrow'  # M1 Mac 환경에서 pyarrow 사용
        )
        
        logging.info(f"{file_info['name']} 로드 완료")
        logging.info(f"컬럼명: {df.columns.tolist()}")

        # 필요한 컬럼만 선택
        df = df[file_info['use_cols']]
        logging.info(f"로드된 데이터 개수: {len(df)}")

        # 라벨 매핑 적용
        if 'label_map' in file_info:
            logging.info(f"라벨 매핑 전 고유값: {df['label'].unique()}")
            df['label'] = df['label'].astype(str).map(file_info['label_map'])
            logging.info(f"라벨 매핑 후 고유값: {df['label'].unique()}")

        df['source'] = file_info['source']

        # 결측치 및 중복 제거
        if file_info.get('drop_na', False):
            df.dropna(inplace=True)
            logging.info("결측치 제거 완료")

        if file_info.get('drop_duplicates', False):
            df.drop_duplicates(inplace=True)
            logging.info("중복 제거 완료")

        logging.info(f"{file_info['name']} 처리 완료 - 총 {len(df)}개")
        return df

    except Exception as e:
        logging.error(f"{file_info['name']} 로드 실패: {e}")
        return pd.DataFrame()

# ====== 5. 파일 목록 로드 및 데이터 병합 ======
def merge_data():
    """ 모든 데이터를 로드 및 병합 """
    file_list_path = f"{RAW_DATA_PATH}file_list.json"
    with open(file_list_path, 'r') as f:
        files = json.load(f)

    dataframes = [read_file(file) for file in files]
    final_df = pd.concat(dataframes, ignore_index=True)
    
    logging.info(f"최종 병합 데이터 크기: {len(final_df)}개")
    return final_df

final_df = merge_data()

# ====== 6. 데이터 분포 시각화 ======
def visualize_label_distribution(df):
    """
    데이터의 긍정/부정 레이블 분포를 시각화하는 함수

    Args:
        df (DataFrame): 병합된 데이터 프레임
    """
    plt.rc('font', family="AppleGothic")  # M1 환경에서 한글 폰트 적용
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(6, 4))
    df['label'].value_counts().plot(kind='bar')
    plt.title('긍정/부정 데이터 분포')
    plt.savefig(f"{LOGS_DATA_PATH}label_distribution.png")
    logging.info("라벨 분포 시각화 완료 및 저장")

visualize_label_distribution(final_df)

# ====== 7. 데이터 분할 함수 ======
def split_data(df, test_size=0.25, random_state=42):
    """
    데이터셋을 훈련 및 테스트 세트로 분할하는 함수

    Args:
        df (DataFrame): 병합된 데이터
        test_size (float): 테스트 세트 비율 (기본값 0.25)
        random_state (int): 난수 시드 고정

    Returns:
        tuple: (훈련 데이터, 테스트 데이터)
    """
    positive = df[df['label'] == 1]
    negative = df[df['label'] == 0]
    
    pos_train, pos_test = train_test_split(positive, test_size=test_size, random_state=random_state)
    neg_train, neg_test = train_test_split(negative, test_size=test_size, random_state=random_state)
    
    train_df = pd.concat([pos_train, neg_train]).sample(frac=1, random_state=random_state).reset_index(drop=True)
    test_df = pd.concat([pos_test, neg_test]).sample(frac=1, random_state=random_state).reset_index(drop=True)
    
    logging.info(f"훈련 데이터 크기: {len(train_df)}개, 테스트 데이터 크기: {len(test_df)}개")
    return train_df, test_df

train_df, test_df = split_data(final_df)

# ====== 8. 데이터 저장 ======
def save_data(train_df, test_df):
    """
    분할된 데이터를 CSV 파일로 저장

    Args:
        train_df (DataFrame): 훈련 데이터 프레임
        test_df (DataFrame): 테스트 데이터 프레임
    """
    train_path = f"{PROCESSED_DATA_PATH}train_data.csv"
    test_path = f"{PROCESSED_DATA_PATH}test_data.csv"
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    logging.info("train_data.csv 및 test_data.csv 저장 완료")

save_data(train_df, test_df)

logging.info("데이터 처리 및 저장 완료")
print("데이터 병합 및 저장이 완료되었습니다.")