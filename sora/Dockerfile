FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY sora_cli/ sora_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["sora-cli"]
