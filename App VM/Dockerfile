FROM alpine:3.17

# Install dependencies
RUN apk add --no-cache python3 py3-pip py3-gunicorn nginx supervisor

# Create app directory
WORKDIR /app

# Copy application files
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Setup directories
RUN mkdir -p /app/logs /run/nginx

# Configure nginx
COPY nginx.conf /etc/nginx/http.d/default.conf
RUN sed -i 's/user nginx;/user root;/' /etc/nginx/nginx.conf

# Make gunicorn start script executable
RUN chmod +x /app/gunicorn.start

# Expose port
EXPOSE 80

# Create entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"] 
