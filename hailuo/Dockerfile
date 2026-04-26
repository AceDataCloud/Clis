FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY hailuo_cli/ hailuo_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["hailuo-cli"]
