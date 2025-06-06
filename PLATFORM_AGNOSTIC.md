# Platform-Agnostic Deployment Guide

This application has been designed to be deployed on any container platform with minimal configuration changes. This guide outlines how to deploy the application on various platforms.

## Environment Variables

The application uses environment variables for all configuration, making it adaptable to any platform. Here are the key environment variables:

### Application Container

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | Hostname/IP for database service (internal) | `database` |
| `DB_PORT` | Port for database service | `80` |
| `API_PROTOCOL` | Protocol for API calls (http/https) | `http` |
| `DB_EXTERNAL_HOST` | External hostname/IP for API docs access | `localhost` |
| `DB_EXTERNAL_PORT` | External port for API docs access | `8081` |

### Database Container

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGO_HOST` | MongoDB host | `127.0.0.1` |
| `MONGO_PORT` | MongoDB port | `27017` |
| `MONGO_DB_NAME` | MongoDB database name | `employees_DB` |
| `MONGO_USERNAME` | MongoDB username (optional) | `` |
| `MONGO_PASSWORD` | MongoDB password (optional) | `` |

## Deployment on Different Platforms

### Docker Compose (Local Development)

```yaml
services:
  database:
    build:
      context: ./DB VM
    environment:
      - MONGO_HOST=127.0.0.1
      - MONGO_PORT=27017
    ports:
      - "8081:80"

  app:
    build:
      context: ./App VM
    environment:
      - DB_HOST=database
      - DB_EXTERNAL_HOST=localhost
      - DB_EXTERNAL_PORT=8081
    ports:
      - "8080:80"
```

### Kubernetes

```yaml
# Database Deployment and Service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: database
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: db-vm
        image: your-registry/db-vm:latest
        env:
        - name: MONGO_HOST
          value: mongodb-service
        - name: MONGO_PORT
          value: "27017"
---
# App Deployment and Service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: app-vm
        image: your-registry/app-vm:latest
        env:
        - name: DB_HOST
          value: database-service
        - name: DB_EXTERNAL_HOST
          value: api.example.com  # Your ingress or load balancer address
        - name: DB_EXTERNAL_PORT
          value: "80"  # External port, often 80 or 443 with ingress
```

### AWS ECS/Fargate

```json
{
  "containerDefinitions": [
    {
      "name": "database",
      "image": "your-registry/db-vm:latest",
      "environment": [
        { "name": "MONGO_HOST", "value": "your-mongodb-host.amazonaws.com" },
        { "name": "MONGO_PORT", "value": "27017" }
      ],
      "portMappings": [
        { "containerPort": 80, "hostPort": 80 }
      ]
    },
    {
      "name": "app",
      "image": "your-registry/app-vm:latest",
      "environment": [
        { "name": "DB_HOST", "value": "database.local" },
        { "name": "DB_EXTERNAL_HOST", "value": "your-load-balancer.region.elb.amazonaws.com" },
        { "name": "DB_EXTERNAL_PORT", "value": "80" }
      ],
      "portMappings": [
        { "containerPort": 80, "hostPort": 80 }
      ]
    }
  ]
}
```

### Google Cloud Run

```yaml
# Database service
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: database
spec:
  template:
    spec:
      containers:
      - image: your-registry/db-vm:latest
        env:
        - name: MONGO_HOST
          value: your-mongodb-host.region.firebasedatabase.app
        - name: MONGO_PORT
          value: "27017"
---
# App service
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: app
spec:
  template:
    spec:
      containers:
      - image: your-registry/app-vm:latest
        env:
        - name: DB_HOST
          value: database.run.app
        - name: DB_EXTERNAL_HOST
          value: database-xyz.run.app
        - name: DB_EXTERNAL_PORT
          value: "443"
```

## Security Considerations

1. **Database Authentication**: In production, always enable MongoDB authentication by setting `MONGO_USERNAME` and `MONGO_PASSWORD`.

2. **TLS/HTTPS**: For production, set `API_PROTOCOL` to `https` and ensure your ingress/load balancer provides TLS termination.

3. **Secrets Management**: Use your platform's secrets management:
   - Kubernetes: Use Secrets resources
   - AWS: Use AWS Secrets Manager or Parameter Store
   - GCP: Use Secret Manager
   - Azure: Use Key Vault

## Persistence

MongoDB data needs to be persisted across container restarts:

- **Docker Compose**: Uses named volume `db_data`
- **Kubernetes**: Use PersistentVolumeClaims
- **AWS ECS**: Use EFS volumes
- **GCP**: Use Persistent Disk or Filestore

## Network Considerations

1. **Container-to-Container Communication**: Uses internal service discovery:
   - Docker Compose: Service names (e.g., `database`)
   - Kubernetes: Service names (e.g., `database-service`)
   - AWS ECS: Service Discovery or task IPs

2. **External Access for API Documentation**:
   - Set `DB_EXTERNAL_HOST` and `DB_EXTERNAL_PORT` to values that are accessible from a user's browser
   - This might be an ingress hostname, load balancer address, or public IP

## Scaling Considerations

The database container contains both MongoDB and FastAPI. In a production environment, consider:

1. Separating MongoDB into its own deployment/service
2. Using a managed MongoDB service (Atlas, AWS DocumentDB, etc.)
3. Configuring connection pooling for MongoDB 