"""Entry point for the SWYNEX Task Manager CLI."""
from pathlib import Path
from task_manager.cli import TaskManagerCLI
from task_manager.storage import TaskStorage

def main():
    project_dir = Path(__file__).resolve().parent
    storage = TaskStorage(project_dir / "data" / "tasks.json")
    app = TaskManagerCLI(storage)
    app.run()

if __name__ == "__main__":
    main()
