FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY serp_cli/ serp_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["serp-cli"]
