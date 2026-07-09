FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY happyhorse_cli/ happyhorse_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["happyhorse-cli"]
