FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY grok_cli/ grok_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["grok-cli"]
