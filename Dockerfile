# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
# RUN pip install uv
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY datetime_server.py .

# Expose the port (default 8000)
EXPOSE 8000

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=8000

# Run the application
CMD ["python", "datetime_server.py"] 