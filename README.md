# hybrid-cloud-architecture


## Overview

This project implements a **Hybrid Cloud Data Pipeline** that transfers files from an **AWS S3 bucket (simulated using LocalStack)** to **Google Cloud Storage (GCS)**.

A **Flask-based microservice** acts as the bridge between AWS and Google Cloud. When the API endpoint is triggered, the service retrieves a file from the S3 bucket and uploads it to the specified GCS bucket.

This project demonstrates **cross-cloud integration** using containerized services and cloud storage platforms.

---

# Architecture

The system consists of three main components:

1. **LocalStack (AWS Simulation)**
   - Simulates AWS services locally
   - Used to create and manage an S3 bucket

2. **Flask Microservice**
   - Exposes an API endpoint `/trigger-pipeline`
   - Downloads files from S3
   - Uploads files to Google Cloud Storage

3. **Google Cloud Storage**
   - Stores the final transferred file

---

# Architecture Diagram
+--------------------+
|  LocalStack (S3)   |
|   test-bucket      |
+---------+----------+
          |
          | File Download
          |
+---------v----------+
|  Flask Microservice|
|   /trigger-pipeline|
+---------+----------+
          |
          | File Upload
          |
+---------v----------+
| Google Cloud       |
| Storage Bucket     |
| padma-hybrid-bucket|
+--------------------+

The file flow is:

1. A file is uploaded to **LocalStack S3** 
2. The **Flask API endpoint** is triggered 
3. The service downloads the file from S3 
4. The file is uploaded to **Google Cloud Storage**

---

# Technologies Used

- Python
- Flask
- Docker
- Docker Compose
- LocalStack
- AWS CLI
- Google Cloud SDK
- Google Cloud Storage
- Terraform

---

# Environment Variables

The project uses environment variables for AWS and GCP configuration.

Example `.env.example`:

GCP Configuration

GCP_PROJECT_ID="cloudarchitecture-491104"
GCP_REGION="us-central1"

AWS / LocalStack Configuration

AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
AWS_DEFAULT_REGION=us-east-1
AWS_ENDPOINT_URL=http://localhost:4566


---

# Setup Instructions

## 1 Start LocalStack

From the project root directory run:


docker-compose up


This starts the **LocalStack container** which simulates AWS services locally.

---

# 2 Create an S3 Bucket

Use AWS CLI with the LocalStack endpoint:


aws --endpoint-url=http://localhost:4566
 s3 mb s3://test-bucket


---

# 3 Upload a Test File

Upload a sample file to the S3 bucket.


aws --endpoint-url=http://localhost:4566
 s3 cp test.txt s3://test-bucket/


Verify upload:


aws --endpoint-url=http://localhost:4566
 s3 ls s3://test-bucket


Example output:


2026-03-06 test.txt


---

# 4 Run the Flask Microservice

Navigate to the application directory:


cd app


Run the service:


python app.py


The service will start at:


http://localhost:8080


---

# API Documentation

## POST /trigger-pipeline

This endpoint triggers the data pipeline that transfers a file from **S3 to Google Cloud Storage**.

### Request


POST /trigger-pipeline


Request body:


{
"s3_object_key": "test.txt"
}


### Response


{
"status": "File transferred"
}


### Description

The API receives the S3 object key, downloads the file from the LocalStack S3 bucket, and uploads it to the configured Google Cloud Storage bucket.

---

# Trigger the Pipeline

Run the following command:


curl -X POST http://localhost:8080/trigger-pipeline

-H "Content-Type: application/json"
-d '{"s3_object_key":"test.txt"}'


Expected output:


{"status":"File transferred"}


---

# Verify File Transfer

Check whether the file appears in the Google Cloud Storage bucket.


gsutil ls gs://pravallika-hybrid-bucket-2026


Example output:


gs://pravallika-hybrid-bucket-2026/test.txt


This confirms the **successful transfer from S3 to GCS**.

---

# Infrastructure with Terraform

Terraform configuration files are located in the **terraform/** directory.

Initialize Terraform:


cd terraform
terraform init


Apply configuration:


terraform apply


This creates and manages the necessary cloud resources.

---

# Testing

The pipeline was tested by:

1. Uploading `test.txt` to the **LocalStack S3 bucket**
2. Triggering the **Flask API endpoint**
3. Verifying the file appeared in **Google Cloud Storage**

The successful presence of the file in GCS confirms that the **pipeline works correctly**.

---

# Conclusion

This project demonstrates a **Hybrid Cloud Data Pipeline** integrating AWS and Google Cloud.

Using **LocalStack, Flask, Docker, and Google Cloud Storage**, the system successfully transfers files from an S3 bucket to a GCS bucket through a microservice API