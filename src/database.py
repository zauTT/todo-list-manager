import sqlite3
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime

DB_PATH = Path.home() / '.todo_manager.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        priority TEXT CHECK(priority IN ('high', 'medium', 'low')),
        due_date TEXT,
        completed INTEGER DEFAULT 0,
        completed_at TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

def add_task(title: str, description: Optional[str] = None, priority: str = 'medium', due_date: Optional[str] = None) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO tasks (title, description, priority, due_date)
        VALUES (?, ?, ?, ?)
    ''', (title, description, priority, due_date))

    task_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return task_id

def get_tasks(show_completed: bool = False, priority_filter: Optional[str] = None, sort_by: str = 'created_at') -> List[Tuple]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT * FROM tasks WHERE 1=1"
    params = []

    if not show_completed:
        query += " AND completed = 0"

    if priority_filter:
        query += " AND priority = ?"
        params.append(priority_filter)

    if sort_by == 'due_date':
        query += " ORDER BY due_date is NULL, due_date ASC"
    elif sort_by == 'priority':
        query += " ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END"
    else:
        query += " ORDER BY created_at DESC"

    cursor.execute(query, params)
    tasks = cursor.fetchall()
    conn.close()

    return tasks

def get_task_by_id(task_id: int) -> Optional[Tuple]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()

    return task

def complete_task(task_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    completed_at = datetime.now().isoformat()

    cursor.execute('''
        UPDATE tasks 
        SET completed = 1, completed_at = ?
        WHERE id = ?
    ''', (completed_at, task_id))

    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()

    return rows_affected > 0

def uncomplete_task(task_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE tasks
        SET completed = 0, completed_at = NULL
        WHERE id = ?
    ''', (task_id,))

    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()

    return rows_affected > 0


def delete_task(task_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()

    return rows_affected > 0

def update_task(task_id: int, **kwargs) -> bool:

    if not kwargs:
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    fields = []
    values = []

    for key, value in kwargs.items():
        if key in ['title', 'description', 'priority', 'due_date']:
            fields.append(f"{key} = ?")
            values.append(value)

    if not fields:
        conn.close()
        return False

    query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
    values.append(task_id)

    cursor.execute(query, values)
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()

    return rows_affected > 0

init_db()

