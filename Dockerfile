# Base image
FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install required packages
RUN apt-get update && apt-get install -y \
    nginx \
    certbot \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Configure Nginx
COPY nginx/default /etc/nginx/sites-available/default

# Apply Let's Encrypt SSL certificate
RUN certbot --nginx

# Run Django and Nginx
CMD ["/bin/bash", "./entrypoint.sh"]
