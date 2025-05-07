import json
import boto3
import logging
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
orders_table = dynamodb.Table('Orders')

def lambda_handler(event, context):
    for record in event['Records']:
        try:
            # Get the message body and parse it as JSON
            message = json.loads(record['body'])
            
            # Log the received message
            logger.info(f"Received message: {message}")
            
            # Write the message to DynamoDB
            orders_table.put_item(Item={
                'orderId': message['orderId'],
                'userId': message['userId'],
                'itemName': message['itemName'],
                'quantity': int(message['quantity']),
                'status': message['status'],
                'timestamp': message['timestamp']
            })
            
            logger.info(f"Order {message['orderId']} inserted into DynamoDB.")
        
        except (KeyError, ValueError, ClientError) as e:
            logger.error(f"Failed to process record: {record}")
            logger.error(str(e))
            # Optionally, raise an exception to send the message to the DLQ
            raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Processed all messages.')
    }
