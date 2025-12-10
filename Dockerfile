ARG PYTHON_VERSION=3.12-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System dependencies for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Install Python packages
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/pip

# Copy project
COPY . /code

# Collect static files during build
# Set a dummy SECRET_KEY for collectstatic
ENV SECRET_KEY="dummy-key-for-collectstatic"
RUN python manage.py collectstatic --noinput --clear

# Use Gunicorn in production
CMD ["gunicorn", "mepunity.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120"]