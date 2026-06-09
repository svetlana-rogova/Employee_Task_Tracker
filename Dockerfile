FROM python 3.13-slim

WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
