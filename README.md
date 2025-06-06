# Containerized 3-Tier Application

## Purpose

This project provides a lightweight, realistic 3-tier application that demonstrates a common enterprise architecture pattern. It was originally designed for VM-based deployment for demonstrations and customer use cases in multi-cloud environments, and has now been containerized for easier deployment and testing.

The application is a simple employee management system with a responsive web interface that allows you to view, add, edit, and delete employee records.

## Application Structure

This is a 3-tier application with:
- **Database tier**: MongoDB with FastAPI backend for data access
- **Application tier**: Flask application serving as middleware
- **Client tier**: Browser interface accessing the Flask application

## Technology Stack

### Database Container
- **Base Image**: Ubuntu 22.04
- **Database**: MongoDB
- **API**: FastAPI with async MongoDB driver
- **Web Server**: Nginx + Gunicorn + Uvicorn

### Application Container
- **Base Image**: Alpine Linux 3.17
- **Application Server**: Flask
- **Web Server**: Nginx + Gunicorn
- **Frontend**: HTML5 + CSS + jQuery

## Docker Containerization

The application has been containerized using Docker and Docker Compose, making it easy to deploy and test regardless of the host environment.

### Container Architecture
- **db-vm**: MongoDB database with FastAPI backend
- **app-vm**: Flask application server
- **Networking**: Custom Docker network for inter-container communication
- **Persistence**: Docker volume for MongoDB data

## How to Run with Docker

1. Ensure Docker and Docker Compose are installed on your machine.

2. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/demo-3-tier-app.git
   cd demo-3-tier-app
   ```

3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

4. Access the application:
   - Flask Application UI: http://localhost:8080
   - FastAPI Database Service: http://localhost:8081
   - API Documentation (Swagger UI): http://localhost:8081/docs

5. To stop the application:
   ```bash
   docker-compose down
   ```

## API Operations

The FastAPI backend supports the following operations:

```
GET /employee/: List all employees
GET /employee/{emp_id}: Get an employee by ID
POST /employee/: Create a new employee record
PUT /employee/{emp_id}: Update an employee record
DELETE /employee/{emp_id}: Delete an employee record
```

## Data Structure

The employee database has the following schema:
- `emp_id`: int (unique)
- `first_name`: str
- `last_name`: str
- `email`: str
- `ph_no`: str
- `home_addr`: str
- `st_addr`: str
- `gender`: str
- `job_type`: str

## Troubleshooting

If you encounter issues with the containers:

1. Check container status:
   ```bash
   docker-compose ps
   ```

2. View container logs:
   ```bash
   docker-compose logs database
   docker-compose logs app
   ```

3. Reset the application (including data):
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

## Screenshots

**Application UI**

![App Screenshots](https://user-images.githubusercontent.com/11576892/226115529-2eec25bd-1746-47f1-a7f3-4c92d2f8fb5e.gif)

**API Documentation**

![Documentation](https://user-images.githubusercontent.com/11576892/226115519-5c1baf4e-f780-4217-932f-37c3aa1058db.gif)

## Contributing

Feel free to use and modify this application as needed. If you have questions or suggestions, please open an issue or pull request.

## Credits

This application is based on the repository: [@sajaldebnath/demo-3-tier-app](https://github.com/sajaldebnath/demo-3-tier-app)

## License

This project is available under the MIT License. See the LICENSE file for details.
