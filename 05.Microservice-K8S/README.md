# Microservice Demo Application

A Flask-based microservice demonstration application with API documentation interface and sample implementations.

## Overview

This project demonstrates a simple microservice architecture using Flask and PostgreSQL. It includes:

- RESTful API endpoints for User, Product, and Order microservices
- Interactive API documentation interface
- Database integration with PostgreSQL
- Kubernetes deployment configuration

## Local Development

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python main.py
   ```

3. Access the application at http://localhost:5000

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster
- kubectl configured to connect to your cluster
- Docker registry to store the container image

### Build and Push Docker Image

1. Build the Docker image:
   ```
   docker build -t your-registry/microservice-demo:latest .
   ```

2. Push the image to your registry:
   ```
   docker push your-registry/microservice-demo:latest
   ```

### Deploy to Kubernetes

1. Create the namespace:
   ```
   kubectl apply -f k8s/namespace.yaml
   ```

2. Create ConfigMaps and Secrets:
   ```
   kubectl apply -f k8s/configmaps/app-config.yaml
   kubectl apply -f k8s/secrets/db-credentials.yaml
   ```

3. Create Persistent Volume and Persistent Volume Claim:
   ```
   kubectl apply -f k8s/volumes/postgres-pv.yaml
   ```

4. Deploy PostgreSQL:
   ```
   kubectl apply -f k8s/deployments/postgres.yaml
   ```

5. Deploy the Flask application:
   ```
   # Replace IMAGE_NAME and IMAGE_TAG with your actual values
   export IMAGE_NAME=your-registry/microservice-demo
   export IMAGE_TAG=latest
   envsubst < k8s/deployments/flask-app.yaml | kubectl apply -f -
   ```

6. Create the Ingress for external access:
   ```
   kubectl apply -f k8s/services/ingress.yaml
   ```

### Verify Deployment

Check if all pods are running:
```
kubectl get pods -n microservice-demo
```

## API Documentation

Access the API documentation by navigating to the application's root URL.

## Architecture

The application is structured as follows:

- `main.py`: Application entry point
- `app.py`: Flask application configuration
- `models.py`: Database models
- `routes.py`: API endpoints
- `services/`: Microservice implementations
- `static/`: Static assets (CSS, JavaScript)
- `templates/`: HTML templates
- `k8s/`: Kubernetes deployment files

## Database

The application uses PostgreSQL for data persistence. Sample data is available in `data.sql`.