# Use lightweight official Python 3.12 slim image
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies without root project
RUN uv sync --frozen --no-install-project --no-cache

# Copy source code
COPY . .

# Install project
RUN uv sync --frozen --no-cache

EXPOSE 10000

# Run the flow
CMD ["uv", "run", "kickoff"]
