# KorSenti-Metal 🍎 
### Apple Silicon 기반 한국어 리뷰 감성 분석 (Educational Project)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Metal-orange)
![License](https://img.shields.io/badge/License-MIT_(Educational)-green)

**KorSenti-Metal**은 네이버 쇼핑 리뷰와 스팀(Steam) 리뷰 데이터를 활용하여 한국어 감성 분석 모델(LSTM)을 학습하고 평가하는 프로젝트입니다.  
특히 **macOS Apple Silicon (M1/M2/M3)** 환경에서 `tensorflow-metal`을 활용한 GPU 가속 학습을 실습할 수 있도록 구성되었습니다.

---

## 📂 프로젝트 구조

```
KorSenti-Metal/
├── data/
│   ├── raw/           # 원본 데이터 (네이버 쇼핑, 스팀 리뷰)
│   └── sample/        # 테스트용 샘플 데이터 (각 100건)
├── src/
│   ├── data_merge.py       # 데이터 병합 및 분할
│   ├── preprocessing.py    # KoNLPy(Okt) 전처리 및 토큰화
│   ├── model_fit.py        # LSTM 모델 학습
│   └── predict_sentiment.py # 감성 예측 실행
├── scripts/           # 유틸리티 스크립트
├── docs/              # 프로젝트 문서 (PRD, Tasks)
└── main.py            # 전체 파이프라인 실행기
```

## 🚀 시작하기 (Getting Started)

### 1. 환경 설정 (macOS Apple Silicon 기준)

Apple Silicon Mac에서는 `tensorflow-deps`, `tensorflow-macos`, `tensorflow-metal`을 순서대로 설치해야 합니다.

```bash
# 1. Conda 환경 생성 (권장)
conda create -n senti_metal python=3.9
conda activate senti_metal

# 2. Apple TensorFlow 의존성 설치
conda install -c apple tensorflow-deps

# 3. 패키지 설치
pip install tensorflow-macos tensorflow-metal
pip install pandas numpy scikit-learn matplotlib konlpy
```

### 2. JDK 설치 (KoNLPy 필수)
KoNLPy의 `Okt` 형태소 분석기를 사용하려면 Java(JDK)가 필요합니다.
```bash
brew install openjdk@11
```

### 3. 실행 방법 (Usage)

샘플 데이터를 이용하여 전체 파이프라인을 테스트할 수 있습니다.

```bash
# 파이프라인 전체 실행
python src/main.py
```
> **참고**: `main.py`는 데이터 병합 -> 전처리 -> 학습 -> 예측을 순차적으로 실행합니다.

---

## 📊 분석 대상 (Benchmarks)
- **네이버 쇼핑 리뷰**: 상품 평점 1,2점(부정) vs 4,5점(긍정)
- **스팀(Steam) 리뷰**: 게임 리뷰 텍스트

## 📝 라이선스
이 프로젝트는 [MIT License](LICENSE) 하에 배포되며, **교육 및 실습 목적**으로 제작되었습니다.
