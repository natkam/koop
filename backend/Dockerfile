FROM python:3.9

ENV POETRY_VERSION=1.1.5

WORKDIR /backend

RUN apt-get update -q && apt-get install -yq netcat
RUN pip install 'poetry==$POETRY_VERSION'

COPY poetry.lock pyproject.toml /backend/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root --no-asci
