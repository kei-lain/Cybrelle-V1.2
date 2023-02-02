# Use an official Python image as the base image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose port 8000 for the Django development server
EXPOSE 8080

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
