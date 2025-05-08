# Use an official Python runtime as the base image
FROM python:3.9-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libodbc1 \
    unixodbc \
    && rm -rf /var/lib/apt/lists/*
# Set the working directory in the container
WORKDIR /app

# Copy the requirements file (if you have one)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Copy the rest of the application code
COPY . .

# Specify the command to run the app
CMD ["python", "app.py"]