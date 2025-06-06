# Containerized 3-Tier Application

This guide shows how to containerize and run the 3-tier application using Docker and Docker Compose.

## Prerequisites

- Docker installed on your machine
- Docker Compose installed on your machine

## Project Structure

The application consists of two main components:
- Database VM: MongoDB with FastAPI backend
- App VM: Flask application serving as middleware

## Steps to Run the Application

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd demo-3-tier-app
   ```

2. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

   This will:
   - Build the database container with MongoDB and FastAPI
   - Build the application container with Flask
   - Set up networking between containers
   - Import the sample data into MongoDB

3. Access the application:
   - The Flask application is accessible at: http://localhost:8080
   - The FastAPI backend is accessible at: http://localhost:8081
   - The FastAPI Swagger UI is accessible at: http://localhost:8081/docs

4. To stop the application:
   ```bash
   docker-compose down
   ```

## Customization

- Database configuration: The database is pre-configured with sample employee data.
- App configuration: The Flask app connects to the database service automatically.

## Troubleshooting

- If you encounter connection issues, ensure both containers are running:
  ```bash
  docker-compose ps
  ```

- Check container logs:
  ```bash
  docker-compose logs database
  docker-compose logs app
  ```

- If the database container isn't healthy, you may need to wait a bit longer for MongoDB to initialize.

## Data Persistence

MongoDB data is persisted using a Docker volume (`db_data`). This ensures your data remains intact even if containers are removed.

To reset the data, remove the volume:
```bash
docker-compose down -v
``` 