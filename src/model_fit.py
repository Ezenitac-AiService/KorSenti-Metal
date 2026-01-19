import os
import json
import numpy as np
import h5py
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, LSTM, GRU, Dense, Dropout, Bidirectional, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import matplotlib.pyplot as plt
import logging

# TensorFlow 로그 억제 설정
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

# ====== 3. 로깅 설정 ======
logging.basicConfig(
    filename=f"{LOGS_DATA_PATH}training.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("[INFO] 모델 학습을 시작합니다.")

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

# ====== 5. 데이터 로드 ======
logging.info("[INFO] 데이터 로드 중...")
data_file = os.path.join(PROCESSED_DATA_PATH, 'data.h5')
word_index_file = os.path.join(MODEL_DATA_PATH, 'wordIndex.json')

with h5py.File(data_file, 'r') as f:
    X_train = np.array(f['X_train'])
    y_train = np.array(f['y_train'])
    X_test = np.array(f['X_test'])
    y_test = np.array(f['y_test'])

with open(word_index_file, "r", encoding="utf-8") as f:
    word_index = json.load(f)

vocab_size = len(word_index) + 1
max_len = X_train.shape[1]

logging.info(f"[INFO] 데이터 로드 완료: 훈련 샘플 {X_train.shape[0]}개, 테스트 샘플 {X_test.shape[0]}개")

# ====== 6. 모델 구성 ======
def build_model(vocab_size, embedding_dim=200, max_len=30):
    """ 모델 생성 함수 """
    model = Sequential([
        Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len),
        Bidirectional(LSTM(128, return_sequences=True)),
        Dropout(0.4),
        BatchNormalization(),
        GRU(128),
        Dropout(0.4),
        BatchNormalization(),
        Dense(1, activation='sigmoid')
    ])
    return model

model = build_model(vocab_size, max_len=max_len)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
logging.info("[INFO] 모델 컴파일 완료.")

# ====== 7. 콜백 설정 ======
callbacks = [
    EarlyStopping(monitor='val_loss', patience=5, verbose=1, mode='min'),
    ModelCheckpoint(os.path.join(MODEL_DATA_PATH, 'best_model.h5'),
                    monitor='val_accuracy', save_best_only=True, mode='max', verbose=1),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, verbose=1)
]
logging.info("[INFO] 콜백 설정 완료.")

# ====== 8. 모델 학습 ======
logging.info("[INFO] 모델 학습 시작...")
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=128,  # M1 Mac의 메모리 제한을 고려하여 감소
    validation_split=0.2,
    callbacks=callbacks
)

# ====== 9. 최적 모델 평가 ======
logging.info("[INFO] 모델 평가 중...")
best_model_path = os.path.join(MODEL_DATA_PATH, 'best_model.h5')
best_model = load_model(best_model_path)
loss, acc = best_model.evaluate(X_test, y_test, verbose=0)
logging.info(f"[INFO] 테스트 정확도: {acc:.4f}")

# ====== 10. 학습 결과 시각화 ======
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.title("Training vs Validation Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plot_path = os.path.join(LOGS_DATA_PATH, 'training_plot.png')
plt.savefig(plot_path)

logging.info("[INFO] 학습 과정 완료 및 모델 저장 완료.")
print("모델 학습 및 평가 완료.")