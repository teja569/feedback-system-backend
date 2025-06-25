# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
