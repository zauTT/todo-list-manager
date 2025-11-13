from datetime import date, datetime
from typing import Optional
import click

def validate_date(date_str:str) -> bool:
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def format_date(date_str: Optional[str]) -> str:
    if not date_str:
        return '-'
    return date_str[:10]

def format_overdue(date_str: str) -> str:
    if not date_str:
        return '-'
    
    due = datetime.fromisoformat(date_str).date()
    today = datetime.now()

    if due < today:
        return f"{date_str} (OVERDUE!)"
    return date_str
    
def get_priority_order(priority: str) -> int:

    priority_map = {'high': 1, 'medium': 2, 'low': 3}
    return priority_map.get(priority, 2)

def success_message(text: str):
    click.echo(click.style(f"✓ {text}", fg='green'))

def error_message(text: str):
    click.echo(click.style(f"✗ {text}", fg='red'), err= True)

def truncate_text(text: str, max_length: int = 30) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + '...'