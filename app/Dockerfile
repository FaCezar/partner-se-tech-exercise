
# Build stage


FROM cgr.dev/chainguard/python:latest-dev AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN python -m venv /app/venv

ENV PATH="/app/venv/bin:${PATH}"


COPY requirements.txt /app/

RUN --mount=type=secret,id=pip_config,target=/run/secrets/pip.conf \
    PIP_CONFIG_FILE=/run/secrets/pip.conf \
    pip install \
        --no-cache-dir \
        --requirement /app/requirements.txt

COPY . /app


# Runtime stage


FROM cgr.dev/chainguard/python:latest

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:${PATH}"

# Copy only what is required to run the application
COPY --from=builder /app/venv /app/venv
COPY --from=builder /app /app

EXPOSE 8000

ENTRYPOINT ["python", "/app/app.py"]
