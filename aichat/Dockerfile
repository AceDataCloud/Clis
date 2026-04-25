FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY aichat_cli/ aichat_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["aichat-cli"]
