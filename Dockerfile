FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root



COPY ./backend /app/backend
COPY ./api /app/api

ENV PORT 8000
EXPOSE 8000


CMD ["uvicorn", "api.api.root:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
