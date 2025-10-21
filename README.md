# Real Estate API

A Django REST Framework-based real estate application with multi-database architecture, featuring separate databases for users and listings with JWT authentication.
- This  app based on this course on youtube:https://www.youtube.com/playlist?list=PLJRGQoqpRwdfgaQujSZMzrG7AkRlbjRkC

## 🏗️ Architecture

- **Multi-Database Setup**: Separate PostgreSQL databases for users and listings
- **Authentication**: JWT-based authentication using Simple JWT
- **API**: RESTful API built with Django REST Framework
- **Testing**: Comprehensive test suite with pytest and factory-boy

## 📋 Features

- User registration and authentication (regular users and realtors)
- Realtor-specific listing management (CRUD operations)
- Public listing browsing
- Image upload support for property photos
- Database routing for optimal performance

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Docker & Docker Compose
- UV package manager

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd real-estate
   ```

2. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your database configurations
   ```

3. **Start with Docker Compose**

   ```bash
   docker-compose up --build
   ```

   Or run locally:

   ```bash
   uv sync
   uv run python manage.py migrate --database=users
   uv run python manage.py migrate --database=listings
   uv run python manage.py runserver
   ```

## 🗄️ Database Architecture

The application uses a multi-database setup with custom routers:

- **users** database: User accounts, authentication, sessions
- **listings** database: Property listings and related data
- **default** database: SQLite for local development fallback

### Database Routers

- [`users.router.AuthRouter`](users/router.py) - Routes user-related models
- [`listings.router.ListingsRouter`](listings/router.py) - Routes listing-related models

## 📡 API Endpoints

### Authentication

- `POST /api/token/` - Login (get access/refresh tokens)
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/token/verify/` - Verify token validity

### Users

- `POST /auth/user/register` - Register new user/realtor
- `GET /auth/user/me` - Get current user profile

### Listings

- `GET /api/listings/get-listings` - Public listings (published only)
- `GET /api/listings/detail?slug=<slug>` - Get listing details
- `GET /api/listings/manage` - Realtor's listings management
- `POST /api/listings/manage` - Create new listing (realtors only)
- `PUT /api/listings/manage` - Update listing (realtors only)
- `PATCH /api/listings/manage` - Update listing status (realtors only)
- `DELETE /api/listings/manage` - Delete listing (realtors only)

## 🏠 Models

### User Model ([`users.models.UserAccount`](users/models.py))

- Custom user model extending AbstractBaseUser
- Fields: email, name, is_active, is_staff, is_realtor
- Custom manager with `create_user`, `create_realtor`, `create_superuser` methods

### Listing Model ([`listings.models.Listing`](listings/models.py))

- Property listings with comprehensive details
- Image upload support (main_photo, photo_1, photo_2, photo_3)
- Choice fields for sale_type and home_type
- Automatic slug generation and unique constraints

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
uv run pytest

# Run specific test modules
uv run pytest users/tests/
uv run pytest listings/tests/

# Run with coverage
uv run pytest --cov=.
```

### Test Structure

- Unit tests in `users/tests/unit/` and `listings/tests/unit/`
- Factory classes for test data generation using [`factory-boy`](users/tests/factories.py)
- Database fixtures for multi-database testing

## 🛠️ Development

### Code Quality

Pre-commit hooks are configured for:

- Black (code formatting)
- isort (import sorting)
- flake8 (linting)
- bandit (security checks)
- Django-specific checks

Install pre-commit hooks:

```bash
pre-commit install
```

### Database Management

```bash
# Create migrations
uv run python manage.py makemigrations users
uv run python manage.py makemigrations listings

# Apply migrations
uv run python manage.py migrate --database=users
uv run python manage.py migrate --database=listings

# Populate with sample data
uv run python manage.py populate_db
```

## 🐳 Docker Setup

The project includes Docker configuration for both development and production:

- [`docker-compose.yml`](docker-compose.yml) - Multi-container setup with PostgreSQL databases
- [`Dockerfile`](Dockerfile) - Python 3.13 slim image with UV package manager
- Health checks for database services

## 📁 Project Structure

```
├── core/                 # Django project settings
├── users/               # User management app
│   ├── models.py       # Custom user model
│   ├── views.py        # Authentication views
│   ├── router.py       # Database router
│   └── tests/          # User tests
├── listings/           # Property listings app
│   ├── models.py       # Listing model
│   ├── views.py        # Listing CRUD views
│   ├── router.py       # Database router
│   └── tests/          # Listing tests
├── nginx/              # Nginx configuration
└── media/              # User-uploaded files
```

## 🔒 Security Features

- JWT token authentication
- Permission-based access control (realtors vs regular users)
- Input validation and sanitization
- Database query optimization with custom routers
- Pre-commit security scanning with bandit

## 📊 Performance

- Database connection pooling with psycopg[pool]
- Optimized queries with select_related and prefetch_related
- Image handling with Pillow
- Custom database routing for load distribution



## 📄 License

This project is licensed under the BSD 3-Clause License - see the [setup.cfg](setup.cfg) file for details.
