FROM python:3.12-slim

WORKDIR /app

# Install curl (needed for health check)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files to the container
COPY main.py .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]