# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for pandas/numpy/pyarrow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Run the data pipeline to ensure data is available in the container
RUN python src/data/generate.py && \
    python src/data/clean.py && \
    python src/data/features.py && \
    python src/metrics/compute.py

# Make port 8050 available to the world outside this container
EXPOSE 8050

# Define environment variable for Dash to listen on all IPs
ENV DASH_PORT=8050
ENV HOST=0.0.0.0

# Run the app using gunicorn
# The -b 0.0.0.0:8050 flag tells gunicorn to listen on all interfaces
# src.viz.dashboard:server refers to the 'server' object in src/viz/dashboard.py
CMD ["gunicorn", "-b", "0.0.0.0:8050", "--timeout", "120", "src.viz.dashboard:server"]
