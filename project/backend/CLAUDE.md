# Backend Development Guide

## Context
This is the FastAPI backend for the Todo Evolution Phase 2 project. It provides REST API endpoints for task management with JWT authentication and user isolation.

## Technology Stack
- **Framework**: FastAPI 0.109+
- **Language**: Python 3.11+
- **ORM**: SQLModel 0.0.14+
- **Database**: PostgreSQL (Neon Serverless)
- **Database Driver**: asyncpg (async PostgreSQL)
- **Authentication**: JWT tokens (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic 2.x (built into SQLModel)

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

## Development Commands
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Unix/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=term-missing

# Run linting
ruff check .

# Run type checking
mypy app/

# Format code
ruff format .
```

## Environment Variables
Copy `.env.example` to `.env` and configure:
- `DATABASE_URL`: PostgreSQL connection string (Neon)
- `BETTER_AUTH_SECRET`: Shared secret for JWT (must match frontend)
- `CORS_ORIGINS`: Allowed frontend origins (comma-separated)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `ENVIRONMENT`: development, staging, or production

## Code Standards

### Python Style
- Follow PEP 8 style guidelines
- Use type hints for all functions and methods
- Maximum line length: 100 characters
- Use async/await for all database operations
- Use f-strings for string formatting

### Type Safety
- All functions must have type hints
- Use `Optional[T]` for nullable types
- Use `List[T]`, `Dict[K, V]` for collections
- No `Any` types unless absolutely necessary
- Enable mypy strict mode

### Database Operations
- Use SQLModel for all database operations
- Always use async sessions
- Filter all queries by user_id for user isolation
- Use transactions for multi-step operations
- Handle database errors gracefully

### API Design
- RESTful endpoint structure: `/api/{user_id}/tasks`
- Use proper HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Return appropriate HTTP status codes
- Use Pydantic models for request/response validation
- Include descriptive error messages

### Authentication & Authorization
- All endpoints (except health check) require JWT token
- Verify JWT signature using BETTER_AUTH_SECRET
- Extract user_id from JWT payload
- Verify JWT user_id matches path user_id
- Return 401 for missing/invalid tokens
- Return 403 for user_id mismatch

### Error Handling
- Use HTTPException for API errors
- Include descriptive error messages
- Log errors for debugging
- Don't expose sensitive information in errors
- Handle database connection errors

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Authenticate and receive JWT token

### Tasks
- `GET /api/{user_id}/tasks` - List all user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get task details
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

### Health Check
- `GET /health` - Health check endpoint (no auth required)

## Testing Strategy

### Test Types
- **Unit Tests**: Test individual functions and utilities
- **Integration Tests**: Test API endpoints with database
- **Authentication Tests**: Test JWT generation and verification
- **User Isolation Tests**: Ensure users cannot access others' data

### Test Fixtures
- Use pytest fixtures for database setup/teardown
- Create test users and tasks in fixtures
- Use async test functions with pytest-asyncio
- Clean up test data after each test

### Coverage Requirements
- Minimum 80% code coverage
- All API endpoints must have tests
- All authentication/authorization paths tested
- All error scenarios covered

## Common Tasks

### Adding a New Model
1. Create model file in `app/models/`
2. Define SQLModel class with table=True
3. Add type hints for all fields
4. Define relationships if needed
5. Create Alembic migration

### Adding a New Endpoint
1. Create route handler in `app/routes/`
2. Add JWT authentication dependency
3. Validate user_id matches JWT
4. Use Pydantic schemas for validation
5. Write tests before implementation (TDD)

### Adding Middleware
1. Create middleware file in `app/middleware/`
2. Define middleware function or class
3. Register in `app/main.py`
4. Test middleware behavior

## Security Checklist
- [ ] All endpoints require JWT authentication
- [ ] User_id validation on every endpoint
- [ ] No SQL injection vulnerabilities (use SQLModel)
- [ ] Passwords hashed with bcrypt
- [ ] JWT tokens signed with strong secret
- [ ] CORS properly configured
- [ ] No secrets in source code
- [ ] Input validation on all endpoints
- [ ] Error messages don't expose sensitive data

## Constitution Compliance
- Follow all standards in `.specify/memory/constitution.md`
- Enforce user isolation on every endpoint
- No hardcoded secrets or credentials
- Minimum 80% test coverage
- All changes must be minimal and focused
- Use async/await for all database operations

## Database Schema

### users table
- id: string (primary key)
- email: string (unique, not null)
- password: string (hashed, not null)
- name: string (nullable)
- created_at: timestamp
- updated_at: timestamp

### tasks table
- id: integer (primary key, auto-increment)
- user_id: string (foreign key → users.id)
- title: string (not null, max 200 chars)
- description: text (nullable, max 1000 chars)
- completed: boolean (default false)
- created_at: timestamp
- updated_at: timestamp

## Related Documentation
- Root: `../CLAUDE.md`
- Frontend: `../frontend/CLAUDE.md`
- Specification: `../specs/phase-2-web-app/spec.md`
- Implementation Plan: `../specs/phase-2-web-app/plan.md`
- Tasks: `../specs/phase-2-web-app/tasks.md`
