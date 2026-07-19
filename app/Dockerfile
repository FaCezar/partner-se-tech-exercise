
# Build stage

FROM cgr.dev/chainguard/python:latest-dev AS builder

WORKDIR /app

COPY requirements.txt /app/

RUN python -m venv /app/venv \
    && /app/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

COPY . /app


# Runtime stage

FROM cgr.dev/chainguard/python:latest

WORKDIR /app

COPY --from=builder /app /app

ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/app/venv/bin/python", "/app/app.py"]
