FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY fish_cli/ fish_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["fish-cli"]
