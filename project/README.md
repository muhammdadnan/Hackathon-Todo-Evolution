# Todo Evolution - Phase 2: Full-Stack Web Application

A modern full-stack todo application built with Next.js 16+, FastAPI, and PostgreSQL. Features secure authentication with JWT tokens, user isolation, and a responsive UI.

## Project Overview

This is Phase 2 of the Todo Evolution hackathon project, implementing a complete full-stack web application with:

- **Frontend**: Next.js 16+ with App Router, TypeScript, and Tailwind CSS
- **Backend**: Python FastAPI with SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens
- **Architecture**: Monorepo with separate frontend and backend

## Features

- ✅ User authentication (signup, signin, signout)
- ✅ Create, read, update, delete tasks
- ✅ Mark tasks as complete/incomplete
- ✅ User isolation (users only see their own tasks)
- ✅ Responsive design (mobile and desktop)
- ✅ Type-safe API with full TypeScript/Python type hints
- ✅ Comprehensive test coverage (>80%)

## Project Structure

```
project/
├── frontend/           # Next.js application
├── backend/            # FastAPI application
├── specs/              # Feature specifications
├── history/            # PHRs and ADRs
├── .specify/           # Spec-Kit configuration
└── README.md           # This file
```

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL database (Neon account recommended)
- Git

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd project

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

**Frontend** (`frontend/.env.local`):
```bash
cp frontend/.env.local.example frontend/.env.local
# Edit .env.local with your configuration
```

**Backend** (`backend/.env`):
```bash
cp backend/.env.example backend/.env
# Edit .env with your database URL and secrets
```

**Important**: Ensure `BETTER_AUTH_SECRET` matches in both frontend and backend.

### 3. Set Up Database

1. Create a Neon PostgreSQL database at https://neon.tech
2. Copy the connection string to `backend/.env` as `DATABASE_URL`
3. Run database migrations (once implemented):
   ```bash
   cd backend
   alembic upgrade head
   ```

### 4. Run Development Servers

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

**Access the application**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development Workflow

This project follows **Spec-Driven Development (SDD)** methodology:

1. **Specification** - Define requirements and acceptance criteria
2. **Planning** - Design architecture and technical approach
3. **Tasks** - Break down into atomic, testable units
4. **Implementation** - Follow TDD (Red-Green-Refactor) cycle
5. **Documentation** - Create PHRs and ADRs

### Running Tests

**Backend**:
```bash
cd backend
pytest                          # Run all tests
pytest --cov=app               # Run with coverage
pytest tests/test_auth.py      # Run specific test file
```

**Frontend**:
```bash
cd frontend
npm test                        # Run all tests
npm run test:watch             # Run in watch mode
```

### Code Quality

**Backend**:
```bash
cd backend
ruff check .                   # Linting
ruff format .                  # Formatting
mypy app/                      # Type checking
```

**Frontend**:
```bash
cd frontend
npm run lint                   # ESLint
npx tsc --noEmit              # Type checking
```

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

All endpoints (except health check) require JWT authentication via `Authorization: Bearer <token>` header.

## Documentation

- **Constitution**: `.specify/memory/constitution.md` - Project principles and standards
- **Specification**: `specs/phase-2-web-app/spec.md` - Feature requirements
- **Implementation Plan**: `specs/phase-2-web-app/plan.md` - Architecture and design
- **Tasks**: `specs/phase-2-web-app/tasks.md` - Task breakdown
- **ADRs**: `history/adr/` - Architecture Decision Records
- **Frontend Guide**: `frontend/CLAUDE.md` - Frontend development guide
- **Backend Guide**: `backend/CLAUDE.md` - Backend development guide

## Architecture Decision Records

Key architectural decisions documented in `history/adr/`:

1. **ADR-001**: Monorepo Structure - Single repository for frontend and backend
2. **ADR-002**: Better Auth with JWT - Authentication strategy
3. **ADR-003**: SQLModel ORM - Type-safe database operations
4. **ADR-004**: Next.js App Router - Modern routing with Server Components

## Deployment

### Frontend (Vercel)

```bash
cd frontend
npm run build
# Deploy to Vercel via CLI or GitHub integration
```

### Backend (Railway/Render/Fly.io)

```bash
cd backend
# Configure production environment variables
# Deploy via platform-specific CLI or GitHub integration
```

### Environment Variables for Production

Ensure all environment variables are configured in your deployment platform:
- Frontend: `NEXT_PUBLIC_API_URL`, `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`
- Backend: `DATABASE_URL`, `BETTER_AUTH_SECRET`, `CORS_ORIGINS`

## Security

- All passwords hashed with bcrypt
- JWT tokens signed with strong secret (minimum 32 characters)
- User isolation enforced on all endpoints
- CORS properly configured
- SQL injection prevention via SQLModel
- No secrets in source code

## Contributing

This project follows strict Spec-Driven Development methodology:

1. All changes must have a specification
2. All code must have tests (TDD approach)
3. Follow the constitution guidelines
4. Create PHRs for all work
5. Suggest ADRs for significant decisions

## License

[Your License Here]

## Support

For issues or questions, please refer to the documentation in `specs/` and `history/` directories.

---

**Built with Spec-Driven Development methodology using Spec-Kit Plus**
