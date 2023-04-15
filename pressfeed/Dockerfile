ARG PYTHON_VERSION=3.10-slim-buster

# Use the official Python image as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app/

# Expose the port that the Django app will run on
EXPOSE 8000

# replace demo.wsgi with <project_name>.wsgi
CMD ["daphne", "pressfeed.asgi:application", "--bind", "0.0.0.0", "-p", "8000"]

