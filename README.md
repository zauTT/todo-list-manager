# Todo List Manager

A simple, powerful CLI-based todo list manager with SQLite storage. Manage your tasks efficiently from the command line with priorities, due dates, and completion tracking.

## Features

- ✅ **CRUD Operations** - Add, view, update, and delete tasks
- 📅 **Due Dates** - Set and track task deadlines
- ⚠️ **Overdue Detection** - Automatic flagging of overdue tasks
- 🎯 **Priority Levels** - Organize tasks by high, medium, or low priority
- ✓ **Completion Tracking** - Mark tasks as complete/incomplete with timestamps
- 🔍 **Filtering & Sorting** - Filter by priority, sort by date or priority
- 💾 **SQLite Storage** - Persistent local database storage
- 🎨 **Formatted Display** - Clean table output with tabulate

## Installation

### Prerequisites
- Python 3.7 or higher
- pip

### Install from source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/todo-list-manager.git
cd todo-list-manager
```

2. Install in development mode:
```bash
pip install -e .
```

3. Add to PATH (if needed):
```bash
echo 'export PATH="/Library/Frameworks/Python.framework/Versions/3.14/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## Usage

### Add a task
```bash
todo add "Task title" [OPTIONS]

Options:
  -d, --description TEXT    Task description
  -p, --priority [high|medium|low]  Task priority (default: medium)
  --due TEXT               Due date in YYYY-MM-DD format
```

**Examples:**
```bash
todo add "Buy groceries"
todo add "Complete project" --priority high --due 2025-12-15
todo add "Call dentist" -p high -d "Schedule annual checkup"
```

### List tasks
```bash
todo list [OPTIONS]

Options:
  -a, --all                Show completed tasks too
  -p, --priority TEXT      Filter by priority (high/medium/low)
  -s, --sort [created_at|due_date|priority]  Sort tasks by field
```

**Examples:**
```bash
todo list                          # Show pending tasks
todo list --all                    # Show all tasks including completed
todo list --priority high          # Show only high priority tasks
todo list --sort due_date          # Sort by due date
```

### View task details
```bash
todo show TASK_ID
```

**Example:**
```bash
todo show 5
```

### Complete a task
```bash
todo complete TASK_ID
```

**Example:**
```bash
todo complete 3
```

### Mark task as incomplete
```bash
todo uncomplete TASK_ID
```

**Example:**
```bash
todo uncomplete 3
```

### Update a task
```bash
todo update TASK_ID [OPTIONS]

Options:
  -t, --title TEXT         New task title
  -d, --description TEXT   New task description
  -p, --priority [high|medium|low]  New task priority
  --due TEXT              New due date in YYYY-MM-DD format
```

**Example:**
```bash
todo update 5 --title "Buy organic groceries" --priority high
todo update 3 --due 2025-12-20
```

### Delete a task
```bash
todo delete TASK_ID
```

**Example:**
```bash
todo delete 7
```
*Note: Requires confirmation prompt*

## Example Workflow

```bash
# Add some tasks
todo add "Write documentation" --priority high --due 2025-11-20
todo add "Review pull requests" --priority medium
todo add "Update dependencies" --priority low --due 2025-12-01

# List all pending tasks
todo list

# View details of a specific task
todo show 1

# Complete a task
todo complete 1

# List with completed tasks
todo list --all

# Filter by priority
todo list --priority high

# Update a task
todo update 2 --priority high --due 2025-11-18

# Delete a task
todo delete 3
```

## Database

Tasks are stored in a SQLite database located at:
```
~/.todo_manager.db
```

### Database Schema
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT CHECK(priority IN ('high', 'medium', 'low')),
    due_date TEXT,
    completed INTEGER DEFAULT 0,
    completed_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
```

## Project Structure

```
todo-list-manager/
├── src/
│   ├── __init__.py       # Package initialization
│   ├── client.py         # CLI interface and commands
│   ├── database.py       # Database operations
│   ├── models.py         # Task data model
│   └── utils.py          # Utility functions
├── setup.py              # Package configuration
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## Dependencies

- [Click](https://click.palletsprojects.com/) - CLI framework
- [Tabulate](https://github.com/astanin/python-tabulate) - Pretty table formatting

## Development

### Running tests
```bash
# Coming soon
```

### Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Author

Giorgi Zautashvili (giorgi.zautashvili@promptrun.ai)

## Acknowledgments

Built with Python, Click, and Tabulate.
