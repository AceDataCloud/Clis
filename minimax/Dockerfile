FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY minimax_cli/ minimax_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["minimax-cli"]
