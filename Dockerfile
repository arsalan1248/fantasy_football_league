# Base image
FROM python:3.12-slim-bookworm

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /apps

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        dos2unix \
        build-essential \
        libpq-dev \
        netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /apps/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . /apps/

# Make entrypoint executable
RUN chmod +x /apps/entrypoint.sh \
    && dos2unix /apps/entrypoint.sh \
    && echo "[INFO] Converted entrypoint.sh to LF and made it executable"

# Expose port
EXPOSE 8000

# Use entrypoint for DB wait, migrations, static files
ENTRYPOINT ["/apps/entrypoint.sh"]

# Default CMD: production Gunicorn server
CMD ["gunicorn", "fantasy_football_league.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--log-level", "info"]
