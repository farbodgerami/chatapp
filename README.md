# ChatApp

A real-time chat application built with **Django Channels** that enables private messaging through WebSockets. The application provides a responsive chat experience with online presence, typing indicators, message history, and message delivery status.

---

## Features

* 🔐 User authentication
* 💬 Real-time private messaging
* 👥 Private one-to-one chats
* ⌨️ Typing indicators
* 👁️ Seen/Not Seen message status
* 📜 Persistent message history
* ⚡ WebSocket communication powered by Django Channels

---

## Tech Stack

### Backend

* Django 5.x
* Django Channels
* ASGI
* Daphne

### Database

* PostgreSQL

### Real-Time Communication

* Redis (Channel Layer)

### Frontend

* HTML
* CSS

### Deployment

* Docker Compose
* Nginx (serving static files)

---

## Architecture

The application uses Django for traditional HTTP requests and authentication while Django Channels manages real-time WebSocket connections.

```
Client
   │
HTTP / WebSocket
   │
Django + Django Channels
   │
Redis Channel Layer
   │
PostgreSQL
```

### Components

* **Django** handles authentication, routing, and HTTP requests.
* **Django Channels** manages WebSocket connections.
* **Redis** acts as the channel layer for real-time communication.
* **PostgreSQL** stores user accounts and chat messages.
* **Daphne** serves the ASGI application.
* **Nginx** serves static files.

---

## Getting Started

### Prerequisites

Make sure you have the following installed:

* Git
* Docker
* Docker Compose

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd chatapp
```

Start the application:

```bash
docker compose up
```

Docker Compose will build and start all required services, including:

* Django
* PostgreSQL
* Redis
* Daphne
* Nginx

---

## Project Structure

```
chatapp/
├── chat/
├── users/
├── templates/
├── static/
├── media/
├── nginx/
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── README.md
```

> The exact structure may differ depending on your project layout.

---

## How It Works

1. Users authenticate using Django's authentication system.
2. After logging in, users can open private conversations.
3. Messages are sent over WebSockets.
4. Django Channels broadcasts messages through Redis.
5. Messages are stored in PostgreSQL.
6. Typing indicators and seen status are updated in real time.

---

## Future Improvements

* Group chats
* File sharing
* Image and video messages
* Emoji reactions
* Push notifications
* Voice and video calls
* Message search

---

## License

This project is available under the MIT License.

---

## Author

Developed by **Your Name**.

