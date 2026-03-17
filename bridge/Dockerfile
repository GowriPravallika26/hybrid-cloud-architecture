# bridge/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy all files from bridge/ to /app in container
COPY . /app

# Install required Python packages
RUN pip install --default-timeout=1000 --no-cache-dir \
    boto3 \
    google-cloud-storage \
    google-cloud-secret-manager \
    requests \
    mysql-connector-python  # if you want Cloud SQL connection

# AWS LocalStack endpoint
ENV AWS_ENDPOINT_URL=http://localstack:4566

# Run main.py
CMD ["python", "main.py"]

