FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY seedance_cli/ seedance_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["seedance-cli"]
