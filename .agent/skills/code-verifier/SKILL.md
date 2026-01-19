---
name: code-verifier
description: Automated quality assurance using project configuration.
version: 1.0.0
---

# Code Verifier Skill

This skill acts as a QA engineer, ensuring code meets the "Definition of Done" before it is committed.

## Actions

### 1. `verify_task`
**Goal**: Run all necessary checks to verify a task is effectively "Done".

**Procedure**:
1.  **Config Check**: Read `docs/PROJECT-CONFIG.md` to identify:
    -   `[TEST_COMMAND]` (e.g., `npm test`, `pytest`)
    -   `[LINT_COMMAND]` (e.g., `npm run lint`, `pylint`)
2.  **Linting**: Execute the lint command.
    -   If fails: **STOP**. Return error analysis.
3.  **Testing**: Execute the test command.
    -   If fails: **STOP**. Return error analysis.
    -   *Optimization*: If possible, run only relevant tests (e.g., `pytest tests/test_login.py`).
4.  **Confirm**: If both pass (Exit Code 0), report "Verification Successful".

### 2. `analyze_failure`
**Goal**: Provide insightful debugging help when verification fails.

**Procedure**:
1.  **Log Capture**: Capture the *stderr* output of the failed command.
2.  **Focus**: Isolate the last 20 lines or the specific traceback.
3.  **Hint**: Suggest a fix based on the error message (e.g., "ImportError suggests missing dependency").

## Usage Examples
- "Verify implementations" -> Reads config, runs lint & test.
- "Check if TASK-01-02 is done" -> Runs verification pipeline.
