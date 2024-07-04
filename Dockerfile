# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install PostgreSQL dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure the static files are collected
RUN python manage.py collectstatic --noinput

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=mydataroom.settings

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mydataroom.wsgi:application"]
