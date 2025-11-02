FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app
WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN uv sync

CMD ["uv", "run", "cerebro.py"]
