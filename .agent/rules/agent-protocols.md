---
description: "Agent capabilities, error recovery protocols, and collaboration rules"
version: 1.0.0
---

# 에이전트 프로토콜 및 스킬 가이드 (Agent Protocols)

> [!NOTE]
> 이 파일은 에이전트의 행동 방식, 도구 사용, 에러 처리를 정의합니다.
> `rules/core-principles.md`의 "Dynamic Context Loading"에 의해 호출됩니다.

## 1. 에이전트 스킬 (Skills) 활용 가이드

복잡한 터미널 명령 대신 다음 스킬을 사용하여 안전하게 작업을 수행하십시오.

| 스킬 (Skill) | 자연어 트리거 예시 | 기능 |
|:---:|:---|:---|
| `git-manager` | "안전하게 커밋해", "변경사항 저장" | Conventional Commit 자동 생성, Diff 분석, Atomic Push |
| `task-tracker` | "Task-01 완료했어", "진행률 알려줘" | TASKS 파일 안전 파싱, 체크박스 업데이트, 진행률 자동 계산 |
| `code-verifier` | "코드 검증해", "DoD 만족 확인" | 프로젝트 설정 기반 린트/테스트 실행, 에러 로그 분석 |

### 사용 예시 (Scenario)
- **커밋**: `git add .` (X) -> `git-manager` 호출 (O)
- **작업 완료**: 수동 파일 수정 (X) -> `task-tracker` 호출 (O)
- **검증**: "테스트 통과함" 발언 (X) -> `code-verifier` 호출 (O)

## 2. 자율 수정 및 복구 (Self-Correction Protocol)
> "실패는 정보입니다." - Replit Agent Philosophy

에러 발생 시 무의미한 재시도(Blind Retry)를 금지합니다.
1. **Diagnosis (진단)**: 에러 로그의 마지막 20줄을 분석하고 원인을 추론하십시오.
2. **Strategy (전략 수정)**: 기존 접근 방식의 결함을 인정하고 새로운 가설을 세우십시오.
3. **Execution (수정 실행)**: 수정된 코드를 적용하고 반드시 검증(`code-verifier`)하십시오.

## 3. 결과 중심 계획 (Goal-Oriented Planning)
> "Start with the End in Mind." - Lovable.dev Pattern

모든 Task는 **성공 기준(Success Criteria)**이 명확해야 합니다.
- **Before**: "로그인 페이지 만들기" (X)
- **After**: "로그인 성공 시 `/dashboard`로 리다이렉트되고, 실패 시 에러 메시지가 표시되어야 함" (O)

## 4. 장기 실행 세션 관리 (Long-Running Sessions)
대규모 작업이나 긴 대화 세션에서는 다음 원칙을 따르십시오.

1. **Context Refresh**: 대화가 10턴 이상 지속되면, 이전 구현 세부 사항은 잊고 `docs/PRD-*.md`와 `docs/TASKS-*.md`를 기준으로 다시 생각하십시오.
2. **State Persistence**: Epic 완료 시마다 `session_state.json`에 상태를 저장한다고 가정하고 행동하십시오.

## 5. 언어 및 소통 규칙 (Collaboration)

### 언어 규칙 (Language Rules)
- **한/영 혼용 전략**:
  - 설명, 분석, 보고: **한국어** (명확한 소통)
  - 기술 용어, 파일명, 코드: **영어** (정확성 유지)

### 행동 원칙
| 상황 | 행동 |
|------|------|
| 요청이 모호할 때 | 명확한 질문을 통해 확인 (추측 금지) |
| 대규모 변경 전 | 영향도 분석(Impact Analysis) 보고 후 승인 요청 |
| 에러 발생 시 | 문제 설명 + 진단 + 해결책(Self-Correction) 순으로 보고 |
