# Containerized Full-Stack To-Do Application

A production-oriented To-Do Management Application built with Python Flask and MySQL and deployed using Docker, Docker Compose, and Nginx.

The project demonstrates containerization, persistent storage, health checks, security scanning, automated testing, CI/CD, Docker Hub integration, and versioned Docker image releases.

---

## 1. Project Overview

The application allows users to:

- View To-Do tasks
- Add new tasks
- Mark tasks as completed or incomplete
- Delete tasks
- Check application health

The application uses:

- Python Flask for the backend
- MySQL 8.4 for persistent data storage
- Nginx as a reverse proxy
- Docker for containerization
- Docker Compose for multi-container deployment
- GitHub Actions for CI/CD
- Docker Hub for container image storage
- Trivy for Docker image vulnerability scanning
- pip-audit for Python dependency scanning

---

## 2. Architecture

The application follows a three-tier containerized architecture:

```text
                    User
                     |
                     | HTTP :8080
                     v
              +--------------+
              |     Nginx    |
              | Reverse Proxy|
              +------+-------+
                     |
                     | HTTP :5000
                     v
              +--------------+
              | Flask App    |
              | Python       |
              +------+-------+
                     |
                     | MySQL :3306
                     v
              +--------------+
              |    MySQL     |
              |   Database   |
              +------+-------+
                     |
                     v
              Persistent Volume
              todo-mysql-data
