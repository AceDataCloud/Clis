FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY claude_cli/ claude_cli/
RUN pip install --no-cache-dir .
ENTRYPOINT ["claude-cli"]
