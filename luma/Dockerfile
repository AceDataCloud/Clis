FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY luma_cli/ luma_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["luma-cli"]
