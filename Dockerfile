FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl ca-certificates && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir uv && uv pip install -U "mcp[cli]" starlette uvicorn jinja2 python-dotenv openai anthropic pytz phonenumbers
COPY src ./src
COPY tools ./tools
ENV PYTHONPATH=/app/src
ENV GMCP_HTTP=1 GMCP_HTTP_HOST=0.0.0.0 GMCP_HTTP_PORT=8288
CMD ["python", "-m", "gmcp.main", "http"]