FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    gnupg \
    curl \
    python3 \
    python3-pip \
    nginx \
    supervisor \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Add MongoDB keys and repository
RUN curl -fsSL https://pgp.mongodb.com/server-6.0.asc | gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor \
    && echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list \
    && apt-get update \
    && apt-get install -y mongodb-org curl \
    && mkdir -p /data/db \
    && chmod 777 /data/db

# Copy application files
WORKDIR /home/app/employee_db
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Setup directories
RUN mkdir -p /home/app/employee_db/run /home/app/employee_db/logs

# Configure Nginx
RUN rm /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/sites-available/fastapi-mongodb-app
RUN ln -s /etc/nginx/sites-available/fastapi-mongodb-app /etc/nginx/sites-enabled/

# Update nginx.conf to use app user instead of www-data
RUN sed -i 's/user www-data;/user root;/' /etc/nginx/nginx.conf

# Copy supervisor configuration
COPY supervisor.conf /etc/supervisor/conf.d/fastapi-mongodb-app.conf

# Make gunicorn.start executable
RUN chmod +x /home/app/employee_db/gunicorn.start

# Make healthcheck script executable
RUN chmod +x /home/app/employee_db/healthcheck.sh

# Expose port 80
EXPOSE 80

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run entrypoint script
ENTRYPOINT ["/entrypoint.sh"] 