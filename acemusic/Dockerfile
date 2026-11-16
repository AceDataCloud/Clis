FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY acemusic_cli/ acemusic_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["acemusic-cli"]
