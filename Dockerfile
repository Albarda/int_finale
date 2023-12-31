# Use an official Python runtime as the base image
FROM python:3.9-slim

EXPOSE 80

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Define environment variable (Optional, you can set these variables from Fargate task definition as well)
ENV AWS_DEFAULT_REGION=eu-west-1

# Run main.py when the container is launched
CMD ["python", "main.py"]
