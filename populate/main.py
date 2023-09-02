import boto3
from datetime import date, timedelta

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Tasks')

# Define a list of tasks
tasks = [
    "Complete Assignment",
    "Go for a Run",
    "Read a Book",
    "Learn a New Skill",
    "Watch a Movie",
    "Cook a New Recipe",
    "Visit a Friend",
    "Meditate",
    "Write a Blog",
    "Go Shopping",
    "Clean the House",
    "Do Gardening",
    "Go Hiking",
    "Visit a Museum",
    "Listen to a Podcast",
    "Do Yoga",
    "Go Swimming",
    "Visit Family",
    "Work on a Side Project",
    "Play a Musical Instrument",
    "Go to a Social Event",
    "Go for a Long Drive",
    "Attend a Workshop",
    "Go Fishing",
    "Take a Day Off",
    "Go to the Gym",
    "Solve Puzzles",
    "Play Video Games",
    "Go Biking",
    "Do Some Painting"
]

# Generate dates for the next month
today = date.today()
dates_for_next_month = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]

# Populate the table
for i in range(30):
    table.put_item(
        Item={
            'date': dates_for_next_month[i],
            'task': tasks[i]
        }
    )
