import os
import re
import json
import tensorflow as tf
from konlpy.tag import Okt
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import logging

# TensorFlow 로그 억제
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')

# ====== 1. 설정 파일 로드 ======
def load_config(config_path='src/config.json'):
    """ JSON 설정 파일 로드 """
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

config = load_config()

# ====== 2. 경로 설정 ======
PROCESSED_DATA_PATH = config['paths']['processed_data']
MODEL_DATA_PATH = config['paths']['model']
LOGS_DATA_PATH = config['paths']['logs']
RAW_DATA_PATH = config['paths']['raw_data']

# ====== 3. 로깅 설정 ======
logging.basicConfig(
    filename=os.path.join(LOGS_DATA_PATH, 'inference.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ====== 4. M1 Mac GPU 설정 ======
try:
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_virtual_device_configuration(
                gpu,
                [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=4096)]
            )
        logging.info("[INFO] GPU가 감지되었습니다. Metal backend를 사용합니다.")
    else:
        logging.info("[INFO] GPU를 찾을 수 없습니다. CPU로 진행합니다.")
except Exception as e:
    logging.warning(f"[WARNING] GPU 설정 중 오류 발생: {e}")
    logging.info("[INFO] CPU 모드로 진행합니다.")

# ====== 5. 불용어 로드 ======
def load_stopwords(filepath=os.path.join(RAW_DATA_PATH, "stopwords.txt")):
    with open(filepath, "r", encoding="utf-8") as f:
        stopwords = set(line.strip() for line in f.readlines())
    return stopwords

stopwords = load_stopwords()
logging.info("[INFO] 불용어 로드 완료.")

# ====== 6. 모델 및 단어 인덱스 로드 ======
model_path = os.path.join(MODEL_DATA_PATH, "best_model.h5")
word_index_path = os.path.join(MODEL_DATA_PATH, "wordIndex.json")

loaded_model = load_model(model_path)
with open(word_index_path, "r", encoding="utf-8") as f:
    word_index = json.load(f)

max_len = 30
logging.info("[INFO] 모델 및 단어 인덱스 로드 완료.")

# ====== 7. 텍스트 전처리 함수 ======
okt = None

def get_okt():
    """ Okt 객체를 전역 캐싱 """
    global okt
    if okt is None:
        okt = Okt()
    return okt

def preprocess_text(sentence):
    """ 텍스트 전처리 (특수문자 제거, 형태소 분석, 불용어 제거) """
    sentence = re.sub(r"[^가-힣0-9\s]", "", sentence).strip()
    okt = get_okt()
    tokens = okt.morphs(sentence, stem=True)
    tokens = [w for w in tokens if w not in stopwords]
    return tokens

# ====== 8. 감성 분석 함수 ======
def predict_sentiment(sentence):
    """ 감성 분석 수행 및 결과 반환 """
    tokens = preprocess_text(sentence)
    encoded = [word_index.get(w, 2) for w in tokens]  # OOV 토큰 2 사용
    pad_seq = pad_sequences([encoded], maxlen=max_len, padding='post')

    score = float(loaded_model.predict(pad_seq, verbose=0))
    result = f"[긍정] {score*100:.2f}% 확률로 긍정 리뷰입니다." if score > 0.5 else f"[부정] {(1-score)*100:.2f}% 확률로 부정 리뷰입니다."

    logging.info(f"[INFO] 입력: {sentence} | 결과: {result}")
    return result

# ====== 9. 인터랙티브 모드 ======
def interactive_mode():
    print("\n[INFO] 감성 분석을 시작합니다. (종료하려면 'exit' 입력)")
    while True:
        user_input = input("입력 문장: ")
        if user_input.lower() == 'exit':
            print("[INFO] 감성 분석을 종료합니다.")
            break
        result = predict_sentiment(user_input)
        print(result)

# ====== 10. 샘플 테스트 실행 ======
if __name__ == "__main__":
    test_sentences = [
        "이 영화 정말 재밌어요!",
        "완전 최악이에요.",
        "배우 연기가 너무 어색하고 스토리가 별로였어요.",
        "사운드트랙이 정말 감동적이었어요.",
        "친절한 서비스에 기분이 너무 좋아졌어요.",
        "이 제품은 기대 이상이에요. 품질이 정말 좋습니다.",
        "오늘 날씨가 정말 좋네요. 기분도 덩달아 좋아져요!",
        "음식이 너무 맛있어요. 추천할 만합니다!",
        "친구들과 즐거운 시간을 보냈어요. 최고의 하루였습니다!",
        "책 내용이 매우 유익하고 도움이 많이 되었어요.",
        "여행이 정말 만족스러웠어요. 다음에 또 오고 싶어요.",
        "선물이 너무 마음에 들어요. 고맙습니다!",
        "배송이 빠르고 포장도 깔끔해요. 만족합니다!",
        "오늘 점심으로 국수를 먹었어요.",
        "날씨가 흐려서 그런지 기분이 애매하네요.",
        "가게 인테리어는 깔끔했지만 특별할 건 없었어요.",
        "이 책은 정보가 많긴 한데 좀 지루해요.",
        "여행지에 대한 기대가 크진 않지만 가볼 만은 해요.",
        "새 핸드폰이 도착했어요. 디자인은 평범하네요.",
        "지금 버스를 기다리고 있어요. 조금 늦을 것 같아요.",
        "회의가 길었지만 중요한 내용은 없었어요.",
        "새로운 운동화를 샀어요. 특별히 편하진 않아요.",
        "영화의 줄거리는 무난하지만 특별한 점은 없어요.",
        "서비스가 정말 최악이었어요. 다시는 이용하지 않을 거예요.",
        "제품이 금방 고장 났어요. 돈이 아깝습니다.",
        "음식이 너무 짜고 차갑더라고요. 실망했어요.",
        "영화가 지루해서 중간에 나왔어요. 시간 낭비였어요.",
        "배송이 늦고 상태도 별로였어요. 추천하지 않아요.",
        "기대가 너무 컸던 탓인지 실망감이 크네요.",
        "여행 내내 불편했어요. 다신 안 가고 싶어요.",
        "이 앱은 너무 자주 오류가 나서 불편해요.",
        "고객 서비스 응대가 너무 불친절했어요.",
        "이 옷은 사진과 너무 달라서 실망스러워요."
    ]

    print("\n[INFO] 샘플 문장에 대한 감성 분석 테스트:")
    for sent in test_sentences:
        print(f"입력: {sent}")
        print(predict_sentiment(sent))
        print("-" * 30)

    #interactive_mode()