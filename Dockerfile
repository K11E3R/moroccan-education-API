FROM python:3.12-slim

WORKDIR /app

# Copy requirements from api directory
COPY api/requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set environment variables
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Set working directory to api
WORKDIR /app/api
