FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE CHANGELOG.md ./
COPY adc_cli/ ./adc_cli/
COPY tests/ ./tests/

RUN pip install --no-cache-dir -e ".[all]"

RUN ruff check . && ruff format --check .
RUN pytest tests/ -v --ignore=tests/test_integration.py

ENTRYPOINT ["adc"]
