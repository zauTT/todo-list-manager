import click
from tabulate import tabulate
from datetime import datetime
from typing import Optional

from src.database import (
    add_task,
    get_tasks,
    get_task_by_id,
    complete_task,
    uncomplete_task,
    delete_task,
    update_task
)

@click.group()
def cli():
    """Todo List Manager"""
    pass

@cli.command()
@click.argument('title')
@click.option('--description', '-d', help='Task description')
@click.option('--priority', '-p',
            type=click.Choice(['high', 'medium', 'low']),
            default='medium',
            help='Task priority (default: medium)')
@click.option('--due', help='Due date in YYYY-MM-DD format')
def add(title: str, description: Optional[str], priority: str, due: Optional[str]):

    try:
        task_id = add_task(title, description, priority, due)
        click.echo(f"✓ Task added successfully (ID: {task_id})")
    except Exception as e:
        click.echo(f"✗ Error adding task: {e}", err=True)

@cli.command()
@click.option('--all', '-a', 'show_all', is_flag=True, help='Show completed tasks too')
@click.option('--priority', '-p', help='Filter by priority (high/medium/low)')
@click.option('--sort', '-s', 
                type=click.Choice(['created_at', 'due_date', 'priority']),
                default='created_at',
                help='Sort tasks by field')
def list(show_all: bool, priority: Optional[str], sort: str):
    try:
        tasks = get_tasks(
            show_completed=show_all,
            priority_filter=priority,
            sort_by=sort
        )

        if not tasks:
            click.echo("No tasks found.")
            return

        headers = ['ID', 'Title', 'Priority', 'Due Date', 'Status', 'Created']
        rows = []

        for task in tasks:
            task_id, title, description, priority, due_date, completed, completed_at, created_at = task

            status = '✓ Done' if completed else '○ pending'

            if due_date and not completed:
                due = datetime.fromisoformat(due_date).date()
                today = datetime.now().date()
                if due < today:
                    due_date = f"{due_date} (OVERDUE!)"

            rows.append([
                len(rows) + 1,
                title[:30],
                priority,
                due_date or '-',
                status,
                created_at[:10] 
            ])

        click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
        click.echo(f"\nTotal: {len(tasks)} task(s)")

    except Exception as e:
        click.echo(f"✗ Error listing tasks: {e}", err=True)

@cli.command()
@click.argument('task_id', type=int)
def complete(task_id: int):
    try:
        task = get_task_by_id(task_id)
        if not task:
              click.echo(f"✗ Task {task_id} not found.", err=True)
              return

        if task[5]:
            click.echo(f"Task {task_id} already completed")
            return

        if complete_task(task_id):
            click.echo(f"✓ Task {task_id} marked as completed!")
        else:
            click.echo(f"✗ Failed to complete task {task_id}.", err=True)

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)

@cli.command()
@click.argument('task_id', type=int)
def uncomplete(task_id: int):
    try:
        task = get_task_by_id(task_id)
        if not task:
            click.echo(f"✗ Task {task_id} not found.", err=True)
            return

        if not task[5]:
            click.echo(f"Task {task_id} is already incomplete")
            return
        
        if uncomplete_task(task_id):
            click.echo(f"✓ Task {task_id} marked as incomplete!")
        else:
            click.echo(f"✗ Failed to uncomplete task {task_id}.", err=True)

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)

@cli.command()
@click.argument('task_id', type=int)
@click.confirmation_option(prompt='Are you sure you want to delete the task?')
def delete(task_id: int):
    try:
        task = get_task_by_id(task_id)
        if not task:
            click.echo(f"✗ Task {task_id} not found.", err=True)
            return

        if delete_task(task_id):
            click.echo(f"✓ Task {task_id} deleted successfully!")
            return

        else:
            click.echo(f"✗ Failed to delete task {task_id}.", err=True)
    
    except Exception as e:
          click.echo(f"✗ Error: {e}", err=True)

@cli.command()
@click.argument('task_id', type=int)
@click.option('--title', '-t', help='New task title')
@click.option('--description', '-d', help='New task description')
@click.option('--priority', '-p', type=click.Choice(['high','medium','low']), help='New task priority')
@click.option('--due', help='New due date in YYYY-MM-DD format')
def update(task_id: int, title: Optional[str], description: Optional[str], priority: Optional[str], due: Optional[str]):
    try:
        task = get_task_by_id(task_id)
        if not task:
            click.echo(f"✗ Task {task_id} not found.", err=True)
            return

        updates = {}
        if title:
            updates['title'] = title
        if description:
             updates['description'] = description
        if priority:
            updates['priority'] = priority
        if due:
            updates['due_date'] = due

        if not updates:
            click.echo("✗ No updates provided. Use --title, --description, --priority, or --due", err=True)
            return

        if update_task(task_id, **updates):
            click.echo(f"✓ Task {task_id} updated successfully!")
        else:
            click.echo(f"✗ Failed to update task {task_id}.", err=True)

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)

@cli.command()
@click.argument('task_id', type=int)
def show(task_id: int):
    try:
        task = get_task_by_id(task_id)
        if not task:
            click.echo(f"✗ Task {task_id} not found.", err=True)
            return

        task_id, title, description, priority, due_date, completed, completed_at, created_at = task

        click.echo(f"\n{'=' * 50}")
        click.echo(f"Task ID: {task_id}")
        click.echo(f"Title: {title}")
        click.echo(f"Description: {description or 'No description'}")
        click.echo(f"Priority: {priority}")
        click.echo(f"Due Date: {due_date or 'Not set'}")
        click.echo(f"Status: {'✓ Completed' if completed else '○ Pending'}")

        if completed and completed_at:
            click.echo(f"Completed At: {completed_at}")
            click.echo(f"Created At: {created_at}")
        click.echo(f"{'='*50}\n")

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)

if __name__ == '__main__':
      cli()