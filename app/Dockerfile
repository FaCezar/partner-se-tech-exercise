# syntax=docker/dockerfile:1.7

# ============================================================
# Build stage
# ============================================================
FROM cgr.dev/chainguard/python:latest-dev AS builder

ENV LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Keep dependencies separate from the application directory.
RUN python -m venv /venv

ENV PATH="/venv/bin:${PATH}"

# Copy dependency metadata separately for build caching.
COPY requirements.txt /app/requirements.txt

# Use Chainguard Libraries through an ephemeral BuildKit secret.
RUN --mount=type=secret,id=pip_config,target=/run/secrets/pip.conf \
    PIP_CONFIG_FILE=/run/secrets/pip.conf \
    pip install \
        --no-cache-dir \
        --requirement /app/requirements.txt

# Copy application source only after dependency installation.
COPY . /app

# ============================================================
# Runtime stage
# ============================================================
FROM cgr.dev/chainguard/python:latest

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:${PATH}"

WORKDIR /app

# Copy only the virtual environment and application required at runtime.
COPY --from=builder --chown=65532:65532 /venv /venv
COPY --from=builder --chown=65532:65532 /app /app

EXPOSE 8000

# Explicitly run as Chainguard's non-root user.
USER 65532:65532

ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-", "app:app"]
