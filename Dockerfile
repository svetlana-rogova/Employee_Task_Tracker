FROM python:3.13-slim

WORKDIR /app

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

EXPOSE 8003

CMD ["python", "manage.py", "runserver", "0.0.0.0:8003"]
