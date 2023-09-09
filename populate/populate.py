"""
This module populates a DynamoDB table with tasks and dates for the next month.
"""

from datetime import date, timedelta
import boto3

# Initialize DynamoDB resource
dynamodb_resource = boto3.resource('dynamodb')
tasks_table = dynamodb_resource.Table('Tasks')

# Define a list of tasks
TASKS_LIST = [
    "Complete Assignment", "Go for a Run", "Read a Book", "Learn a New Skill",
    "Watch a Movie", "Cook a New Recipe", "Visit a Friend", "Meditate",
    "Write a Blog", "Go Shopping", "Clean the House", "Do Gardening",
    "Go Hiking", "Visit a Museum", "Listen to a Podcast", "Do Yoga",
    "Go Swimming", "Visit Family", "Work on a Side Project",
    "Play a Musical Instrument", "Go to a Social Event", "Go for a Long Drive",
    "Attend a Workshop", "Go Fishing", "Take a Day Off", "Go to the Gym",
    "Solve Puzzles", "Play Video Games", "Go Biking", "Do Some Painting"
]

# Generate dates for the next month
TODAY_DATE = date.today()
DATES_NEXT_MONTH = [(TODAY_DATE + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]

# Populate the table
for i in range(30):
    tasks_table.put_item(
        Item={
            'date': DATES_NEXT_MONTH[i],
            'task': TASKS_LIST[i]
        }
    )
