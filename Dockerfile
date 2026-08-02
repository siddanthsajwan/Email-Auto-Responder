# Use lightweight official Python 3.12 slim image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

# Install uv for fast, reliable package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project specification files first for caching dependencies
COPY crewAI-examples/flows/email_auto_responder_flow/pyproject.toml \
     crewAI-examples/flows/email_auto_responder_flow/uv.lock \
     /app/crewAI-examples/flows/email_auto_responder_flow/

WORKDIR /app/crewAI-examples/flows/email_auto_responder_flow

# Install dependencies without building the package yet
RUN uv sync --frozen --no-install-project --no-cache

# Copy the full application source code
COPY crewAI-examples/flows/email_auto_responder_flow /app/crewAI-examples/flows/email_auto_responder_flow

# Install the editable project
RUN uv sync --frozen --no-cache

# Expose default port
EXPOSE 10000

# Default command to start the continuous email auto-responder flow and health dashboard
CMD ["uv", "run", "kickoff"]
