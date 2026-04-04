FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY seedream_cli/ seedream_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["seedream-cli"]
