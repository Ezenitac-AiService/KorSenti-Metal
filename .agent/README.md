# Antigravity IDE Configuration

**Antigravity Agent**의 모든 설정과 지침은 이 디렉토리(`/.agent`)를 유일한 **Source of Truth**로 사용합니다.

## 📁 Directory Structure

### 1. `rules/` (Core Guidelines)
에이전트의 행동 원칙과 코딩 표준을 정의합니다. **Dynamic Context Loading**에 의해 상황에 맞게 로드됩니다.
- **`core-principles.md`**: [Entry Point] 에이전트 페르소나, 핵심 락(Latch), 워크플로우 트리거. (가장 먼저 읽어야 함)
- **`coding-standards.md`**: 기술 스택, 네이밍 규칙, Definition of Done (DoD).
- **`agent-protocols.md`**: 스킬 사용법, 에러 복구 전략, 커뮤니케이션 규칙.

### 2. `workflows/` (Process Definitions)
반복적인 작업을 수행하기 위한 단계별 가이드입니다. (구 `.github/prompts/*.prompt.md` 대체)
- `/create-prd`: 요구사항 분석 및 PRD 생성.
- `/generate-tasks`: PRD 기반 작업 분해.
- `/execute-task`: 개별 Task 구현 및 검증.
- `/run-epic`: Epic 단위 배치 실행.
- `/scaffold-feature`: 통합 워크플로우.

### 3. `skills/` (Capability Modules)
에이전트가 활용할 수 있는 고급 도구 모음입니다.
- **`git-manager`**: 안전한 Git 조작.
- **`task-tracker`**: 작업 상태 추적.
- **`code-verifier`**: 품질 검증 자동화.

## 🚀 Usage (For Agent)
작업을 시작할 때 반드시 `rules/core-principles.md`를 먼저 로드하여 정체성과 원칙을 확인하십시오.
외부 의존성(`.github` 등)은 레거시이며, 이 폴더의 내용이 우선합니다.
