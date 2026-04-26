FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY deepseek_cli/ deepseek_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["deepseek-cli"]
