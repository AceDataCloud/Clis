FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY nanobanana_cli/ nanobanana_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["nano-banana-cli"]
