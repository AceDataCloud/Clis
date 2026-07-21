FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY midjourney_cli/ midjourney_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["midjourney-cli"]
