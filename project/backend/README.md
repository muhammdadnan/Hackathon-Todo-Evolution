# Backend - FastAPI Todo API

Python FastAPI backend with SQLModel ORM, JWT authentication, and PostgreSQL database.

## Technology Stack

- **Framework**: FastAPI 0.109+
- **Language**: Python 3.11+
- **ORM**: SQLModel 0.0.14+
- **Database**: PostgreSQL (Neon Serverless)
- **Database Driver**: asyncpg (async PostgreSQL)
- **Authentication**: JWT tokens (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic 2.x

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL database (Neon account recommended)
- pip or uv package manager

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Unix/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Edit .env with your configuration
# IMPORTANT: BETTER_AUTH_SECRET must match frontend
```

### Environment Variables

Create `.env` with the following variables:

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database
# Example for Neon: postgresql+asyncpg://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# Authentication
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-long

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Environment
ENVIRONMENT=development
```

### Database Setup

1. Create a Neon PostgreSQL database at https://neon.tech
2. Copy the connection string to `.env` as `DATABASE_URL`
3. The database tables will be created automatically on first run

### Development

```bash
# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access API documentation
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   ├── models/              # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   └── task.py          # Task model
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   └── task.py          # Task schemas
│   ├── routes/              # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   └── tasks.py         # Task CRUD endpoints
│   └── middleware/          # Middleware
│       ├── __init__.py
│       ├── auth.py          # JWT verification
│       └── cors.py          # CORS configuration
├── tests/                   # Test suite
│   ├── conftest.py          # Pytest fixtures
│   ├── test_auth.py         # Authentication tests
│   ├── test_tasks.py        # Task endpoint tests
│   └── test_isolation.py    # User isolation tests
├── pyproject.toml           # Python project configuration
└── requirements.txt         # Python dependencies
```

## Available Commands

```bash
# Development
uvicorn app.main:app --reload              # Run dev server
uvicorn app.main:app --reload --port 8001  # Run on different port

# Testing
pytest                                      # Run all tests
pytest --cov=app                           # Run with coverage
pytest --cov=app --cov-report=html         # Generate HTML coverage report
pytest tests/test_auth.py                  # Run specific test file
pytest -v                                  # Verbose output
pytest -k "test_name"                      # Run specific test

# Code Quality
ruff check .                               # Linting
ruff format .                              # Formatting
mypy app/                                  # Type checking

# Database
alembic revision --autogenerate -m "msg"   # Create migration
alembic upgrade head                       # Apply migrations
alembic downgrade -1                       # Rollback one migration
```

## API Endpoints

### Health Check
- `GET /health` - Health check endpoint (no auth required)

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Authenticate and receive JWT token

### Tasks (All require JWT authentication)
- `GET /api/{user_id}/tasks` - List all user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get task details
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

### API Documentation
- `GET /docs` - Swagger UI (interactive API documentation)
- `GET /redoc` - ReDoc (alternative API documentation)
- `GET /openapi.json` - OpenAPI schema

## Authentication

All protected endpoints require JWT token in Authorization header:

```bash
Authorization: Bearer <jwt_token>
```

JWT tokens are issued by Better Auth on the frontend and verified by the backend using the shared `BETTER_AUTH_SECRET`.

## Database Schema

### users table
- `id`: string (primary key)
- `email`: string (unique, not null)
- `password`: string (hashed, not null)
- `name`: string (nullable)
- `created_at`: timestamp
- `updated_at`: timestamp

### tasks table
- `id`: integer (primary key, auto-increment)
- `user_id`: string (foreign key → users.id)
- `title`: string (not null, max 200 chars)
- `description`: text (nullable, max 1000 chars)
- `completed`: boolean (default false)
- `created_at`: timestamp
- `updated_at`: timestamp

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_signup_success

# Run tests matching pattern
pytest -k "auth"
```

### Test Structure

- `conftest.py` - Pytest fixtures (database, test client, test users)
- `test_auth.py` - Authentication endpoint tests
- `test_tasks.py` - Task CRUD endpoint tests
- `test_isolation.py` - User isolation security tests

### Coverage Requirements

- Minimum 80% code coverage
- All API endpoints must have tests
- All authentication/authorization paths tested
- All error scenarios covered

## Security

### Authentication & Authorization
- All passwords hashed with bcrypt
- JWT tokens signed with strong secret (min 32 characters)
- User isolation enforced on all endpoints
- JWT user_id must match path user_id

### Input Validation
- All inputs validated with Pydantic models
- SQL injection prevented by SQLModel (parameterized queries)
- Request size limits enforced
- CORS properly configured

### Error Handling
- No sensitive information in error messages
- Proper HTTP status codes
- Descriptive error messages for debugging

## Deployment

### Environment Variables

Ensure all environment variables are set in your deployment platform:
- `DATABASE_URL` - PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Shared secret (must match frontend)
- `CORS_ORIGINS` - Allowed frontend origins
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `ENVIRONMENT` - production

### Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Set environment variables
railway variables set DATABASE_URL=<your-neon-url>
railway variables set BETTER_AUTH_SECRET=<your-secret>
railway variables set CORS_ORIGINS=<your-frontend-url>

# Deploy
railway up
```

### Render

1. Create new Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in dashboard

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Database Connection Issues

```bash
# Test database connection
python -c "from app.database import engine; print('Connected!')"

# Check DATABASE_URL format
# Should be: postgresql+asyncpg://user:pass@host:port/db
```

### CORS Issues

Ensure `CORS_ORIGINS` in `.env` includes your frontend URL:
```bash
CORS_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
```

### JWT Verification Failures

1. Verify `BETTER_AUTH_SECRET` matches frontend
2. Check JWT token format in Authorization header
3. Ensure token hasn't expired

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.11+
```

## Development Workflow

This project follows Test-Driven Development (TDD):

1. **RED**: Write failing tests first
2. **GREEN**: Implement code to pass tests
3. **REFACTOR**: Improve code quality

All changes must:
- Have tests with >80% coverage
- Pass type checking (mypy)
- Pass linting (ruff)
- Follow code standards in `CLAUDE.md`

## Related Documentation

- Root README: `../README.md`
- Frontend README: `../frontend/README.md`
- Development Guide: `CLAUDE.md`
- Specification: `../specs/phase-2-web-app/spec.md`
- Implementation Plan: `../specs/phase-2-web-app/plan.md`

## Support

For issues or questions, refer to the project documentation in `../specs/` and `../history/` directories.
