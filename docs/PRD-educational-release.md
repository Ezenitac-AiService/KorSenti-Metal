# Product Requirements Document (PRD): KorSenti-Metal (교육용 배포)

## 1. 프로젝트 개요
**프로젝트 명**: KorSenti-Metal (Apple Silicon 기반 한국어 리뷰 감성 분석)
**목표**: 네이버 쇼핑 리뷰와 스팀(Steam) 리뷰 데이터를 활용한 LSTM 감성 분석 모델 프로젝트를 정리하여, macOS(Apple Silicon/Metal) 환경에서 최적화된 교육용 오픈소스 프로젝트로 GitHub에 배포할 수 있도록 준비한다.
**대상 독자**: 한국어 텍스트 마이닝, LSTM 모델링, 그리고 Apple Silicon 기반 딥러닝 환경 구축을 실습하고자 하는 학생 및 연구자.

## 2. 핵심 요구사항

### 2.1. 데이터 및 산출물 아카이빙 (Archive & Cleanup)
- **보존 대상**:
  - `data/raw/`: 학습용 원시 데이터 (네이버 쇼핑, 스팀 리뷰 데이터셋).
  - `data/sample/` (신규 생성 필요): 사용자가 즉시 테스트해볼 수 있는 소량의 샘플 데이터 (각 데이터셋 별 100건 내외).
- **아카이브 대상**:
  - `data/processed/`: 전처리 완료된 데이터 (HDF5, Tokenizer JSON 등).
  - `data/model/`: 학습된 LSTM 모델 가중치 파일.
  - `logs/`: 실행 로그.
  - 기타 임시 파일.
- **동작**:
  - `archive_artifacts/` 폴더를 생성하여 위 '아카이브 대상'을 이동.
  - 깃헙 업로드 시 제외되도록 `.gitignore` 점검 및 업데이트 (단, `data/raw`와 `data/sample`은 포함).

### 2.2. 문서화 (Documentation)
- **README.md 작성**:
  - **프로젝트 소개**: 네이버 쇼핑/스팀 리뷰 데이터를 이용한 한국어 감성 분석 (LSTM).
  - **기술 스택 뱃지**: Python, TensorFlow-Metal, KoNLPy(Okt), Pandas, MIT License.
  - **설치 및 실행 가이드**:
    - macOS Apple Silicon (M1/M2/M3) 환경에서의 `tensorflow-macos`, `tensorflow-metal` 설치 방법.
    - KoNLPy 및 JDK 설정 가이드.
  - **폴더 구조 설명**: `src` (전처리, 학습, 예측), `data` 등 디렉토리 역할 설명.
- **License**:
  - MIT License 적용.
  - "이 프로젝트는 교육 목적으로 제작되었습니다" (This project is designed for educational purposes) 문구 포함.

### 2.3. 배포 준비
- **Code Clean-up**: 불필요한 주석 제거, 코드 가독성 개선.
- **Requirements**: `requirements.txt`가 macOS Metal 환경(`tensorflow-metal`)에 맞는지 최종 확인.

## 3. 기술 스택 및 환경
- **OS**: macOS (Apple Silicon optimized)
- **Language**: Python 3.8+
- **Key Libraries**:
  - `tensorflow-macos`, `tensorflow-metal` (GPU Acceleration)
  - `konlpy` (한국어 형태소 분석 - Okt)
  - `pandas`, `numpy`, `scikit-learn`
- **Model**: LSTM (Long Short-Term Memory) based Sentiment Classifier

## 4. 성공 기준 (Success Criteria)
1. GitHub 저장소에 불필요한 대용량 파일(processed data, model weights)이 올라가지 않도록 정리되었는가?
2. `data/sample`을 통해 사용자가 별도 다운로드 없이도 `main.py`를 돌려볼 수 있는가?
3. README를 통해 Mac 사용자가 시행착오 없이 환경을 구축할 수 있는가?
4. 프로젝트의 목적(교육용, 쇼핑/스팀 리뷰 분석)이 명확히 전달되는가?
