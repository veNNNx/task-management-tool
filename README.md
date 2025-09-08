# Task manager tool
## Project info
Some changes during implementation:
- A task's deadline cannot be earlier than the current time.
- Completed tasks cannot be marked completed again (uncompletion has a separate endpoint).
- When linking a task to a project, if the task’s deadline exceeds the project’s deadline, it will be shortened to match the project.
- A task cannot have a deadline later than the project it belongs to (in task create).
- Tasks cannot be linked or unlinked from a project that is already completed.

## Dependency Management (Poetry)

This project uses [Poetry](https://python-poetry.org/) for dependency and virtual environment management.

## Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to automate code quality checks and enforce best practices before commits.

## Run with Docker

```bash
# Build the Docker image
docker compose build

# Start the backend service
docker compose up
```

## Swagger / API Documentation

Interactive API documentation is available via Swagger at:

http://localhost:8000/docs
