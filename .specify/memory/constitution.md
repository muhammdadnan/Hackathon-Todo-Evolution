# Todo Evolution - Phase 2 Constitution

## Core Principles

### I. Technology Stack Standards (NON-NEGOTIABLE)
**Frontend:**
- Next.js 16+ with App Router (mandatory)
- Tailwind CSS for styling (mandatory)
- TypeScript for type safety
- Better Auth for authentication with JWT tokens

**Backend:**
- Python FastAPI for REST API
- SQLModel as ORM
- Neon Serverless PostgreSQL as database
- JWT token verification for all protected endpoints

**Architecture:**
- Monorepo structure with separate frontend/ and backend/ directories
- Shared authentication secret (BETTER_AUTH_SECRET) between frontend and backend
- RESTful API design with user_id in URL paths

### II. Security-First Development (NON-NEGOTIABLE)
**Authentication & Authorization:**
- All API endpoints MUST require valid JWT tokens
- User isolation MUST be enforced - users only see their own tasks
- JWT tokens issued by Better Auth on frontend
- Backend verifies JWT signature using shared secret
- No hardcoded secrets - use environment variables only

**Data Protection:**
- All task operations filtered by authenticated user_id
- User_id from JWT must match user_id in URL path
- 401 Unauthorized for missing/invalid tokens
- 403 Forbidden for user_id mismatch

### III. Test-First Development (NON-NEGOTIABLE)
**Testing Requirements:**
- Unit tests for all business logic
- Integration tests for API endpoints
- Authentication flow tests (token generation, verification)
- User isolation tests (ensure users cannot access others' data)
- Red-Green-Refactor cycle strictly enforced

**Test Coverage:**
- Minimum 80% code coverage
- All API endpoints must have tests
- All authentication/authorization paths tested
- Error handling scenarios covered

### IV. API Design Standards
**Endpoint Structure:**
- Base path: `/api/{user_id}/tasks`
- RESTful conventions: GET (list/retrieve), POST (create), PUT (update), DELETE (remove), PATCH (partial update)
- Consistent response formats with proper HTTP status codes
- Error responses include descriptive messages

**Required Endpoints:**
- GET /api/{user_id}/tasks - List all tasks
- POST /api/{user_id}/tasks - Create new task
- GET /api/{user_id}/tasks/{id} - Get task details
- PUT /api/{user_id}/tasks/{id} - Update task
- DELETE /api/{user_id}/tasks/{id} - Delete task
- PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion

### V. Database Design Principles
**Schema Standards:**
- Every task MUST have user_id foreign key
- Timestamps (created_at, updated_at) on all entities
- Proper indexes on user_id and frequently queried fields
- Use SQLModel for type-safe database operations

**Data Integrity:**
- Foreign key constraints enforced
- NOT NULL constraints on required fields
- Default values where appropriate (e.g., completed=false)

### VI. Code Quality Standards
**Python (Backend):**
- Type hints required for all functions
- Async/await for database operations
- Pydantic models for request/response validation
- Proper error handling with HTTPException
- Follow PEP 8 style guidelines

**TypeScript/JavaScript (Frontend):**
- TypeScript strict mode enabled
- Server components by default, client components only when needed
- Proper error handling and loading states
- Tailwind CSS classes only (no inline styles)
- Component reusability and composition

### VII. Monorepo Organization
**Project Structure:**
```
project/
├── .specify/                 # Spec-Kit configuration
├── specs/                    # Specifications
├── history/                  # PHRs and ADRs
├── frontend/                 # Next.js app
│   ├── app/                  # Next.js App Router pages
│   ├── components/           # React components
│   ├── lib/                  # Utilities and API client
│   └── CLAUDE.md             # Frontend-specific instructions
├── backend/                  # FastAPI app
│   ├── main.py               # FastAPI entry point
│   ├── models.py             # SQLModel database models
│   ├── routes/               # API route handlers
│   ├── auth.py               # JWT verification middleware
│   └── CLAUDE.md             # Backend-specific instructions
├── CLAUDE.md                 # Root instructions
└── README.md
```

## Development Workflow

### Spec-Driven Development Process
1. **Specify** - Define requirements and acceptance criteria
2. **Plan** - Design architecture and technical approach
3. **Tasks** - Break down into atomic, testable units
4. **Red** - Write failing tests
5. **Green** - Implement to pass tests
6. **Refactor** - Improve code quality
7. **Document** - Create PHRs and suggest ADRs

### Implementation Rules
- No code without a specification
- No implementation without tasks
- No tasks without a plan
- No plan without requirements
- All changes must be minimal and focused
- Cite code references (file:line) in all modifications

## Deployment Standards

### Environment Configuration
**Frontend (.env.local):**
- NEXT_PUBLIC_API_URL - Backend API URL
- BETTER_AUTH_SECRET - Shared authentication secret
- BETTER_AUTH_URL - Frontend URL for Better Auth

**Backend (.env):**
- DATABASE_URL - Neon PostgreSQL connection string
- BETTER_AUTH_SECRET - Shared authentication secret (must match frontend)
- CORS_ORIGINS - Allowed frontend origins

### Deployment Targets
- Frontend: Vercel (recommended) or similar Next.js hosting
- Backend: Any Python hosting supporting FastAPI (Railway, Render, etc.)
- Database: Neon Serverless PostgreSQL

## Quality Gates

### Pre-Commit Checks
- All tests pass
- Type checking passes (mypy for Python, tsc for TypeScript)
- Linting passes (ruff for Python, eslint for TypeScript)
- No hardcoded secrets or credentials

### Pre-Deployment Checks
- Integration tests pass
- Authentication flow verified
- User isolation verified
- Environment variables documented
- README updated with setup instructions

## Governance

### Constitution Authority
- This constitution supersedes all other development practices
- All code reviews must verify compliance with these principles
- Amendments require documentation and approval
- Breaking changes require migration plan

### Architectural Decisions
- Significant architectural decisions must be documented as ADRs
- ADRs stored in history/adr/ directory
- ADR suggestions made during planning phase
- User approval required before creating ADRs

### Prompt History Records
- PHR created after every user request
- PHRs stored in history/prompts/ with appropriate routing
- All placeholders must be filled
- Prompt text captured verbatim (never truncated)

**Version**: 1.0.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-08
