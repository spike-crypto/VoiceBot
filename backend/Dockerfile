# Use Python 3.10 (stable and compatible)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for audio processing if any)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create uploads directory
RUN mkdir -p app/uploads && chmod 777 app/uploads

# Expose port 7860 (Hugging Face default)
EXPOSE 7860

# Set environment variables
ENV FLASK_APP=run.py
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "run.py"]
