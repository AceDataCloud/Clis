FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY kling_cli/ kling_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["kling-cli"]
