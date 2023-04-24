import json
import boto3

# Initialize AWS clients
sns_client = boto3.client('sns')
dynamodb_client = boto3.client('dynamodb')

# Lambda handler function
def lambda_handler(event, context):
    # Extract data from the event object
    message = event['Records'][0]['SNS']['Message']
    
    # Process the message
    processed_message = process_message(message)
    
    # Store the processed message in DynamoDB
    store_message_in_dynamodb(processed_message)
    
    # Publish the processed message to another SNS topic
    sns_topic_arn = 'arn:aws:sns:us-east-1:123456789012:my-topic'
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=processed_message
    )
    
    # Return a response
    response = {
        'statusCode': 200,
        'body': json.dumps({'message': 'Serverless communication processed successfully'})
    }
    
    return response

# Function to process the message
def process_message(message):
    # Add custom processing logic here
    processed_message = "Processed: " + message
    return processed_message

# Function to store the message in DynamoDB
def store_message_in_dynamodb(message):
    # Create a unique ID for the message
    message_id = str(hash(message))
    
    # Store the message in DynamoDB
    dynamodb_client.put_item(
        TableName='my-table',
        Item={
            'MessageId': {'S': message_id},
            'Message': {'S': message}
        }
    )
