# 1. Fix Dockerfile — remove the collectstatic line completely
ARG PYTHON_VERSION=3.12-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/pip

COPY . /code

CMD ["gunicorn", "mepunity.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120"]
