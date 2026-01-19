---
name: git-manager
description: Automates git operations ensuring conventional commits and safety.
version: 1.0.0
---

# Git Manager Skill

This skill handles version control operations with a focus on "Atomic Commits" and "Safety".

## Actions

### 1. `smart_commit`
**Goal**: Create a semantic commit for the current changes.

**Procedure**:
1.  **Status Check**: Run `git status`.
    -   If clean, stop (nothing to commit).
    -   If there are untracked files you created, run `git add <file>`.
2.  **Diff Analysis**: Run `git diff --cached`.
    -   If empty (but status showed changes), run `git add .` then `git diff --cached`.
3.  **Message Generation**: Generate a commit message based on the diff using **Conventional Commits**:
    -   `feat: ...` for new features
    -   `fix: ...` for bugs
    -   `refactor: ...` for code restructuring
    -   `docs: ...` for documentation
    -   `test: ...` for tests
    -   *Rule*: Keep subject under 50 chars. Use imperative mood.
4.  **Execute**: Run `git commit -m "messsage"`.
5.  **Verify**: Run `git log -1 --oneline` to confirm.

### 2. `safe_push`
**Goal**: Push changes to remote without force-overwriting.

**Procedure**:
1.  **Fetch**: Run `git fetch`.
2.  **Rebase**: Run `git pull --rebase`.
    -   If conflicts, STOP and ask user.
3.  **Push**: Run `git push`.

## Usage Examples
- "Save these changes" -> checks status, adds, commits with generated message.
- "Push to origin" -> safe push.
