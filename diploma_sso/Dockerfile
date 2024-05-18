FROM docker:latest as docker

FROM python:3.12-slim

COPY --from=docker /usr/local/bin/docker /usr/local/bin/

ENV PIP_TIMEOUT=30

WORKDIR /app
COPY poetry.lock .
COPY pyproject.toml .
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install
COPY . .
ENV USE_WSGI=0