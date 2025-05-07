# Order Notification System (Event-Driven Architecture)

This project implements a simple serverless order notification system using AWS services. It demonstrates an event-driven architecture where messages flow from SNS → SQS → Lambda → DynamoDB.

---

## 🧱 Architecture

**Services Used:**

- **Amazon DynamoDB**: Stores order records in a table named `Orders`.
- **Amazon SNS**: Publishes incoming order messages via the `OrderTopic`.
- **Amazon SQS**: Queue (`OrderQueue`) receives messages from SNS and triggers Lambda.
- **Amazon SQS DLQ**: `OrderDLQ` handles failed messages after 3 unsuccessful attempts.
- **AWS Lambda**: Processes messages from the queue and inserts them into DynamoDB.
- **IAM Role**: Pre-created role used by Lambda for permissions.

**Flow:**
1. An order message is published to the `OrderTopic`.
2. The topic sends the message to the `OrderQueue`.
3. The Lambda function is triggered by the SQS queue.
4. The function stores the message into the `Orders` DynamoDB table.

---

## ⚙️ Setup Instructions

### 1. Deploy CloudFormation Stack

- Upload the included `order-notification-system.json` to AWS CloudFormation.
- Navigate to **CloudFormation > Create Stack > With new resources (standard)**.
- Choose **Upload a template file** and select the JSON file.
- Click **Next** through the prompts and create the stack.

> Ensure the following resources already exist:
> - Lambda function: `OrderFunction`
> - IAM role: `service-role/OrderFunction-role-w0cq2m6w`

### 2. Manually Subscribe SQS Queue to SNS

> This step is manual unless added to CloudFormation.

- Go to **SNS > OrderTopic > Create subscription**
- Protocol: `Amazon SQS`
- Endpoint: ARN of the `OrderQueue`
- Confirm the subscription

---

## 🧪 Test Instructions

1. Go to **SNS > OrderTopic > Publish message**
2. Use the following test JSON:

```json
{
  "orderId": "O1234",
  "userId": "U123",
  "itemName": "Laptop",
  "quantity": 1,
  "status": "new",
  "timestamp": "2025-05-03T12:00:00Z"
}
