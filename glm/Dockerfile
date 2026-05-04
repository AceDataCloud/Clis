FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY glm_cli/ glm_cli/

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["glm"]
