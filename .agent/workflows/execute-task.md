---
description: 개별 Task를 실행하고 코드를 구현합니다.
version: 1.0.0
author: Antigravity
---


# 단일 Task 실행 프롬프트

> [!NOTE]
> **문서 독자**: 한국인 개발자 + AI 에이전트
> **언어 규칙**: 코드 주석과 결과 보고는 **한국어**로 작성합니다. 핵심 기술 용어는 **영어**를 사용하거나 **한국어 (English)** 형식을 사용합니다.

이 프롬프트를 사용하여 TASKS 문서의 특정 Task를 실행하고 완료 표시합니다.

## 사용법

```
/execute-task TASK-XX-XX
```

> [!NOTE]
> Task ID만 제공하면 모든 `docs/TASKS-*.md` 파일에서 자동으로 검색합니다.

## 지침

당신은 작업 목록에서 하나의 Task를 체계적으로 수행하는 개발자입니다. Task를 완료하고 Definition of Done (DoD) 기준을 충족시킨 후 체크 표시를 해야 합니다.

### 프로세스

1. **Plan & Binding (계획 및 바인딩)** [필수]:
   - `docs/TASKS-*.md` 파일에서 대상 Task의 XML 정의를 읽습니다.
   - **반드시** 다음 `<execution-plan>` 블록을 작성하여 사용자에게 출력해야 합니다:
   
   ```xml
   <execution-plan>
     <context-analysis>
       <read_file>docs/TASKS-*.md</read_file>
       <read_file>docs/PRD-*.md</read_file>
       <read_file>[Task XML의 relevant_context에 명시된 파일]</read_file>
     </context-analysis>
     <target-spec>
       <file>[수정할 파일 경로]</file>
       <goal>[TASK의 목표 요약]</goal>
     </target-spec>
     <test-spec>
       <file>[테스트 파일 경로]</file>
       <command>[TASKS 파일의 verification_method]</command>
     </test-spec>
     <tdd-strategy>
       1. [Red] 테스트 작성 (예상 실패)
       2. [Green] 기능 구현
       3. [Refactor] 코드 개선
     </tdd-strategy>
     <risk-assessment>
       [예상되는 부작용 또는 구현 난이도 상]
     </risk-assessment>
   </execution-plan>
   ```

2. **Context Preservation (컨텍스트 확보)**:
   - 관련 `docs/TASKS-*.md`, `docs/PRD-*.md`, `docs/PROJECT-CONFIG.md`를 읽습니다.

3. **Intelligent Research (지능형 조사)** [필요시]:
   > [!TIP]
   > 구현 방법이 확실하지 않거나 복잡한 경우, 혼자서 추측하지 말고 **반드시 도구를 사용**하십시오.

   | 도구 | Trigger (언제 사용?) | 용도 |
   |------|---|---|
   | `#tool:context7` | "API가 뭐더라?" | 라이브러리 최신 스펙 확인 |
   | `#tool:firecrawl` | "공식 문서가 필요해" | 외부 문서/블로그 검색 및 스크랩 |
   | `#tool:sequential-thinking` | "어떻게 설계하지?" | 복잡한 로직 분해, 대안 분석 |

4. **BASELINE CHECK (사전 검증)**:
   - 작업을 시작하기 전에 `<verification-command>`를 한 번 실행하여 현재 상태를 확인합니다. (이미 통과한다면 TDD 위반 가능성 체크)

5. **TDD Cycle (테스트 주도 개발)** [핵심]:
   
   > [!IMPORTANT]
   > 구현 코드를 먼저 작성하지 마십시오. 반드시 **테스트 실패(Red)**를 먼저 확인해야 합니다.

   **Step 1: Fail Test (Red)**
   - `<test-file>`을 생성하거나 테스트 케이스를 추가합니다.
   - 테스트를 실행하여 **실패함**을 확인합니다. (에이전트는 실패 로그를 확인해야 함)

   **Step 2: Implement (Green)**
   - `replace_string_in_file` 등으로 `<target-file>`을 수정하여 기능을 구현합니다.
   - *Safe Implementation*: 수정 후 즉시 `view_file`로 문법/들여쓰기를 시각적으로 검증합니다.

   **Step 3: Verify (Blue)**
   - **`code-verifier` 스킬**("코드 검증해줘")을 사용하거나, `<verification-command>`를 실행하여 **성공(Pass)**함을 확인합니다.

6. **Completion Latch (완료 잠금)**:
   > [!CRITICAL]
   > `task-tracker` 스킬을 사용하여 안전하게 완료 처리하십시오.
   
   - 다음 자연어 명령 또는 스크립트를 사용하여 Task를 완료 처리합니다:
     - "TASK-XX-XX 완료 처리해줘"
     - 또는 `python3 .agent/skills/task-tracker/scripts/update_task.py TASK-XX-XX --status done`
   - **Proof of Work**: 스크립트가 반환하는 "Successfully updated..." 메시지와 진행률을 확인합니다.

7. **Git Commit (형상관리)**:
   - **`git-manager` 스킬을 호출**하여 안전하게 커밋합니다.
   - "이 변경사항 커밋해줘" 라고 말하거나 `smart_commit` 기능을 사용하십시오.
   - 스킬이 자동으로 Status 확인 -> Add -> Diff 분석 -> 메시지 생성 -> Commit 과정을 수행합니다.

8. **Result Report (결과 보고)**:
   - 완료된 작업을 요약하고 다음 Task를 제안합니다.

### Task 실행 예시 (TDD Workflow)

```
Task ID: TASK-04-02
Task 내용: 할일 추가 UI 컴포넌트 생성

1. [Plan]
   - Target: components/todo-form.tsx
   - Test: tests/unit/todo-form.test.tsx
   - Command: npm test tests/unit/todo-form.test.tsx

2. [Red]
   - 테스트 파일 생성 (TodoForm 렌더링 시도)
   - 실행 -> FAIL (컴포넌트 없음)

3. [Green]
   - components/todo-form.tsx 생성 (기본 골격)
   - Safe Check: view_file로 문법 확인

4. [Verify]
   - 실행 -> PASS

5. [Latch]
   - TASKS 파일 수정 -> grep으로 확인

6. [Commit]
   - git commit -m "feat(todo): TASK-04-02 - UI 컴포넌트 추가"
```

### Task 복잡도 레이블

| 레이블 | 예상 시간 | 설명 |
|--------|----------|------|
| 🟢 간단 | ~30분 | 단일 파일 수정 |
| 🟡 보통 | ~2시간 | 여러 파일 수정 |
| 🔴 복잡 | ~1일+ | 아키텍처 변경 |

### DoD (Definition of Done) 기준

> [!TIP]
> 전체 DoD 정의는 `.agent/rules/coding-standards.md`의 **Definition of Done** 섹션을 참조하세요.
> 아래는 Task 실행 시 빠르게 확인할 수 있는 요약입니다.

각 Task는 다음 조건을 **모두** 충족해야 완료로 표시할 수 있습니다:

#### 1. 코드 작성 완료 ✅
- 요구사항에 명시된 모든 기능 구현
- TypeScript 타입 에러 0개
- ESLint 경고/에러 0개

#### 2. 테스트 작성 및 통과 ✅
- 유닛 테스트 작성 (최소 주요 기능)
- E2E 테스트 작성 (사용자 플로우에 해당되는 경우)
- 모든 테스트 통과 (기존 테스트 포함)

#### 3. 문서화 ✅
- 복잡한 로직에 주석 추가
- 공개 API에 JSDoc 추가
- README 업데이트 (새로운 기능인 경우)

#### 4. 코드 리뷰 ✅
- 자기 검토 완료
- 디버깅 코드 제거 (console.log 등)
- 코드 스타일 가이드 준수

#### 5. 통합 확인 ✅
- 로컬 개발 환경에서 동작 확인
- 기존 기능과의 호환성 확인
- 시각적 확인 (UI 관련 Task인 경우)

### 에러 처리 및 복구

Task 실행 중 문제가 발생한 경우:

#### 에러 복구 절차 (Proactive Recovery)

1. **에러 식별**: 정확한 에러 메시지와 위치를 파악합니다
2. **원인 분석**: 에러의 근본 원인을 찾습니다
3. **Proactive Search (능동적 검색)**:
   - 에러 메시지 그대로 `#tool:context7` 또는 `#tool:firecrawl` 검색 쿼리로 사용합니다.
   - *자신의 지식에만 의존하여 추측하지 마십시오.*
4. **해결책 적용**: 조사된 공식 문서를 바탕으로 수정 사항을 적용합니다
5. **재검증**: 수정 후 모든 테스트를 다시 실행합니다
6. **문서화**: 복잡한 문제였다면 해결 과정을 주석으로 남깁니다

#### 반복 및 재구성 전략 (Iteration Strategy)

> [!TIP]
> **ai-dev-tasks Best Practice**: AI가 Task를 제대로 수행하지 못할 경우, 포기하지 말고 다음을 시도하세요.

**문제 상황별 대응**:

| 상황 | 대응 전략 |
|------|----------|
| AI가 요구사항을 잘못 이해함 | Task 설명을 더 구체적으로 **재구성(Rephrase)** |
| 구현이 너무 복잡함 | Task를 더 작은 단위로 **분할** |
| 컨텍스트 부족 | 관련 파일을 `@filename`으로 **추가 제공** |
| 반복적인 실패 | `#tool:sequential-thinking`으로 **단계별 분석** |

**재구성 예시**:
```text
# Before (모호함)
"로그인 기능 구현해줘"

# After (구체적)
"Flask-Login을 사용하여 app.py에 /login 라우트를 추가하고,
models.py의 User 클래스에 password_hash 필드를 사용한 
인증 로직을 구현해줘. 참조: @models.py @templates/login.html"
```

#### 4. 자율 수정 및 복구 루프 (Autonomous Recovery Loop)
> [!CRITICAL]
> **Replit Agent Pattern**: 에러 발생 시 단순 재시도를 금지합니다.
> 다음 루프를 **최대 3회** 수행하여 스스로 문제를 해결하십시오.

1. **Diagnosis (진단)**:
   - 에러 로그의 `stderr`를 분석하여 근본 원인을 파악합니다.
   - 필요시 `#tool:firecrawl`로 에러 메시지를 검색합니다.

2. **Strategy Adjustment (전략 수정)**:
   - 기존 `<execution-plan>`이 실패했음을 인정하고 수정합니다.
   - 예: "라이브러리 버전 호환성 문제임. 다운그레이드 전략으로 변경."

3. **Execution (수정 실행)**:
   - 수정된 코드를 적용합니다.
   - **반드시** `code-verifier` 스킬로 재검증합니다.

**에스컬레이션 트리거 (Human Escalation)**:
- 3회 연속 동일 오류 발생
- 보안 관련 오류 (인증/권한 문제)
- 데이터 손실 위험 감지
- 외부 서비스 장애 (API 다운)

#### 롤백 절차 (Rollback Procedure)

심각한 문제 발생 시:

```bash
# 변경사항 취소
git checkout .

# 또는 임시 저장 후 나중에 복구
git stash
```

#### 에러 유형별 대응

| 에러 유형 | 대응 방법 |
|----------|----------|
| 타입 에러 | 타입 정의 수정, context7로 올바른 타입 확인 |
| 테스트 실패 | 테스트 코드 또는 구현 코드 수정 |
| 린트 에러 | 코드 스타일 수정 |
| 빌드 에러 | 의존성 확인, 설정 파일 검토 |

### 출력 형식

Task 실행이 완료되면 다음과 같이 보고합니다:

```
✅ TASK-01-01 완료!

📝 작업 내용:
- components/todo-form.tsx 생성
- 할일 추가 폼 UI 구현
- Tailwind CSS 스타일링 적용

📄 변경된 파일:
- components/todo-form.tsx (새 파일)
- tests/unit/todo-form.test.tsx (새 파일)

✅ DoD 체크리스트:
- [x] 코드 작성 완료
- [x] 테스트 작성 및 통과
- [x] 문서화
- [x] 코드 리뷰
- [x] 통합 확인

📋 TASKS 파일 업데이트:
- docs/TASKS-todo-list.md에서 TASK-01-01을 [x]로 표시했습니다

다음 Task:
- TASK-01-02: 할일 목록 표시 컴포넌트 생성

계속하려면: /execute-task TASK-01-02
```

### 주의사항

1. **한 번에 하나의 Task만**: 여러 Task를 동시에 수행하지 마세요
2. **DoD 필수 준수**: 모든 DoD 기준을 충족해야만 Task를 완료로 표시합니다
3. **테스트 필수**: 테스트 없이 Task를 완료로 표시하지 마세요
4. **문서 업데이트**: 항상 TASKS 파일을 업데이트하여 진행 상황을 추적합니다
5. **의존성 확인**: 이전 Task가 완료되지 않았다면 먼저 완료하세요

### 관련 명령어

- **다음 Task 실행**: `/execute-task TASK-XX-XX`
- **Epic 전체 실행**: `/run-epic EPIC-XX`
- **진행 상황 확인**: TASKS 파일을 직접 열어서 확인
