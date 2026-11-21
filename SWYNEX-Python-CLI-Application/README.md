# SWYNEX Python CLI Task Manager

A modular, menu-driven task management application built with Python. It supports creating, viewing, completing, and deleting tasks, with persistent storage using a local JSON file.

## Features

- Add tasks with a title, optional description, priority, and due date.
- View all saved tasks and their current status.
- Mark tasks as completed.
- Delete tasks by ID.
- View a summary of total, pending, and completed tasks.
- Persist task information in `data/tasks.json`.
- Validate task titles, priorities, dates, and task IDs.
- Handle invalid input, JSON errors, and file read/write errors.
- Include automated unit tests.

## Technologies

- Python 3.9+
- Standard Python libraries: `json`, `dataclasses`, `datetime`, `pathlib`, `unittest`

No third-party packages are required.

## Project structure

```text
SWYNEX-Python-CLI-Application/
├── main.py
├── task_manager/
│   ├── __init__.py
│   ├── models.py
│   ├── storage.py
│   └── cli.py
├── data/
│   └── tasks.json
├── tests/
│   └── test_task_manager.py
├── .gitignore
└── README.md
```

## Requirements

Install Python 3.9 or newer. Check the installation:

```bash
python --version
```

On some systems, use `python3` instead of `python`.

## Run the application

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

```bash
python main.py
```

The application creates `data/tasks.json` automatically if it does not exist.

## Menu options

```text
1. Add task
2. View all tasks
3. Mark task as completed
4. Delete task
5. View task summary
0. Exit
```

For a due date, enter the date in `YYYY-MM-DD` format. Leave it blank if no due date is needed. Valid priorities are `low`, `medium`, and `high`.

## Run tests

From the project root, run:

```bash
python -m unittest discover -s tests -v
```

## Data storage

Tasks are stored locally in `data/tasks.json`. The file is updated when tasks are added, completed, or deleted. Keep a backup of this file if you want to preserve your task records when moving the project.

