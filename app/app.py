from flask import Flask, request, jsonify
import boto3
import os
from google.cloud import storage

app = Flask(__name__)

# Resource names
SQS_QUEUE_NAME = "test-queue"
S3_BUCKET = "test-bucket"
GCS_BUCKET = "pravallika-hybrid-bucket-2026"

# LocalStack SQS client
sqs = boto3.client(
    "sqs",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# LocalStack S3 client
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# GCS client
gcs_client = storage.Client()


# ------------------------------------------------
# Endpoint 1 : Send message to SQS
# ------------------------------------------------
@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.json
    message = data.get("message")

    queue_url = sqs.get_queue_url(QueueName=SQS_QUEUE_NAME)["QueueUrl"]

    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message
    )

    return jsonify({"status": "Message sent"}), 202


# ------------------------------------------------
# Endpoint 2 : Transfer file from S3 → GCS
# ------------------------------------------------
@app.route("/trigger-pipeline", methods=["POST"])
def trigger_pipeline():
    data = request.json
    key = data.get("s3_object_key")

    # Local temporary file (Windows compatible)
    file_path = "temp_" + key

    # Download from LocalStack S3
    s3.download_file(S3_BUCKET, key, file_path)

    # Upload to Google Cloud Storage
    bucket = gcs_client.bucket(GCS_BUCKET)
    blob = bucket.blob(key)
    blob.upload_from_filename(file_path)

    return jsonify({"status": "File transferred"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

