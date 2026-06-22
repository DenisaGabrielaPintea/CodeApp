# We are using an official Python image
FROM public.ecr.aws/docker/library/python:3.11-slim

# Set the working folder in the container
WORKDIR /app

# Copy the dependencies file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code (app.py)
COPY . .

# Expose port 5050
EXPOSE 5050

# Application startup command
CMD ["python", "app.py"]