# Todo App — Full-Stack DevOps Project

A containerized full-stack To-Do application built with Python Flask and MySQL, deployed using Docker Compose and Nginx. This project demonstrates practical DevOps practices including containerization, multi-container orchestration, persistent storage, reverse proxy configuration, health checks, application logging, automated testing, security scanning, CI/CD, Docker Hub integration, and versioned Docker image releases.

## Project Overview

The application provides a simple To-Do management system where users can view To-Do tasks, add new tasks, mark tasks as completed, undo completed tasks, delete tasks, and check application health.

The application is deployed as a multi-container architecture using Docker Compose.

## Architecture

                         USER
                           |
                           | HTTP :8080
                           v
                   +---------------+
                   |     NGINX     |
                   | Reverse Proxy |
                   +-------+-------+
                           |
                           | HTTP :5000
                           v
                   +---------------+
                   |   FLASK APP   |
                   |    Python     |
                   +-------+-------+
                           |
                           | MySQL :3306
                           v
                   +---------------+
                   |     MYSQL     |
                   |     8.4       |
                   +-------+-------+
                           |
                           v
                   +---------------+
                   | Docker Volume |
                   |todo-mysql-data|
                   +---------------+

All application containers communicate through a custom Docker bridge network named todo-network.

## CI/CD Architecture

Developer
    |
    | git push
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +---------------------------+
    |                           |
    v                           v
 Test Job                  Docker Job
    |                           |
    +-- Flake8                  +-- Docker Login
    +-- Pytest                  +-- Build Image
    +-- pip-audit               +-- Trivy Scan
                                +-- Push Image
                                      |
                                      v
                                  Docker Hub
                                  |       |
                                  v       v
                                :v1.1   :latest

## Technology Stack

- Backend: Python Flask
- Database: MySQL 8.4
- Reverse Proxy: Nginx
- Containerization: Docker
- Orchestration: Docker Compose
- CI/CD: GitHub Actions
- Container Registry: Docker Hub
- Unit Testing: Pytest
- Code Quality: Flake8
- Dependency Security: pip-audit
- Container Security: Trivy
- Database Storage: Docker Volume
- Network: Docker Bridge Network

## Project Structure

todo-app/
├── app/
│   ├── app.py
│   ├── database.py
│   ├── static/
│   └── templates/
│       └── index.html
├── mysql/
│   └── init.sql
├── nginx/
│   └── nginx.conf
├── tests/
│   └── test_app.py
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
└── README.md

## Application Features

The application supports:

- Creating To-Do tasks
- Viewing To-Do tasks
- Completing tasks
- Undoing completed tasks
- Deleting tasks
- Application health monitoring
- Database connectivity verification
- Application logging

## Flask Application

The backend is implemented using Python Flask.

Main application file:

app/app.py

Database connection logic:

app/database.py

The application communicates with MySQL using mysql-connector-python.

The Flask application provides the following main routes:

GET /
POST /add
GET /complete/<todo_id>
GET /delete/<todo_id>
GET /health

## Environment Variables

The application uses environment variables for configuration.

Example configuration:

DB_HOST=mysql
DB_PORT=3306
DB_USER=todo_user
DB_PASSWORD=todo_password
DB_NAME=todo_db

MYSQL_ROOT_PASSWORD=root_password
MYSQL_DATABASE=todo_db
MYSQL_USER=todo_user
MYSQL_PASSWORD=todo_password

PORT=5000

The .env file contains environment-specific configuration and should not be committed to GitHub.

Sensitive credentials such as Docker Hub tokens must never be stored inside the source code or README.

## Dockerfile

The application is containerized using Docker.

The Docker image provides:

- Python runtime
- Python virtual environment
- Application dependencies
- Multi-stage build
- Non-root application user
- Health check
- Runtime configuration

The application runs as a non-root user named appuser.

Verify the container user:

docker run --rm sajinskaria/todo-app:v1.1 whoami

Expected output:

appuser

Running containers as a non-root user reduces the impact of a potential application compromise.

## Docker Compose

Docker Compose is used to run the complete application stack.

The Compose deployment contains three services:

- app
- mysql
- nginx

The Flask application listens internally on port 5000.

MySQL listens internally on port 3306.

Nginx is exposed to the host on port 8080.

The application can be accessed at:

http://localhost:8080

## Docker Network

The services communicate through a custom Docker bridge network:

todo-network

The Flask application connects to MySQL using:

DB_HOST=mysql
DB_PORT=3306

The hostname mysql refers to the MySQL Compose service.

MySQL does not need to expose port 3306 to the host because Flask communicates with it internally through the Docker network.

This provides better network isolation.

## Nginx Reverse Proxy

Nginx acts as the public entry point for the application.

Traffic flow:

Client
   |
   | :8080
   v
Nginx
   |
   | :5000
   v
Flask
   |
   | :3306
   v
MySQL

The Nginx configuration is located at:

nginx/nginx.conf

The Flask application is not directly exposed to the host in the Compose deployment.

## Persistent Database Storage

MySQL uses a Docker named volume:

todo-mysql-data

The volume is mounted at:

/var/lib/mysql

This ensures that database data survives container recreation.

View Docker volumes:

docker volume ls

Inspect the volume:

docker volume inspect todo-app_todo-mysql-data

The database volume should not be deleted during normal cleanup.

## Database Initialization

The database initialization script is located at:

mysql/init.sql

It creates the required database table structure when the MySQL database is initialized.

The application uses the todos table to store To-Do items.

## Health Checks

Health checks are configured for both the Flask application and MySQL.

### Application Health Check

The Flask application provides:

GET /health

A healthy application returns:

{
  "status": "healthy"
}

The health endpoint also verifies database connectivity.

Verify application health:

docker inspect --format='{{.State.Health.Status}}' todo-app

Expected:

healthy

### MySQL Health Check

MySQL is checked using mysqladmin ping.

Verify MySQL health:

docker inspect --format='{{.State.Health.Status}}' todo-mysql

Expected:

healthy

Health checks allow Docker Compose to determine whether dependent services are ready.

## Application Logging

The Flask application uses Python's logging module.

Logging levels include:

- INFO
- WARNING
- ERROR

The application logs events such as:

- Application startup
- Todo creation
- Todo updates
- Todo deletion
- Database connection failures
- Health-check results
- Application errors

Example:

INFO __main__: Health check successful

View application logs:

docker logs todo-app

View the latest logs:

docker logs todo-app --tail 20

Follow logs in real time:

docker logs -f todo-app

## MySQL Logging

MySQL logs database startup and server events.

View MySQL logs:

docker logs todo-mysql

Example:

MySQL Server - start.
mysqld: ready for connections.

## Running the Application

Start the complete application:

docker compose up -d --build

Check running services:

docker compose ps

The expected services are:

todo-app
todo-mysql
todo-nginx

Access the application:

http://localhost:8080

## Health Verification

Check the application through Nginx:

curl http://localhost:8080/health

Expected:

{
  "status": "healthy"
}

Check Flask container health:

docker inspect --format='{{.State.Health.Status}}' todo-app

Check MySQL container health:

docker inspect --format='{{.State.Health.Status}}' todo-mysql

Both should return:

healthy

## Testing

The project uses Pytest for automated testing.

Run the test suite:

pytest

Expected result:

5 passed

Tests are located in:

tests/test_app.py

The tests verify important application functionality.

## Code Quality

Flake8 is used to check Python code quality.

Run:

flake8 app tests

A successful scan should produce no output.

Flake8 is also executed automatically by GitHub Actions.

## Python Dependency Security

Python dependencies are scanned using pip-audit.

Run:

pip-audit

The expected result after updating vulnerable dependencies is:

No known vulnerabilities found

The dependency security scan is also executed automatically in CI.

## Docker Image Security

Docker images are scanned using Trivy.

The project scans for:

- HIGH severity vulnerabilities
- CRITICAL severity vulnerabilities

Example:

docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:0.70.0 \
  image \
  --scanners vuln \
  --ignore-unfixed \
  --severity HIGH,CRITICAL \
  todo-app:security-test

The final Docker image was verified after addressing vulnerable Python packages.

## GitHub Actions CI/CD

The CI/CD workflow is located at:

.github/workflows/ci-cd.yml

The pipeline automates testing, security scanning, Docker image building, and Docker Hub deployment.

### CI Pipeline

The test job performs:

1. Checkout repository
2. Set up Python 3.14
3. Install dependencies
4. Run Flake8
5. Run Pytest
6. Run pip-audit

### CD Pipeline

The Docker job runs after the test job succeeds.

It performs:

1. Login to Docker Hub
2. Generate Docker image version
3. Build Docker image
4. Scan Docker image using Trivy
5. Push Docker image to Docker Hub

Pipeline flow:

Git Push
   |
   v
Checkout
   |
   v
Install Dependencies
   |
   +------> Flake8
   |
   +------> Pytest
   |
   +------> pip-audit
   |
   v
Docker Build
   |
   v
Trivy Security Scan
   |
   v
Docker Hub

## CI/CD Workflow Triggers

The GitHub Actions workflow runs when:

- Code is pushed to main
- A pull request targets main
- A version tag matching v* is pushed

Example release tag:

v1.1

## GitHub Secrets

The CI/CD workflow uses GitHub repository secrets for Docker Hub authentication.

Required secrets:

DOCKERHUB_USERNAME
DOCKERHUB_TOKEN

The Docker Hub access token is stored securely as a GitHub Actions secret.

Credentials are not hard-coded into the workflow.

## Docker Hub

Docker images are published to Docker Hub.

Docker Hub repository:

sajinskaria/todo-app

Versioned image:

sajinskaria/todo-app:v1.1

Latest image:

sajinskaria/todo-app:latest

Pull the versioned image:

docker pull sajinskaria/todo-app:v1.1

Pull the latest image:

docker pull sajinskaria/todo-app:latest

## Docker Image Versioning

The project uses Git tags for application releases.

Example:

git tag v1.1
git push origin v1.1

The GitHub Actions pipeline detects the version tag and publishes the corresponding Docker image.

Version flow:

Git tag v1.1
     |
     v
GitHub Actions
     |
     v
Docker Build
     |
     v
Trivy Scan
     |
     v
Docker Hub
     |
     +---- sajinskaria/todo-app:v1.1
     |
     +---- sajinskaria/todo-app:latest

Future releases can use:

v1.2
v1.3
v2.0

## Docker Image Verification

Verify the image:

docker pull sajinskaria/todo-app:v1.1

Check the container user:

docker run --rm sajinskaria/todo-app:v1.1 whoami

Expected:

appuser

Check Python:

docker run --rm sajinskaria/todo-app:v1.1 python --version

## Useful Docker Commands

List running containers:

docker ps

List all containers:

docker ps -a

View application logs:

docker logs todo-app

Follow application logs:

docker logs -f todo-app

View MySQL logs:

docker logs todo-mysql

Check application health:

docker inspect --format='{{.State.Health.Status}}' todo-app

Check MySQL health:

docker inspect --format='{{.State.Health.Status}}' todo-mysql

Restart Compose services:

docker compose restart

Stop Compose services:

docker compose down

Start Compose services:

docker compose up -d

Validate Compose configuration:

docker compose config

## Database Persistence Test

The project uses a Docker volume for MySQL persistence.

Start the application:

docker compose up -d

Create a To-Do item through the application.

Stop the containers:

docker compose down

Start them again:

docker compose up -d

The previously created To-Do item should still exist.

This demonstrates persistent database storage.

## Security Practices

The project implements several security practices:

- Application container runs as a non-root user
- Sensitive configuration is stored using environment variables
- .env is excluded from Git
- MySQL is isolated inside the Docker network
- Docker image vulnerability scanning with Trivy
- Python dependency scanning with pip-audit
- Automated testing before Docker image deployment
- Health checks for application and database
- Minimal runtime container configuration
- Docker Hub authentication through GitHub Secrets

## Troubleshooting

### Port 5000 Already in Use

Check:

sudo ss -ltnp | grep :5000

Find the process using the port and stop it if necessary.

### Port 8080 Already in Use

Check:

sudo ss -ltnp | grep :8080

Stop the conflicting service or change the host port in docker-compose.yml.

### Application Is Unhealthy

Check:

docker logs todo-app

Then check MySQL:

docker logs todo-mysql

Check health:

docker inspect --format='{{.State.Health.Status}}' todo-app
docker inspect --format='{{.State.Health.Status}}' todo-mysql

### Check Compose Configuration

Before starting the stack:

docker compose config

### Check Container Networking

List networks:

docker network ls

Inspect the application network:

docker network inspect todo-app_todo-network

## Cleanup

Stop the application:

docker compose down

This removes the Compose containers and network but preserves the named MySQL volume.

Temporary test containers can be removed using:

docker rm -f todo-logging-test 2>/dev/null || true

Reusable Docker images should not be removed if they are needed for future demonstrations.

The MySQL volume should also be preserved unless the database is intentionally being reset.

## Project Verification Checklist

The following components have been implemented and tested:

- [x] Flask application
- [x] MySQL database
- [x] Nginx reverse proxy
- [x] Dockerfile
- [x] Multi-stage Docker build
- [x] Non-root container user
- [x] Docker Compose
- [x] Custom Docker network
- [x] Persistent MySQL volume
- [x] Application health check
- [x] MySQL health check
- [x] Application logging
- [x] Docker container logging
- [x] Pytest
- [x] Flake8
- [x] pip-audit
- [x] Trivy vulnerability scanning
- [x] GitHub Actions CI/CD
- [x] Docker Hub integration
- [x] Versioned Docker images
- [x] v1.1 release
- [x] latest image
- [x] Project documentation
- [x] Architecture documentation

## Final Architecture Summary

                         Internet / User
                                |
                                | :8080
                                v
                         +-------------+
                         |    Nginx    |
                         |   :80       |
                         +------+------+
                                |
                                | :5000
                                v
                         +-------------+
                         | Flask App   |
                         | Python 3.14 |
                         +------+------+
                                |
                                | :3306
                                v
                         +-------------+
                         | MySQL 8.4   |
                         +------+------+
                                |
                                v
                         +-------------+
                         | Docker      |
                         | Volume      |
                         +-------------+

All application services communicate through the Docker network todo-network.

## Final CI/CD Summary

Developer
    |
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +--> Flake8
    |
    +--> Pytest
    |
    +--> pip-audit
    |
    +--> Docker Build
    |
    +--> Trivy Scan
    |
    v
Docker Hub
    |
    +--> sajinskaria/todo-app:v1.1
    |
    +--> sajinskaria/todo-app:latest

## Project Summary

This project demonstrates a complete DevOps workflow for a containerized web application.

The application is developed using Flask and MySQL, containerized using Docker, orchestrated using Docker Compose, exposed through an Nginx reverse proxy, and backed by persistent database storage.

The development workflow is automated using GitHub Actions. Every change is tested with Pytest and Flake8, Python dependencies are checked using pip-audit, Docker images are scanned using Trivy, and validated images are published to Docker Hub using versioned tags.

The project also implements health checks, application logging, container logging, network isolation, persistent storage, and non-root container execution.

This project provides practical experience with modern DevOps and CI/CD practices and demonstrates an end-to-end workflow from source code to automated testing, security validation, container image creation, and Docker Hub deployment.
