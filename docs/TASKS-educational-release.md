# Tasks: KorSenti-Metal 교육용 배포 준비

## Epic 1: Project Organization (프로젝트 정리 및 아카이빙)
- **Goal**: 배포에 불필요한 파일들을 정리하고, 사용자 테스트를 위한 샘플 데이터를 확보한다.
- **Tasks**:
  - [ ] **TASK-01-01**: `archive_artifacts/` 디렉토리 생성 및 데이터 이동 스크립트(`scripts/archive_data.sh`) 작성 및 실행. (이동 대상: `data/processed`, `data/model`, `logs`)
  - [ ] **TASK-01-02**: `data/raw` 데이터를 기반으로 각 데이터셋 별 100건의 샘플 데이터를 추출하여 `data/sample/`에 저장하는 파이썬 스크립트(`scripts/create_sample.py`) 작성 및 실행.
  - [ ] **TASK-01-03**: `.gitignore` 파일을 검토하고 업데이트하여 `archive_artifacts/` 및 시스템 파일(.DS_Store 등)이 커밋되지 않도록 설정. 단, `data/raw`와 `data/sample`은 포함.

## Epic 2: Documentation (문서화)
- **Goal**: 사용자가 프로젝트를 쉽게 이해하고 실행할 수 있도록 문서를 작성한다.
- **Tasks**:
  - [ ] **TASK-02-01**: `LICENSE` 파일 생성. (MIT License 기반, "Educational Purpose" 명시 문구 추가)
  - [ ] **TASK-02-02**: `README.md` 작성. (프로젝트 소개, 기술 스택 뱃지, macOS Metal 환경 설정 가이드, 실행 방법 포함)
  - [ ] **TASK-02-03**: 코드 내 불필요한 주석 제거 및 docstring 보완 (`src/*.py` 대상).

## Epic 3: Final Verification (최종 검증)
- **Goal**: 배포 전 패키지 의존성과 실행 가능성을 검증한다.
- **Tasks**:
  - [ ] **TASK-03-01**: `requirements.txt` 최신화 및 검증 (tensorflow-macos, tensorflow-metal 버전 명시 확인).
  - [ ] **TASK-03-02**: 로컬 환경에서 `data/sample` 데이터를 이용해 `main.py` 파이프라인이 에러 없이 완주되는지 테스트.
