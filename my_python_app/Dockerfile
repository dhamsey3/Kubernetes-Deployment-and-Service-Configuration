# Use an official Python runtime as a parent image
FROM python:3.9-slim AS base

# Set the working directory in the container
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt first for better caching
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Create and switch to a non-root user
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

# Expose port 5000 for the Flask application
EXPOSE 5000

# Run the application with Gunicorn when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers", "2"]
