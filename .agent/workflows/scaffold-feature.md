---
description: 한 번의 명령으로 PRD 생성부터 Task 분해, 초기 구현까지 연결하는 통합 워크플로우입니다.
version: 1.0.0
author: Antigravity
---

# Feature Scaffold Workflow (기능 개발 통합 실행)

> [!NOTE]
> 이 워크플로우는 `/create-prd`, `/generate-tasks`, `/run-epic`을 논리적으로 연결하여 기능 개발의 초기 단계를 자동화합니다.
> **Orchestrator Role**: 에이전트는 각 단계의 산출물이 확실히 생성되었는지 검증(Latch)한 후 다음 단계로 넘어갑니다.

## 사용법

```
/scaffold-feature [기능명] [간단한 요구사항 설명]
```

## 실행 프로세스 (Orchestration Flow)

### Phase 1: PRD 생성 (Product Definition)

1.  **Trigger**: 내부적으로 `/create-prd` 로직을 수행합니다.
    -   사용자의 요구사항 설명을 분석합니다.
    -   (필요시) 기술 스택(`docs/PROJECT-CONFIG.md`)을 읽어옵니다.
    -   명확화 질문 3~5개를 사용자에게 던집니다.
2.  **Wait**: 사용자의 답변을 기다립니다.
3.  **Draft & Confirm**: PRD 초안을 작성하여 사용자에게 보여줍니다.
4.  **Latch (잠금)**: 
    -   사용자가 승인하면 `docs/PRD-[기능명].md`를 저장합니다.
    -   **검증**: `ls -l docs/PRD-[기능명].md`로 파일 생성을 확인합니다.
    -   *파일이 없으면 Phase 2로 진행하지 마십시오.*

### Phase 2: Tasks 분해 (Work Breakdown)

1.  **Trigger**: Phase 1에서 생성된 PRD를 입력으로 `/generate-tasks` 로직을 수행합니다.
2.  **Epic Design**: 먼저 상위 Epic 목록을 설계하여 사용자에게 보여줍니다.
3.  **Wait**: 사용자의 "Go" 신호를 기다립니다.
4.  **Generation**: 승인 즉시 상세 Task 목록을 생성합니다.
5.  **Latch (잠금)**: 
    -   `docs/TASKS-[기능명].md`를 저장합니다.
    -   **검증**: `ls -l docs/TASKS-[기능명].md`로 파일 생성을 확인합니다.
    -   *파일이 없으면 Phase 3로 진행하지 마십시오.*

### Phase 3: 실행 계획 수립 및 킥오프 (Kickoff)

1.  **Review**: 생성된 TASKS 파일을 읽고, 첫 번째 Epic(보통 '프로젝트 설정')을 식별합니다.
2.  **Proposal**: 사용자에게 다음 행동을 제안합니다.
    -   옵션 A: `/run-epic EPIC-XX`로 즉시 구현 시작
    -   옵션 B: `/execute-task TASK-XX-01`로 첫 작업만 수동 시작
    -   옵션 C: 여기서 멈추고 검토
3.  **Auto-Start (선택)**: 사용자가 `/scaffold-feature ... --auto` 플래그를 사용했다면, 옵션 A를 자동으로 시작합니다.

---

## 에이전트 행동 지침 (Orchestration Rules)

1.  **Context Passing**: 이전 단계의 결과물(파일명, 핵심 내용)을 다음 단계의 컨텍스트로 명확히 전달하세요.
    -   *"PRD 생성이 완료되었습니다. 이제 이 파일(`docs/PRD-auth.md`)을 바탕으로 Task를 생성하겠습니다."*
2.  **Step-by-Step Verification**: 각 단계 사이에는 반드시 **물리적 파일 검증**이 있어야 합니다. 예측으로 진행하지 마세요.
3.  **Error Handling**: 만약 중간 단계에서 실패하면, 전체 프로세스를 중단하고 사용자에게 개입을 요청하세요.
    -   *"PRD 저장에 실패하여 Task 생성을 중단합니다. 다시 시도해 주세요."*

## 출력 예시

```markdown
🚀 **기능 스캐폴딩 시작 (Feature Scaffolding Started): [Auth System]**

---

### Phase 1: PRD 정의 (PRD Definition)
✅ PRD 생성됨 (PRD Created): `docs/PRD-auth.md`

### Phase 2: Task 분해 (Task Breakdown)
✅ TASKS 생성됨 (TASKS Generated): `docs/TASKS-auth.md`
   - Epic 개수: 3
   - 총 Task 수: 12

---

🏁 **구현 준비 완료! (Ready to code!)**
첫 번째 Epic (EPIC-01: 초기 설정)을 시작하려면 다음을 입력하세요:
`/run-epic EPIC-01`
```
