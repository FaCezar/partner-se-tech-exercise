# Build stage
FROM cgr.dev/chainguard/python:3.12-dev AS builder

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /app/venv \
    && /app/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . /app

#Run stage
FROM cgr.dev/chainguard/python:3.12

WORKDIR /app

COPY --from=builder /app /app

ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["/app/venv/bin/python", "/app/app.py"]
