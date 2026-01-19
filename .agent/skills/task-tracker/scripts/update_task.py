import argparse
import re
import os
import sys

def find_tasks_file():
    docs_dir = 'docs'
    if not os.path.exists(docs_dir):
        return None
    for f in os.listdir(docs_dir):
        if f.startswith('TASKS-') and f.endswith('.md'):
            return os.path.join(docs_dir, f)
    return None

def update_task_status(file_path, task_id, status):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find the task line: "- [ ] TASK-ID ..."
    # We look for "- [ ]" or "- [x]" followed by the ID
    pattern = rf'(-\s*\[)([\sx])(\]\s*{re.escape(task_id)}\b.*)'
    
    match = re.search(pattern, content)
    if not match:
        print(f"Error: Task ID '{task_id}' not found in {file_path}")
        return False

    current_mark = match.group(2)
    new_mark = 'x' if status == 'done' else ' '
    
    if current_mark == new_mark:
        print(f"Task '{task_id}' is already set to '{status}'.")
        return True

    # Replace logic
    # Group 1: "- ["
    # Group 2: mark
    # Group 3: "] TASK-ID..."
    new_line = f"{match.group(1)}{new_mark}{match.group(3)}"
    content = content.replace(match.group(0), new_line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Successfully updated '{task_id}' to '{status}' in {file_path}.")
    return True

def calculate_progress(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    total = len(re.findall(r'-\s*\[[\sx]\]\s*TASK-', content))
    done = len(re.findall(r'-\s*\[x\]\s*TASK-', content))
    
    if total == 0:
        return 0
    return int((done / total) * 100)

def main():
    parser = argparse.ArgumentParser(description='Update Task Status in Markdown')
    parser.add_argument('task_id', help='Task ID (e.g., TASK-01-01)')
    parser.add_argument('--status', choices=['done', 'todo'], default='done', help='New status')
    parser.add_argument('--file', help='Path to TASKS file (optional)')
    
    args = parser.parse_args()
    
    target_file = args.file
    if not target_file:
        target_file = find_tasks_file()
    
    if not target_file:
        print("Error: Could not find any TASKS-*.md file in docs/")
        sys.exit(1)
        
    print(f"Targeting file: {target_file}")
    success = update_task_status(target_file, args.task_id, args.status)
    
    if success:
        progress = calculate_progress(target_file)
        print(f"Current Progress: {progress}%")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
