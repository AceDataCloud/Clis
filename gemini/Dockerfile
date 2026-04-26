FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY gemini_cli/ gemini_cli/
RUN pip install --no-cache-dir .
ENTRYPOINT ["gemini-cli"]
