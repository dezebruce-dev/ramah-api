# Dockerfile for Ramah API
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port (Railway will override with PORT env var)
EXPOSE 5000

# Start command
CMD ["python", "ramah_api_server.py"]
