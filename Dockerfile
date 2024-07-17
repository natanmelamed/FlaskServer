# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt and app.py into the container
COPY requirements.txt requirements.txt
COPY app.py app.py

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for the port
ENV PORT 5000

# Expose the port the app runs on
EXPOSE $PORT

# Run the application
CMD ["python", "app.py"]
