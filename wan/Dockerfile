FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY wan_cli/ wan_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["wan-cli"]
