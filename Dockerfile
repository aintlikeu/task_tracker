# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=task_tracker.settings \
    PYTHONPATH=/app:/app/task_tracker

# Create and set the working directory
WORKDIR /app

# Copy only the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY task_tracker /app/task_tracker

# Copy the example configuration file
RUN cp /app/task_tracker/config.example.yaml /app/task_tracker/config.yaml

# Run migrations
RUN python /app/task_tracker/manage.py migrate

# Set the command to run the application
CMD ["python", "/app/task_tracker/manage.py", "runserver", "0.0.0.0:8000"]

# Expose the port used by the application
EXPOSE 8000