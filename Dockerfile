FROM python:3.11-slim

# System deps with cleanup
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

# Copy CODE first for better caching
COPY wsgi.py .
COPY service/ ./service/

# Copy dependencies LAST
COPY Pipfile Pipfile.lock ./

# Install with no cache
RUN pip install --no-cache-dir --upgrade pip pipenv && \
    pipenv install --system --deploy && \
    pip install --no-cache-dir psycopg2-binary

# Non-root setup
RUN chmod 777 /app  # 👈 Temp permissions fix
USER 1001

EXPOSE 8080
ENTRYPOINT ["gunicorn"]
CMD ["--log-level=info", "wsgi:app"]
