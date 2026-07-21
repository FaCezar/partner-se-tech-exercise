
# Builder

FROM cgr.dev/chainguard/python:latest-dev AS builder

ENV LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN python -m venv /app/venv

ENV PATH="/app/venv/bin:${PATH}"

COPY requirements.txt .

RUN --mount=type=secret,id=pip_config,target=/run/secrets/pip.conf \
    PIP_CONFIG_FILE=/run/secrets/pip.conf \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Runtime

FROM cgr.dev/chainguard/python:latest

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/venv/bin:${PATH}"

WORKDIR /app

COPY --from=builder --chown=65532:65532 /app /app

EXPOSE 8000

USER 65532:65532

ENTRYPOINT ["python"]
CMD ["app.py"]
