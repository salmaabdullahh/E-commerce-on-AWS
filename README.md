# Assignment 2 – Event-Driven Order Notification System

This project implements a serverless, event-driven backend system for processing e-commerce orders using AWS services. The system automatically stores new orders and sends out notifications using SNS, SQS, Lambda, and DynamoDB — fully deployed via CloudFormation.

## 📦 Architecture Overview

- **Amazon SNS** (`OrderTopic`): Receives order events
- **Amazon SQS** (`OrderQueue`): Buffers events
- **Amazon SQS DLQ** (`OrderDLQ`): Handles failed messages after 3 tries
- **AWS Lambda** (`OrderFunction`): Parses the message and stores data in DynamoDB
- **Amazon DynamoDB** (`Orders`): Stores order data

## 🏗️ Stack Deployment (CloudFormation)

To deploy the full architecture:

1. Save `template.yaml` from this repo
2. Go to AWS Console → CloudFormation → Create Stack → Upload `template.yaml`
3. Launch and monitor stack creation

## 🔧 Lambda Function Behavior

The `OrderProcessor` Lambda:
- Triggers from `OrderQueue`
- Parses each message (JSON)
- Writes order to DynamoDB
- Logs the process using CloudWatch

### Example Input (SNS Message Body):

```json
{
  "orderId": "O1234",
  "userId": "U123",
  "itemName": "Laptop",
  "quantity": 1,
  "status": "new",
  "timestamp": "2025-05-07T12:00:00Z"
}

``````
🔐 IAM Permissions
The Lambda role includes:

dynamodb:PutItem for writing orders

sqs:ReceiveMessage, DeleteMessage, GetQueueAttributes

Logging with logs:*

🧪 Testing
After deployment:

Go to SNS → OrderTopic → Publish a message

Confirm the message is:

Sent to SQS

Processed by Lambda

Stored in DynamoDB

View logs in CloudWatch

🎯 Bonus: CloudFormation Deployment
This assignment is deployed entirely using AWS CloudFormation. The template.yaml defines:

SNS topic

SQS queue + DLQ

DynamoDB table

Lambda function and permissions

Event source mappings (SQS → Lambda)

🧠 DLQ & Visibility Timeout Explanation
✅ What is a DLQ?
A Dead-Letter Queue is a backup queue for messages that can't be processed successfully. In this assignment:

DLQ Name: OrderDLQ

MaxReceiveCount: 3

After 3 failed Lambda attempts to process a message, it moves to the DLQ. This prevents infinite retries and helps with debugging.

⏱️ What is Visibility Timeout?
The visibility timeout temporarily hides a message after a consumer (like Lambda) retrieves it. If the Lambda doesn’t successfully delete it before the timeout expires, the message becomes visible again for retry.

🔄 Why It Matters
Together, DLQ and visibility timeout:

Ensure that failed messages are handled separately

Prevent duplicate processing

Improve reliability and observability in serverless architectures
