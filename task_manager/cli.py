"""Command-line user interface."""
from task_manager.models import (
    validate_title, validate_priority, validate_due_date
)
from task_manager.storage import StorageError

class TaskManagerCLI:
    def __init__(self, storage):
        self.storage = storage

    @staticmethod
    def _read_task_id():
        raw_value = input("Enter task ID: ").strip()
        try:
            task_id = int(raw_value)
            if task_id <= 0:
                raise ValueError
            return task_id
        except ValueError:
            print("Please enter a positive whole-number task ID.")
            return None

    def add_task(self):
        try:
            title = validate_title(input("Task title: "))
            description = input("Description (optional): ").strip()
            priority = validate_priority(
                input("Priority (low/medium/high) [medium]: ") or "medium"
            )
            due_date = validate_due_date(
                input("Due date YYYY-MM-DD (optional): ")
            )
            task = self.storage.add(title, description, priority, due_date)
            print(f"Task #{task.task_id} added successfully.")
        except ValueError as exc:
            print(f"Invalid input: {exc}")

    def view_tasks(self):
        tasks = self.storage.get_all()
        if not tasks:
            print("\nNo tasks found. Add your first task!")
            return
        print("\n" + "-" * 82)
        print(f"{'ID':<5}{'STATUS':<13}{'PRIORITY':<12}{'DUE DATE':<14}TITLE")
        print("-" * 82)
        for task in tasks:
            status = "Completed" if task.completed else "Pending"
            due = task.due_date or "-"
            print(f"{task.task_id:<5}{status:<13}{task.priority.title():<12}"
                  f"{due:<14}{task.title}")
            if task.description:
                print(f"     Description: {task.description}")
        print("-" * 82)

    def complete_task(self):
        task_id = self._read_task_id()
        if task_id is None:
            return
        task = self.storage.mark_completed(task_id)
        if task:
            print(f"Task #{task_id} marked as completed.")
        else:
            print(f"No task found with ID {task_id}.")

    def delete_task(self):
        task_id = self._read_task_id()
        if task_id is None:
            return
        if self.storage.delete(task_id):
            print(f"Task #{task_id} deleted.")
        else:
            print(f"No task found with ID {task_id}.")

    def show_summary(self):
        tasks = self.storage.get_all()
        completed = sum(task.completed for task in tasks)
        pending = len(tasks) - completed
        print("\nTASK SUMMARY")
        print(f"Total tasks: {len(tasks)}")
        print(f"Pending:     {pending}")
        print(f"Completed:  {completed}")

    def run(self):
        print("\n===================================")
        print("       SWYNEX TASK MANAGER")
        print("===================================")
        actions = {
            "1": self.add_task,
            "2": self.view_tasks,
            "3": self.complete_task,
            "4": self.delete_task,
            "5": self.show_summary,
        }
        while True:
            print("\n1. Add task")
            print("2. View all tasks")
            print("3. Mark task as completed")
            print("4. Delete task")
            print("5. View task summary")
            print("0. Exit")
            choice = input("\nChoose an option: ").strip()
            if choice == "0":
                print("Thank you for using SWYNEX Task Manager. Goodbye!")
                break
            action = actions.get(choice)
            if action is None:
                print("Invalid menu option. Please choose 0 to 5.")
                continue
            try:
                action()
            except StorageError as exc:
                print(f"Storage error: {exc}")
            except (EOFError, KeyboardInterrupt):
                print("\nApplication interrupted. Goodbye!")
                break
