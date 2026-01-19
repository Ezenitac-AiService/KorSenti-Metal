---
description: Run the project's test suite (Unit, E2E, Regression) and verify quality.
version: 1.0.0
author: Antigravity
---

# Test Suite Execution & QA

> [!NOTE]
> **문서 독자**: 한국인 개발자 + AI 에이전트
> **언어 규칙**: 문서는 **한국어**로 작성하되, 핵심 기술 용어는 **영어**를 사용하거나 **한국어 (English)** 형식을 사용합니다.

This prompt guides the AI to systematically run, analyze, and improve the project's tests. It covers Unit, E2E, and Regression testing to ensure "Release Readiness".

## 1. Test Strategy Analysis
Before running commands, identifying the scope is critical.

### The Test Pyramid
1.  **Unit Tests** (Fast, Isolated): Verify individual functions/classes.
2.  **Integration Tests** (Medium): Verify modules working together (e.g., API + DB).
3.  **E2E Tests** (Slow, Critical): Verify full user flows (e.g., Playwright/Cypress).

### Scope Determination
- **Target**: What changed? (Specific file, specific feature, or full release?)
- **Impact**: What other parts might break? (Regression risk)

## 2. Environment Discovery
Identify the test runner and configuration:
- Look for `package.json` scripts (`test`, `test:e2e`, `test:unit`).
- Look for `Makefile`, `pytest.ini`, `playwright.config.ts`.
- **Action**: Check if defining a "Test Plan" is necessary before execution.

## 3. Execution Process

### Step 1: Unit & Integration Tests (The Base)
Run the fast feedback loop first.
```bash
# Example
npm run test:unit
# or
pytest tests/unit
```
- **If Fail**: Analyze the stack trace. Is it logic error or test error?
- **Self-Healing**: If the fix is trivial (e.g., typo, import), fix it. If logic is deep, report it.

### Step 2: E2E & UI Tests (The Peak)
Only proceed if Unit tests pass.
```bash
# Example
npx playwright test
```
- **Screenshot Analysis**: If visual regression is detected, compare `actual` vs `expected`.
- **Flakiness**: Identify if the failure is random (Network) or real.

### Step 3: Regression Verification [CRITICAL]
- Did previously passing tests fail?
- **Rule**: A feature is NOT done if it breaks existing functionality.

## 4. Test Gap Analysis (BDD/TDD)
- Read the active `docs/PRD-*.md` file.
- Are there "Acceptance Criteria" without corresponding tests?
- **Action**: Suggest or Generate missing test cases if coverage is low.

## 5. Final Report & Latch

### Output Format
Generate a summary table:

| Category | Total | Passed | Failed | Skipped | Status |
|----------|-------|--------|--------|---------|--------|
| Unit     | 50    | 50     | 0      | 0       | ✅      |
| E2E      | 5     | 4      | 1      | 0       | ❌      |
| Coverage | 85%   | -      | -      | -       | ⚠️      |

### [Test Report Latch] [CRITICAL]
1.  **Save Report**: 테스트 결과를 분석하여 `docs/TEST_REPORT.md` (또는 적절한 이름)에 저장하십시오.
2.  **Filesystem Proof**:
    - `write_to_file` 실행.
    - **즉시 `ls -l docs/TEST_REPORT.md` 실행하여 파일 확인.**
    - *파일이 없으면 완료 보고를 하지 마십시오.*

**Completion Condition**:
- If tests pass: "✅ All Systems Go. Ready for generic/deployment."
- If tests fail: "❌ QA Failed. See Report above."
