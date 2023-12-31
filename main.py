import boto3
from datetime import date

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Tasks')

# Get today's task
today = date.today().strftime('%Y-%m-%d')  # Format date as a string, if needed
response = table.get_item(
    Key={
        'date': today  # Assumes the date is the primary key
    }
)

task = response.get('Item', {}).get('task', 'No task found')

# Send SNS Notification
sns = boto3.client('sns')
topic_arn = "arn:aws:sns:eu-west-1:704059047372:db-app"
message = f"Task for {today}: {task}"
sns.publish(TopicArn=topic_arn, Message=message)
