FROM python:3.9-slim

WORKDIR /app

# Copy only the requirements file
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files to the container
COPY main.py .

# Expose the port the app runs on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "main.py"]