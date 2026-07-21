
# Build stage

FROM cgr.dev/chainguard/python:latest-dev AS builder

ENV LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app


RUN python -m venv /venv

ENV PATH="/venv/bin:${PATH}"


COPY requirements.txt /app/requirements.txt


RUN --mount=type=secret,id=pip_config,target=/run/secrets/pip.conf \
    PIP_CONFIG_FILE=/run/secrets/pip.conf \
    pip install \
        --no-cache-dir \
        --requirement /app/requirements.txt


COPY . /app


# Runtime stage

FROM cgr.dev/chainguard/python:latest

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:${PATH}"

WORKDIR /app


COPY --from=builder --chown=65532:65532 /venv /venv
COPY --from=builder --chown=65532:65532 /app /app

EXPOSE 8000

# Explicitly run as Chainguard's non-root user.
USER 65532:65532

ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-", "app:app"]
