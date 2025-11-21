# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Install the project into `/app`
WORKDIR /app

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy
ENV PYTHONUNBUFFERED=1

# Install Semgrep for security scanning
RUN apt-get update && \
    apt-get install -y curl && \
    pip install --no-cache-dir semgrep && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD . /app

# Install the project's dependencies using the lockfile and settings
RUN uv sync --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
RUN uv sync --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Expose the port
EXPOSE 8080

# Run adk web by default
ENTRYPOINT ["uv", "run", "adk", "web", "/app", "--host", "0.0.0.0", "--port", "8080"]