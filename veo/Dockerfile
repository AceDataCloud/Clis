FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY veo_cli/ veo_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["veo-cli"]
