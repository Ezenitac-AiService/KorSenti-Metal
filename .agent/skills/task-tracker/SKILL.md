---
name: task-tracker
description: Manages task status and progress tracking using Python scripts.
version: 1.0.0
---

# Task Tracker Skill

This skill ensures reliable updates to the project's tracking documents (`docs/TASKS-*.md`).
It avoids regex errors common with LLMs by using a dedicated Python script.

## Actions

### 1. `mark_task_done`
**Goal**: Mark a specific task as complete `[x]`.

**Procedure**:
1.  **Identify Task ID**: Extract the ID (e.g., `TASK-01-01`) from the user request.
2.  **Execute Script**:
    ```bash
    python3 .agent/skills/task-tracker/scripts/update_task.py [TASK_ID] --status done
    ```
3.  **Report**: Output the result and the new progress percentage returned by the script.

### 2. `mark_task_todo`
**Goal**: Revert a task to incomplete `[ ]`.

**Procedure**:
1.  **Identify Task ID**: Extract the ID.
2.  **Execute Script**:
    ```bash
    python3 .agent/skills/task-tracker/scripts/update_task.py [TASK_ID] --status todo
    ```

### 3. `get_status`
**Goal**: Check the status of a specific task.

**Procedure**:
1.  **Grep Check**: `grep "[TASK_ID]" docs/TASKS-*.md`
2.  **Visual Verify**: interpret the `[ ]` or `[x]`.

## Usage Examples
- "I finished TASK-01-05" -> calls `mark_task_done TASK-01-05`
- "Rollback status of TASK-02-01" -> calls `mark_task_todo`
