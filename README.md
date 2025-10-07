# Task Manager Tool
This application allows users to create and manage **tasks** and **projects**, link them together, and enforce strict **business rules** around deadlines and completion states.

The project structure, base configuration, and test setup were derived from my own custom FastAPI DDD Template - available at 👉 [github.com/veNNNx/fastAPI-bookshop-DDD-template](https://github.com/veNNNx/fastAPI-bookshop-DDD-template)

---

## Project Overview
- Managing **Tasks** and **Projects**
- Enforcing **deadline and completion constraints**
- Maintaining **clear domain boundaries**
- Providing **Swagger API documentation**
- Running via **Docker Compose**
- Testing via pytest
- CI via GitHub Actions
- JWT-based authentication

---

## Core Functionalities

### Task Management
- Create, retrieve, update, and delete tasks  
- Mark tasks as **completed** or **reopened**
- Filter tasks by completion state, overdue status, or project

### Project Management
- Create, retrieve, update, and delete projects  
- Get all tasks linked to a specific project

### Task–Project Association
- Link or unlink tasks to/from projects  
- A task can belong to **only one project**  
- Prevent linking/unlinking tasks from **completed projects**

### Business Rules
- **Deadline Constraints:**
  - A task's deadline cannot exceed the project's deadline.  
  - If a project’s deadline is shortened, associated task deadlines are adjusted accordingly.
- **Completion Lifecycle:**
  - A project can only be completed if **all tasks** are completed.  
  - Reopening a completed task reopens its project.  
  - Configurable auto-complete behavior when the last open task is finished.

### Logging / Notifications (Optional)
- Logs when a task is marked completed  
- Logs warnings for tasks nearing their deadline (<24h)

---

## Continuous Integration (CI) with GitHub Actions
To automate testing and code quality checks, this project includes a GitHub Actions workflow that:

> Runs on every pull request and push
- Installs Python 3.11 and Poetry
- Installs dependencies
- Runs pre-commit hooks for linting/formatting checks
- Executes the test suite with pytest

## Tech Stack

- **FastAPI** – async web framework for the API layer  
- **Domain-Driven Design (DDD)** architecture  
- **Dependency Injection** – via `dependency-injector`  
- **SQLAlchemy** – ORM with **SQLite** backend  
- **Poetry** – dependency & virtual environment management  
- **Pre-commit hooks** – code quality checks  
- **Docker Compose** – containerized setup for easy deployment  
- **Swagger / OpenAPI** – interactive API docs at `/docs`

---

## Dependency Management (Poetry)

This project uses [Poetry](https://python-poetry.org/) for dependency management and virtual environments.

```bash
poetry install --no-root
```

## Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to automate code quality checks and enforce best practices before commits.
