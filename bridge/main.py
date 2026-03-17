import boto3
import time
import os

print("Starting Hybrid Bridge...", flush=True)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localstack:4566")

print("Connecting to SQS...", flush=True)

sqs = boto3.client(
    "sqs",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
    endpoint_url=AWS_ENDPOINT_URL
)

queue_name = "test-queue"

while True:
    try:
        response = sqs.create_queue(QueueName=queue_name)
        queue_url = response["QueueUrl"]
        print("Queue ready:", queue_url, flush=True)
        break
    except Exception as e:
        print("Waiting for SQS...", e, flush=True)
        time.sleep(2)

print("Listening for messages...", flush=True)

while True:
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=5
    )

    messages = response.get("Messages", [])

    if messages:
        for msg in messages:
            print("Received message:", msg["Body"], flush=True)
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=msg["ReceiptHandle"]
            )

    time.sleep(2)

