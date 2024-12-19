# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variable for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY src/ ./src/
COPY run.py .

# Create necessary directories
RUN mkdir -p text processed chroma_db
RUN chmod -R 777 text processed chroma_db

# Expose the port Gradio will run on
EXPOSE 7860

# Set environment variables
ENV PYTHONPATH=/app
ENV GOOGLE_API_KEY=""

# Create entrypoint script
RUN echo '#!/bin/bash\n\
if [ -z "$GOOGLE_API_KEY" ]; then\n\
    echo "Error: GOOGLE_API_KEY environment variable is required"\n\
    exit 1\n\
fi\n\
exec python run.py' > /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

# Set the entry point
ENTRYPOINT ["/app/entrypoint.sh"]
