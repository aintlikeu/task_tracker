# First stage: build with the full Python image
FROM python:3.11 as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create and set the working directory
WORKDIR /task_tracker/

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Second stage: create the final image with Python slim
FROM python:3.11-slim

# Copy the environment variables from the first stage
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy the installed dependencies and the application code from the first stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /task_tracker /task_tracker

# Set the working directory
WORKDIR /task_tracker

# Copy the example configuration file
RUN cp task_tracker/config.example.yaml task_tracker/config.yaml

# Run migrations
RUN python task_tracker/manage.py migrate

# Set the command to run the application
CMD ["python", "task_tracker/manage.py", "runserver", "0.0.0.0:8000"]

# Expose the port used by the application
EXPOSE 8000