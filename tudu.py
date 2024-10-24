import argparse
import shelve
import os
from datetime import datetime, timedelta
from plyer import notification
from tabulate import tabulate

# Initialize the argument parser
parser = argparse.ArgumentParser(description='Terminal task management app')

# Define subcommands
subparsers = parser.add_subparsers(dest='command')

# New task command
new_parser = subparsers.add_parser('new', help='Create a new task')
new_parser.add_argument('task', type=str, help='Task description')
new_parser.add_argument('-s', '--status', type=str, default='todo', help='Task status')
new_parser.add_argument('-p', '--priority', type=str, default='normal', help='Task priority')
new_parser.add_argument('-d', '--due', type=str, help='Task due time (e.g., 1h, 2d)')

# List tasks command
list_parser = subparsers.add_parser('ls', help='List tasks')
list_parser.add_argument('-s', '--status', type=str, help='Filter by status')
list_parser.add_argument('-p', '--priority', type=str, help='Filter by priority')

# Reminder command
reminder_parser = subparsers.add_parser('reminder', help='Manage reminders')
reminder_parser.add_argument('action', choices=['start', 'stop', 'time'], help='Reminder action')
reminder_parser.add_argument('times', nargs='*', help='Reminder times (e.g., 1m, 15m)')

# Remove task command
rm_parser = subparsers.add_parser('rm', help='Remove a task')
rm_parser.add_argument('task_id', type=str, help='ID of the task to remove')

# Update task command
update_parser = subparsers.add_parser('update', help='Update a task')
update_parser.add_argument('task_id', type=str, help='ID of the task to update')
update_parser.add_argument('-s', '--status', type=str, help='New status for the task')
update_parser.add_argument('-p', '--priority', type=str, help='New priority for the task')
update_parser.add_argument('-d', '--due', type=str, help='New due time for the task')

# Task storage
TASK_DB = os.path.expanduser('~/.tudu_tasks.db')

def add_task(task, status, priority, due):
    print(f"Adding task: {task}, Status: {status}, Priority: {priority}, Due: {due}")
    print(f"Database path: {TASK_DB}")
    with shelve.open(TASK_DB) as db:
        task_id = str(len(db) + 1)
        due_date = None
        if due:
            due_date = datetime.now() + parse_due_time(due)
        db[task_id] = {'task': task, 'status': status, 'priority': priority, 'due': due_date}
        print(f"Task '{task}' added with ID {task_id}")

def list_tasks(status=None, priority=None):
    with shelve.open(TASK_DB) as db:
        tasks = []
        for task_id, task_info in db.items():
            if (status and task_info['status'] != status) or (priority and task_info['priority'] != priority):
                continue
            status_emoji = {
                'todo': '📝',
                'doing': '⏳',
                'done': '✅'
            }.get(task_info['status'], '')
            priority_emoji = {
                'low': '🟢',
                'normal': '🟡',
                'high': '🔴'
            }.get(task_info['priority'], '')
            tasks.append([
                task_id,
                task_info['task'],
                f"{status_emoji} {task_info['status']}",
                f"{priority_emoji} {task_info['priority']}",
                task_info['due'].strftime('%Y-%m-%d %H:%M:%S') if task_info['due'] else 'None'
            ])
        print(tabulate(tasks, headers=['ID', 'Task', 'Status', 'Priority', 'Due'], tablefmt='fancy_grid'))

def parse_due_time(due):
    unit = due[-1]
    value = int(due[:-1])
    if unit == 'h':
        return timedelta(hours=value)
    elif unit == 'd':
        return timedelta(days=value)
    else:
        raise ValueError("Invalid due time format")

def start_reminder(times):
    # Example implementation for starting reminders
    print(f"Starting reminders at: {', '.join(times)}")

def remove_task(task_id):
    with shelve.open(TASK_DB) as db:
        if task_id in db:
            del db[task_id]
            print(f"Task with ID {task_id} removed.")
        else:
            print(f"No task found with ID {task_id}.")

def update_task(task_id, status=None, priority=None, due=None):
    with shelve.open(TASK_DB) as db:
        if task_id in db:
            task = db[task_id]
            if status:
                task['status'] = status
            if priority:
                task['priority'] = priority
            if due:
                task['due'] = datetime.now() + parse_due_time(due)
            db[task_id] = task
            print(f"Task with ID {task_id} updated.")
        else:
            print(f"No task found with ID {task_id}.")

def main():
    # Parse arguments
    args = parser.parse_args()

    # Command execution
    if args.command == 'new':
        add_task(args.task, args.status, args.priority, args.due)
    elif args.command == 'ls':
        list_tasks(args.status, args.priority)
    elif args.command == 'rm':
        remove_task(args.task_id)
    elif args.command == 'update':
        update_task(args.task_id, args.status, args.priority, args.due)
    elif args.command == 'reminder':
        if args.action == 'start':
            start_reminder(args.times)

if __name__ == '__main__':
    main()
