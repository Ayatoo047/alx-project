# Django BlogPost Application

This is a simple blog post application built with Django. It utilizes `django-tenants` for multi-tenancy with a landlord tenant model. The app includes features such as pagination, search, real-time comments using WebSockets and Django Channels, and user authentication.

## Features

- Multi-tenancy using `django-tenants` with a landlord tenant model.
- Pagination for blog posts.
- Search functionality to find blog posts.
- Real-time comments on blog posts using WebSockets and Django Channels.
- User authentication for secure access and management.

## Getting Started

### Prerequisites
- Docker and Docker Compose installed on your machine.
- Python 3.8 or higher.
- PostgreSQL database.

### Installation

1. **Clone the repository**:


2. **Set up Docker Compose for the Postgress DB**:
    docker-compose up -d

3. **Install the required dependencies**:
    pip install -r requirements.txt

4. **Migrate the Models**:
    python manage.py migrate

5. **Start the Django server**:
    python manage.py runserver

### Running the Application

After setting up the database and starting the Django server, you can access the application at `http://localhost:8000`.
