FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY kimi_cli/ kimi_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["kimi-cli"]
