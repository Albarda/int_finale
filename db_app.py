import boto3
from datetime import date

# Initialize clients for DynamoDB and SNS
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# Get today's task from DynamoDB
table = dynamodb.Table('Tasks')
today = date.today().strftime('%Y-%m-%d')  # Format date as a string
response = table.get_item(Key={'Date': today})
task = response['Item']['Task']

# Send SNS Notification
topic_arn = "YOUR_SNS_TOPIC_ARN"
message = f"Task for {today}: {task}"
sns.publish(TopicArn=topic_arn, Message=message)