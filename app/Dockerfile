# Build stage: possui shell e ferramentas de desenvolvimento
FROM cgr.dev/chainguard/python:3.11-dev AS builder

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /app/venv \
    && /app/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . /app


# Runtime stage: mínimo e distroless
FROM cgr.dev/chainguard/python:latest

WORKDIR /app

COPY --from=builder /app /app

ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["/app/venv/bin/python", "/app/app.py"]
