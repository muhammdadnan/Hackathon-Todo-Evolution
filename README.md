# Phase 2 Todo Application - README

## Overview

A full-stack todo application built with Next.js 16+, FastAPI, and PostgreSQL. Features complete CRUD functionality, JWT authentication, and user isolation.

## Features

- **Authentication**: Sign up, sign in with JWT tokens
- **Task Management**: Create, read, update, delete tasks
- **Task Completion**: Toggle completion status with optimistic UI
- **Filtering**: View all, pending, or completed tasks
- **User Isolation**: Each user sees only their own tasks
- **Responsive Design**: Works on desktop and mobile
- **Real-time Validation**: Character counters and error messages
- **Confirmation Dialogs**: Prevent accidental deletion

## Tech Stack

### Backend
- FastAPI 0.109+
- Python 3.11+
- SQLModel (ORM)
- PostgreSQL (Neon)
- JWT Authentication
- pytest (65 test cases)

### Frontend
- Next.js 16+ (App Router)
- TypeScript (strict mode)
- Tailwind CSS 3.x
- React hooks
- Better Auth

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Neon PostgreSQL account

### 1. Database Setup

See [DATABASE-SETUP.md](DATABASE-SETUP.md) for detailed instructions.

Quick version:
1. Create Neon account at [neon.tech](https://neon.tech)
2. Create new project
3. Copy connection string

### 2. Backend Setup

```bash
cd project/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL and BETTER_AUTH_SECRET

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

### 3. Frontend Setup

```bash
cd project/frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local with your configuration

# Run development server
npm run dev
```

Frontend will be available at: http://localhost:3000

### 4. Run Tests

```bash
cd project/backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test suite
pytest tests/test_auth.py -v
pytest tests/test_tasks.py -v
```

## Project Structure

```
Phase-2/
├── project/
│   ├── backend/              # FastAPI backend
│   │   ├── app/
│   │   │   ├── main.py       # App entry point
│   │   │   ├── models/       # Database models
│   │   │   ├── routes/       # API endpoints
│   │   │   ├── schemas/      # Pydantic schemas
│   │   │   └── middleware/   # Auth middleware
│   │   └── tests/            # Test suite (65 tests)
│   └── frontend/             # Next.js frontend
│       ├── app/              # App Router pages
│       ├── components/       # React components
│       └── lib/              # Utilities
├── specs/                    # Specifications
│   └── phase-2-web-app/
│       ├── spec.md           # Feature specification
│       ├── plan.md           # Implementation plan
│       └── tasks.md          # Task breakdown
├── history/
│   ├── prompts/              # Prompt History Records
│   └── adr/                  # Architecture Decision Records
├── DATABASE-SETUP.md         # Database setup guide
├── PROJECT-SUMMARY.md        # Project summary
└── README.md                 # This file
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create account
- `POST /api/auth/signin` - Sign in

### Tasks
- `GET /api/{user_id}/tasks` - List tasks
- `POST /api/{user_id}/tasks` - Create task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion
- `DELETE /api/{user_id}/tasks/{id}` - Delete task

### Health
- `GET /health` - Health check

## User Stories

All 6 user stories are complete:

1. ✅ **Authentication** - Sign up, sign in with JWT
2. ✅ **View Task List** - List and filter tasks
3. ✅ **Add Task** - Create new tasks
4. ✅ **Mark Complete** - Toggle completion status
5. ✅ **Update Task** - Edit task details
6. ✅ **Delete Task** - Remove tasks with confirmation

## Development Workflow

This project follows:
- **Test-Driven Development (TDD)**: Tests written before implementation
- **Spec-Driven Development (SDD)**: Specifications guide implementation
- **RED-GREEN-REFACTOR**: TDD cycle for all features

## Testing

- **Backend**: 65 test cases covering all endpoints
- **Coverage**: Authentication, CRUD operations, user isolation, validation
- **Framework**: pytest with async support

Run tests:
```bash
pytest                    # All tests
pytest -v                 # Verbose output
pytest --cov=app          # With coverage
```

## Security

- JWT token authentication
- Password hashing with bcrypt
- User isolation on all endpoints
- Input validation
- CORS configuration
- No hardcoded secrets

## Documentation

- [DATABASE-SETUP.md](DATABASE-SETUP.md) - Database setup guide
- [PROJECT-SUMMARY.md](PROJECT-SUMMARY.md) - Complete project summary
- [specs/phase-2-web-app/spec.md](specs/phase-2-web-app/spec.md) - Feature specification
- [specs/phase-2-web-app/plan.md](specs/phase-2-web-app/plan.md) - Implementation plan
- [specs/phase-2-web-app/tasks.md](specs/phase-2-web-app/tasks.md) - Task breakdown

## Next Steps

1. **Set up database** - Follow DATABASE-SETUP.md
2. **Run tests** - Verify all functionality works
3. **Test manually** - Try all features in browser
4. **Deploy** - Deploy to production (Vercel + Railway/Render)

## Contributing

This project follows Spec-Driven Development methodology. See `.specify/memory/constitution.md` for coding standards and principles.

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check DATABASE-SETUP.md for setup issues
2. Check PROJECT-SUMMARY.md for architecture details
3. Review test cases for expected behavior
4. Check API documentation in code comments

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Neon](https://neon.tech/)
- [Tailwind CSS](https://tailwindcss.com/)
