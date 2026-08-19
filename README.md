Absolutely — here’s a polished, senior-level `README.md` tailored to the project structure, Docker setup, PostgreSQL, Redis, WebSockets, REST API, Swagger/ReDoc, and pytest workflow you provided.

# Chaty

**Chaty** is a Django-based private messaging application that allows users to communicate with each other through real-time private chats.

The project is built with **Django 5.2**, **Django REST Framework**, **Django Channels**, **Redis**, and **PostgreSQL**. It is containerized with Docker and uses **Nginx** as a reverse proxy for serving the application and static files.

---

## Features

* 👤 **User Registration & Authentication**

  * User registration
  * Login/logout
  * Authentication and authorization

* 🔐 **Role-Based Permissions**

  * Role-based access control
  * Permission management
  * Protected API endpoints and application functionality

* 💬 **Private Chat**

  * Private conversations between users
  * Real-time messaging
  * WebSocket-based communication

* ⚡ **WebSockets**

  * Real-time communication using Django Channels
  * Redis used as the channel layer
  * Supports asynchronous chat communication

* 🌐 **REST API**

  * RESTful API endpoints
  * API documentation with Swagger and ReDoc

* 📁 **File Uploads**

  * Support for uploading files through the application

* 🛠️ **Django Admin**

  * Built-in Django administration panel
  * Management of users and application data

* 🗄️ **PostgreSQL**

  * PostgreSQL as the primary relational database

* 🐳 **Dockerized Environment**

  * Backend
  * PostgreSQL
  * Redis
  * Nginx

* 🧪 **Testing**

  * Automated tests using `pytest`

---

## Technology Stack

| Technology            | Purpose                             |
| --------------------- | ----------------------------------- |
| Python                | Programming language                |
| Django 5.2            | Web framework                       |
| Django REST Framework | REST API                            |
| Django Channels       | WebSocket / real-time communication |
| Daphne                | ASGI server                         |
| PostgreSQL 14         | Relational database                 |
| Redis 6               | Channel layer / caching             |
| Nginx                 | Reverse proxy and static files      |
| Docker                | Containerization                    |
| pytest                | Automated testing                   |
| drf-yasg              | Swagger / ReDoc API documentation   |
| Pillow                | Image/file processing               |

---

## Project Structure

```text
.
├── chat/
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py
│   ├── migrations/
│   ├── models.py
│   ├── routing.py
│   ├── scope.py
│   ├── static/
│   ├── templates/
│   ├── tests/
│   ├── urls.py
│   └── views.py
│
├── chatapp/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── nginx/
│   ├── default.conf
│   ├── Dockerfile
│   └── nginx.conf
│
├── compose.yml
├── Dockerfile
├── manage.py
├── pytest.ini
├── requirements.txt
└── README.md
```

### Main Components

#### `chat/`

The main application responsible for chat functionality.

Important files include:

* `models.py` — Database models
* `views.py` — HTTP/API views
* `urls.py` — Application URL routes
* `consumers.py` — WebSocket consumers
* `routing.py` — WebSocket routing
* `admin.py` — Django Admin configuration
* `tests/` — Application tests
* `templates/` — HTML templates
* `static/` — Static assets

#### `chatapp/`

The main Django project configuration.

* `settings.py` — Django configuration
* `urls.py` — Root URL configuration
* `asgi.py` — ASGI configuration for WebSockets
* `wsgi.py` — WSGI configuration

#### `nginx/`

Nginx configuration used as a reverse proxy and for serving static files.

---

# Requirements

Before starting the project, make sure you have the following installed:

* Docker
* Docker Compose
* Git

The application itself runs inside Docker containers, so Python and PostgreSQL do not need to be installed directly on the host machine.

---

# Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
cd chaty
```

Replace `<repository-url>` with the URL of your repository.

---

## 2. Configure Environment Variables

Create your local environment file from the example:

```bash
cp .env.example .env
```

The `.env.example` file contains the required environment variables:

```env
POSTGRES_USER=chatpostgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=chatdb
POSTGRES_PORT=5432
POSTGRES_APP=chatpostgresql

SECRET_KEY=your-secret-key

DEBUG=True

REDIS_HOST=redis://redis:6379/1
```

### Environment Variables

| Variable            | Description                           |
| ------------------- | ------------------------------------- |
| `POSTGRES_USER`     | PostgreSQL username                   |
| `POSTGRES_PASSWORD` | PostgreSQL password                   |
| `POSTGRES_DB`       | PostgreSQL database name              |
| `POSTGRES_PORT`     | PostgreSQL internal container port    |
| `POSTGRES_APP`      | PostgreSQL service/container hostname |
| `SECRET_KEY`        | Django secret key                     |
| `DEBUG`             | Enables/disables Django debug mode    |
| `REDIS_HOST`        | Redis connection URL                  |

> **Security:** Never commit your real `.env` file or production secrets to version control.

For production, use a strong randomly generated `SECRET_KEY` and a secure database password.

---

# Docker Setup

The project uses Docker Compose to run four services:

```text
                  ┌─────────────┐
                  │   Nginx     │
                  │    :81      │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │   Backend   │
                  │    :8000    │
                  └──────┬──────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       ┌─────────────┐       ┌─────────────┐
       │ PostgreSQL  │       │    Redis    │
       │    :5433    │       │    :6379    │
       └─────────────┘       └─────────────┘
```

### Services

#### Backend

Django application running on port `8000`.

#### PostgreSQL

PostgreSQL 14 database.

The host exposes PostgreSQL on:

```text
localhost:5433
```

The container itself uses the standard PostgreSQL port:

```text
5432
```

#### Redis

Redis is used by Django Channels as the WebSocket channel layer.

```text
localhost:6379
```

#### Nginx

Nginx acts as the reverse proxy in front of the Django backend.

The host exposes Nginx on:

```text
localhost:81
```

---

# Start the Application

Build the Docker images:

```bash
docker compose build
```

Start all services in detached mode:

```bash
docker compose up -d
```

Check the running containers:

```bash
docker compose ps
```

You should see the following services:

```text
backend
chatpostgresql
redis
nginx
```

---

# Database Migrations

After starting the containers, run Django migrations:

```bash
docker exec -it backend bash
```

Then:

```bash
python manage.py migrate
```

Alternatively, run the migration directly:

```bash
docker exec -it backend python manage.py migrate
```

---

# Create a Superuser

To access the Django Admin panel, create a superuser:

```bash
docker exec -it backend python manage.py createsuperuser
```

Follow the prompts to configure the administrator account.

---

# Run the Development Server

If you want to run Django's development server inside the backend container:

```bash
docker exec -it backend bash
```

Then:

```bash
python manage.py runserver
```

The development server will be available at:

```text
http://localhost:8000/
```

> When using Docker Compose with the project's normal backend command, the application may already be running. Check the `Dockerfile` to determine the default container command.

---

# Application URLs

Assuming the default configuration:

| Service        | URL                              |
| -------------- | -------------------------------- |
| Django backend | `http://localhost:8000/`         |
| Nginx          | `http://localhost:81/`           |
| Swagger        | `http://localhost:8000/swagger/` |
| ReDoc          | `http://localhost:8000/redoc/`   |
| Health check   | `http://localhost:8000/health/`  |
| Django Admin   | `http://localhost:8000/admin/`   |

When accessing the application through Nginx, use:

```text
http://localhost:81/
```

---

# API Documentation

Chaty uses `drf-yasg` to generate interactive API documentation.

## Swagger

Swagger UI is available at:

```text
http://localhost:8000/swagger/
```

Swagger provides an interactive interface for exploring and testing API endpoints.

## ReDoc

ReDoc is available at:

```text
http://localhost:8000/redoc/
```

ReDoc provides a clean, documentation-oriented view of the API.

---

# WebSockets

Chaty uses **Django Channels** to provide real-time private messaging.

The WebSocket implementation is primarily located in:

```text
chat/
├── consumers.py
└── routing.py
```

### `consumers.py`

Contains the WebSocket consumers responsible for handling:

* WebSocket connections
* Authentication
* Receiving messages
* Sending messages
* Disconnect handling
* Real-time chat events

### `routing.py`

Defines the WebSocket URL routing used by Django Channels.

The application uses **Redis** as the Channels backend, allowing WebSocket communication to work across application processes/instances.

---

# Redis

Redis is configured as a supporting service for Django Channels.

The Docker Compose configuration uses:

```yaml
redis:
  image: redis:6.0-alpine
```

The Redis connection is configured through:

```env
REDIS_HOST=redis://redis:6379/1
```

Inside the Docker network, the backend connects to Redis using the service name:

```text
redis
```

Redis data is persisted through the Docker volume:

```text
redis_data
```

---

# PostgreSQL

The application uses PostgreSQL 14.

The Docker Compose service is:

```yaml
chatpostgresql:
  image: postgres:14
```

Database data is persisted using:

```text
chat_postgres
```

The PostgreSQL service is accessible from the host through:

```text
localhost:5433
```

However, Django should connect to PostgreSQL using the Docker service hostname and the container port:

```text
chatpostgresql:5432
```

This distinction is important:

```text
Host machine:
localhost:5433

Docker network:
chatpostgresql:5432
```

---

# Static Files

Static files are shared between the backend and Nginx containers using the Docker volume:

```text
static_files_volume
```

The volume is mounted at:

```text
/static
```

Both services share this volume:

```text
backend  → /static
nginx    → /static
```

This allows Nginx to serve static assets without routing those requests through Django.

---

# File Uploads

The application supports file uploads.

The project currently contains the relevant application structure for handling uploaded files, including Pillow as an image-processing dependency.

For production deployments, make sure media/upload storage is configured explicitly and persisted independently of the application container.

> The current `compose.yml` has the `/media` volume commented out. If uploaded media needs to survive container recreation, configure a persistent media volume or use object storage such as S3-compatible storage.

---

# Testing

The project uses **pytest** for automated testing.

Tests are located under:

```text
chat/tests/
```

The project also contains:

```text
pytest.ini
```

Run the test suite from inside the backend container:

```bash
docker exec -it backend pytest
```

For verbose output:

```bash
docker exec -it backend pytest -v
```

To run a specific test file:

```bash
docker exec -it backend pytest chat/tests/test_example.py
```

---

# Useful Django Commands

Open a shell inside the backend container:

```bash
docker exec -it backend bash
```

Run migrations:

```bash
python manage.py migrate
```

Create migrations:

```bash
python manage.py makemigrations
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Collect static files:

```bash
python manage.py collectstatic
```

Open the Django shell:

```bash
python manage.py shell
```

Run tests:

```bash
pytest
```

---

# Docker Commands

Start the application:

```bash
docker compose up -d
```

Stop the application:

```bash
docker compose down
```

Rebuild the application:

```bash
docker compose build
```

Rebuild and start:

```bash
docker compose up -d --build
```

View logs:

```bash
docker compose logs
```

View backend logs:

```bash
docker compose logs -f backend
```

View Nginx logs:

```bash
docker compose logs -f nginx
```

View PostgreSQL logs:

```bash
docker compose logs -f chatpostgresql
```

View Redis logs:

```bash
docker compose logs -f redis
```

Check running containers:

```bash
docker compose ps
```

---

# Production Considerations

The current configuration is suitable as a Dockerized development/deployment foundation, but additional hardening is recommended before deploying to production.

### Environment

Set:

```env
DEBUG=False
```

Use a secure, randomly generated Django `SECRET_KEY`.

Do not commit `.env` files containing production credentials.

### PostgreSQL

Use a strong database password and restrict external database access where possible.

The current configuration exposes PostgreSQL on:

```text
5433
```

For production, consider removing the host port mapping if PostgreSQL only needs to be accessed by the application containers.

### Nginx

Nginx should be the public-facing service, with Django kept behind the reverse proxy.

A typical production architecture is:

```text
Internet
   │
   ▼
Nginx
   │
   ▼
Django / Daphne
   │
   ├── PostgreSQL
   │
   └── Redis
```

### HTTPS

Production deployments should use HTTPS/TLS.

For example:

```text
https://chat.example.com
```

rather than exposing the application directly over HTTP.

### WebSocket Security

When deploying WebSockets in production:

* Use `wss://` over HTTPS.
* Configure trusted origins correctly.
* Ensure Nginx forwards WebSocket upgrade headers.
* Protect WebSocket endpoints with appropriate authentication and authorization.

### Persistent Storage

Database, Redis, and uploaded media should use persistent storage.

The project already defines Docker volumes for:

```text
static_files_volume
chat_postgres
redis_data
```

Make sure these volumes exist before starting the application when they are configured as external volumes.

For example:

```bash
docker volume create static_files_volume
docker volume create chat_postgres
docker volume create redis_data
```

Then:

```bash
docker compose up -d
```

---

# Dependencies

The main Python dependencies include:

```text
Django==5.2
django-cors-headers==4.2.0
django-dotenv==1.4.2
geocoder==1.38.1
gunicorn==21.2.0
pillow==12.2.0
psycopg2-binary==2.9.12
channels[daphne]
channels-redis
django-redis
drf-yasg
```

The complete dependency list is maintained in:

```text
requirements.txt
```

---

# Architecture Overview

Chaty follows a Django application architecture with separate responsibilities for HTTP requests, REST APIs, and real-time communication.

```text
                         ┌──────────────────┐
                         │      Client      │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                 HTTP/REST                  WebSocket
                    │                           │
                    ▼                           ▼
              ┌───────────┐               ┌───────────┐
              │   Nginx   │               │  Channels │
              └─────┬─────┘               │ Consumers │
                    │                     └─────┬─────┘
                    ▼                           │
              ┌───────────┐                     ▼
              │  Django   │◄───────────────► Redis
              │  Backend  │
              └─────┬─────┘
                    │
                    ▼
              ┌───────────┐
              │PostgreSQL │
              └───────────┘
```

---

# Health Check

The backend container includes a health check against:

```text
/health/
```

Docker periodically checks:

```bash
curl -f http://localhost:8000/health/
```

The health check runs every 30 seconds with a 10-second timeout and three retries.

This endpoint can also be used by deployment infrastructure or monitoring systems to determine whether the application is responding correctly.

---

# Development Workflow

A typical development workflow is:

```bash
# Clone the project
git clone <repository-url>

# Enter the project
cd chaty

# Configure environment
cp .env.example .env

# Build containers
docker compose build

# Start services
docker compose up -d

# Apply migrations
docker exec -it backend python manage.py migrate

# Run tests
docker exec -it backend pytest

# Check the application
# http://localhost:8000/
```

For API development:

```text
Swagger:
http://localhost:8000/swagger/

ReDoc:
http://localhost:8000/redoc/
```

---

# License

This project is distributed under the license included in:

```text
LICENSE
```

Please review the `LICENSE` file for the complete licensing terms.

---

# Contributing

Contributions are welcome.

Before submitting changes:

1. Create a dedicated branch for your changes.
2. Follow the existing project structure and coding conventions.
3. Add or update tests where appropriate.
4. Run the test suite with `pytest`.
5. Verify database migrations.
6. Verify REST API functionality.
7. Verify WebSocket functionality for changes related to real-time chat.
8. Submit a pull request describing the changes.

---

## Quick Start

For experienced developers who just want to get the project running:

```bash
git clone <repository-url>
cd chaty

cp .env.example .env

docker compose build
docker compose up -d

docker exec -it backend python manage.py migrate

docker exec -it backend python manage.py createsuperuser
```

Then open:

```text
Application: http://localhost:8000/
Nginx:       http://localhost:81/
Swagger:     http://localhost:8000/swagger/
ReDoc:       http://localhost:8000/redoc/
Admin:       http://localhost:8000/admin/
```

Run tests with:

```bash
docker exec -it backend pytest
```

**Chaty** provides a Dockerized Django foundation for private, real-time user-to-user communication using PostgreSQL for persistent data and Redis/Django Channels for WebSocket communication.
