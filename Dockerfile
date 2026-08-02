# Use lightweight official Python 3.12 slim image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

# Install uv for fast, reliable package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project specification files first to leverage Docker layer caching
COPY crewAI-examples/flows/email_auto_responder_flow/pyproject.toml \
     crewAI-examples/flows/email_auto_responder_flow/uv.lock \
     /app/crewAI-examples/flows/email_auto_responder_flow/

# Install dependencies
WORKDIR /app/crewAI-examples/flows/email_auto_responder_flow
RUN uv sync --frozen --no-cache

# Copy the application source code
COPY crewAI-examples/flows/email_auto_responder_flow /app/crewAI-examples/flows/email_auto_responder_flow

# Default command to start the continuous email auto-responder flow
CMD ["uv", "run", "kickoff"]
