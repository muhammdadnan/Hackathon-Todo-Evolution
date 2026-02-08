# Implementation Plan: Phase 2 - Full-Stack Web Application

**Branch**: `phase-2-web-app` | **Date**: 2026-02-08 | **Spec**: [specs/phase-2-web-app/spec.md](./spec.md)
**Input**: Feature specification from `/specs/phase-2-web-app/spec.md`

## Summary

Implement a full-stack web application for the Todo Evolution project with secure multi-user authentication and task management. The system consists of a Next.js 16+ frontend with Tailwind CSS, a Python FastAPI backend, SQLModel ORM for database operations, and Neon Serverless PostgreSQL for data persistence. Authentication is handled by Better Auth on the frontend, issuing JWT tokens that the backend verifies for all protected endpoints. The application enforces strict user isolation, ensuring each user can only access their own tasks.

**Technical Approach**: Monorepo structure with separate frontend and backend directories. Frontend uses Next.js App Router with server and client components, Better Auth for authentication, and Tailwind CSS for styling. Backend uses FastAPI with async endpoints, SQLModel for type-safe database operations, JWT middleware for authentication, and CORS configuration for frontend communication. Shared BETTER_AUTH_SECRET enables JWT verification across services.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.x with Node.js 18+
- Backend: Python 3.11+

**Primary Dependencies**:
- Frontend: Next.js 16+, React 18+, Tailwind CSS 3.x, Better Auth, TypeScript
- Backend: FastAPI 0.109+, SQLModel 0.0.14+, Pydantic 2.x, python-jose[cryptography] (JWT), passlib[bcrypt] (password hashing), asyncpg (PostgreSQL driver)

**Storage**:
- Neon Serverless PostgreSQL (cloud-hosted)
- Better Auth manages user authentication data
- Tasks table with foreign key to users

**Testing**:
- Frontend: Jest + React Testing Library for unit tests, Playwright for E2E tests
- Backend: pytest + pytest-asyncio for async tests, httpx for API testing
- Integration: Full authentication flow tests, user isolation tests

**Target Platform**:
- Frontend: Vercel (recommended) or any Next.js hosting
- Backend: Any Python hosting supporting FastAPI (Railway, Render, Fly.io)
- Database: Neon Serverless PostgreSQL (cloud)

**Project Type**: Web application (monorepo with frontend + backend)

**Performance Goals**:
- API response time: <500ms p95
- Frontend Lighthouse score: >80
- Database query time: <100ms for task operations
- JWT verification: <10ms

**Constraints**:
- User isolation must be 100% enforced (security critical)
- All API endpoints require valid JWT tokens
- No hardcoded secrets in source code
- CORS must be properly configured
- Minimum 80% test coverage

**Scale/Scope**:
- Initial: Single-user development and testing
- Target: Support 100+ concurrent users
- Database: ~1000 tasks per user expected
- 5 basic features (Add, Delete, Update, View, Mark Complete)

## Constitution Check

*GATE: Must pass before implementation. Re-check after design.*

### Technology Stack Standards ✓
- [x] Next.js 16+ with App Router - COMPLIANT
- [x] Tailwind CSS for styling - COMPLIANT
- [x] Python FastAPI for backend - COMPLIANT
- [x] SQLModel as ORM - COMPLIANT
- [x] Neon Serverless PostgreSQL - COMPLIANT
- [x] Better Auth with JWT tokens - COMPLIANT
- [x] Monorepo structure - COMPLIANT

### Security-First Development ✓
- [x] JWT authentication on all endpoints - PLANNED
- [x] User isolation enforced - PLANNED
- [x] No hardcoded secrets - PLANNED
- [x] Environment variables for configuration - PLANNED

### Test-First Development ✓
- [x] Unit tests for business logic - PLANNED
- [x] Integration tests for API endpoints - PLANNED
- [x] Authentication flow tests - PLANNED
- [x] User isolation tests - PLANNED
- [x] Minimum 80% coverage - PLANNED

### API Design Standards ✓
- [x] RESTful endpoint structure - COMPLIANT
- [x] All required endpoints defined - COMPLIANT
- [x] Consistent response formats - PLANNED
- [x] Proper HTTP status codes - PLANNED

### Database Design Principles ✓
- [x] user_id foreign key on tasks - PLANNED
- [x] Timestamps on all entities - PLANNED
- [x] Proper indexes - PLANNED
- [x] SQLModel for type safety - COMPLIANT

**GATE STATUS**: PASSED - All constitution requirements met

## Project Structure

### Documentation (this feature)

```text
specs/phase-2-web-app/
├── spec.md              # Feature specification (COMPLETED)
├── plan.md              # This file - implementation plan (IN PROGRESS)
└── tasks.md             # Task breakdown (NEXT - created by /sp.tasks)
```

### Source Code (monorepo root: project/)

```text
project/
├── .specify/                      # Spec-Kit configuration
│   ├── memory/
│   │   └── constitution.md        # Project constitution (COMPLETED)
│   ├── templates/                 # Spec-Kit templates
│   └── scripts/                   # Spec-Kit scripts
│
├── specs/                         # All specifications
│   └── phase-2-web-app/          # This feature's specs
│
├── history/                       # PHRs and ADRs
│   ├── prompts/
│   │   ├── constitution/         # Constitution-related PHRs
│   │   ├── phase-2-web-app/      # Feature-specific PHRs
│   │   └── general/              # General PHRs
│   └── adr/                      # Architecture Decision Records
│
├── frontend/                      # Next.js application
│   ├── app/                      # Next.js App Router
│   │   ├── (auth)/               # Auth route group
│   │   │   ├── signin/
│   │   │   │   └── page.tsx      # Sign in page
│   │   │   └── signup/
│   │   │       └── page.tsx      # Sign up page
│   │   ├── (dashboard)/          # Protected route group
│   │   │   └── tasks/
│   │   │       └── page.tsx      # Task list page
│   │   ├── layout.tsx            # Root layout
│   │   └── page.tsx              # Home/landing page
│   │
│   ├── components/               # React components
│   │   ├── ui/                   # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Card.tsx
│   │   │   └── Modal.tsx
│   │   ├── TaskList.tsx          # Task list component
│   │   ├── TaskItem.tsx          # Individual task component
│   │   ├── TaskForm.tsx          # Create/edit task form
│   │   └── AuthForm.tsx          # Sign in/up form
│   │
│   ├── lib/                      # Utilities and services
│   │   ├── api.ts                # API client for backend
│   │   ├── auth.ts               # Better Auth configuration
│   │   └── types.ts              # TypeScript types
│   │
│   ├── public/                   # Static assets
│   ├── .env.local.example        # Environment variables template
│   ├── next.config.js            # Next.js configuration
│   ├── tailwind.config.js        # Tailwind CSS configuration
│   ├── tsconfig.json             # TypeScript configuration
│   ├── package.json              # Dependencies
│   ├── CLAUDE.md                 # Frontend-specific instructions
│   └── README.md                 # Frontend setup instructions
│
├── backend/                       # FastAPI application
│   ├── app/                      # Application code
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── config.py             # Configuration management
│   │   ├── database.py           # Database connection
│   │   │
│   │   ├── models/               # SQLModel database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py           # User model (Better Auth)
│   │   │   └── task.py           # Task model
│   │   │
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   └── task.py           # Task schemas
│   │   │
│   │   ├── routes/               # API route handlers
│   │   │   ├── __init__.py
│   │   │   └── tasks.py          # Task CRUD endpoints
│   │   │
│   │   └── middleware/           # Middleware
│   │       ├── __init__.py
│   │       ├── auth.py           # JWT verification
│   │       └── cors.py           # CORS configuration
│   │
│   ├── tests/                    # Test suite
│   │   ├── conftest.py           # Pytest fixtures
│   │   ├── test_auth.py          # Authentication tests
│   │   ├── test_tasks.py         # Task endpoint tests
│   │   └── test_isolation.py    # User isolation tests
│   │
│   ├── alembic/                  # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── .env.example              # Environment variables template
│   ├── requirements.txt          # Python dependencies
│   ├── pyproject.toml            # Python project configuration
│   ├── CLAUDE.md                 # Backend-specific instructions
│   └── README.md                 # Backend setup instructions
│
├── CLAUDE.md                      # Root project instructions
└── README.md                      # Project overview and setup
```

**Structure Decision**: Web application monorepo structure selected. This structure enables:
1. Single repository for both frontend and backend (easier for Claude Code to navigate)
2. Shared documentation and specifications
3. Coordinated deployment and versioning
4. Clear separation of concerns between frontend and backend
5. Independent development and testing of each layer

## Architecture Design

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT BROWSER                          │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Next.js Frontend (Vercel)                    │ │
│  │                                                           │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │ │
│  │  │   Pages     │  │  Components  │  │  Better Auth   │  │ │
│  │  │ (App Router)│  │  (React)     │  │  (JWT Issue)   │  │ │
│  │  └─────────────┘  └──────────────┘  └────────────────┘  │ │
│  │         │                 │                   │          │ │
│  │         └─────────────────┴───────────────────┘          │ │
│  │                           │                              │ │
│  │                    ┌──────▼──────┐                       │ │
│  │                    │  API Client │                       │ │
│  │                    │ (with JWT)  │                       │ │
│  │                    └──────┬──────┘                       │ │
│  └───────────────────────────┼────────────────────────────┘ │
└────────────────────────────┼─────────────────────────────────┘
                             │ HTTPS + JWT Token
                             │
┌────────────────────────────▼─────────────────────────────────┐
│              FastAPI Backend (Railway/Render)                │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ CORS         │  │ JWT          │  │  Task Routes     │   │
│  │ Middleware   │→ │ Middleware   │→ │  (Protected)     │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
│                           │                    │             │
│                           │                    │             │
│                    ┌──────▼────────────────────▼──────┐      │
│                    │      SQLModel ORM                │      │
│                    │   (Type-safe queries)            │      │
│                    └──────────────┬───────────────────┘      │
└───────────────────────────────────┼──────────────────────────┘
                                    │ asyncpg
                                    │
┌───────────────────────────────────▼──────────────────────────┐
│           Neon Serverless PostgreSQL (Cloud)                 │
│                                                               │
│  ┌─────────────┐              ┌─────────────┐               │
│  │ users table │              │ tasks table │               │
│  │ (Better Auth)│◄─────────────│ (user_id FK)│               │
│  └─────────────┘              └─────────────┘               │
└───────────────────────────────────────────────────────────────┘
```

### Authentication Flow

```
1. User Sign Up/Sign In
   ┌──────────┐                    ┌──────────────┐
   │ Frontend │                    │ Better Auth  │
   │  Form    │───credentials────► │  (Frontend)  │
   └──────────┘                    └──────┬───────┘
                                          │
                                          │ Hash password
                                          │ Store in DB
                                          │ Generate JWT
                                          │
                                   ┌──────▼───────┐
                                   │  JWT Token   │
                                   │  (signed)    │
                                   └──────────────┘

2. API Request with JWT
   ┌──────────┐                    ┌──────────────┐
   │ Frontend │─Authorization:─────►│   Backend    │
   │  Client  │  Bearer <token>    │   FastAPI    │
   └──────────┘                    └──────┬───────┘
                                          │
                                          │ Verify JWT signature
                                          │ Extract user_id
                                          │ Match with URL user_id
                                          │
                                   ┌──────▼───────┐
                                   │  Authorized  │
                                   │   Request    │
                                   └──────────────┘

3. User Isolation Enforcement
   ┌──────────────────────────────────────────────┐
   │  JWT user_id: "user123"                      │
   │  URL path: /api/user123/tasks                │
   │                                              │
   │  ✓ Match → Proceed with request             │
   │  ✗ Mismatch → 403 Forbidden                 │
   │                                              │
   │  All DB queries filtered by user_id          │
   └──────────────────────────────────────────────┘
```

### Database Schema Design

```sql
-- users table (managed by Better Auth)
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,  -- bcrypt hashed
    name VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL CHECK (LENGTH(title) >= 1),
    description TEXT CHECK (description IS NULL OR LENGTH(description) <= 1000),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);

-- Composite index for common query pattern
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

### API Contract Details

#### Request/Response Flow

```
1. List Tasks
   GET /api/{user_id}/tasks
   Headers: Authorization: Bearer <jwt_token>

   Response 200:
   [
     {
       "id": 1,
       "user_id": "user123",
       "title": "Buy groceries",
       "description": "Milk, eggs, bread",
       "completed": false,
       "created_at": "2026-02-08T10:00:00Z",
       "updated_at": "2026-02-08T10:00:00Z"
     }
   ]

2. Create Task
   POST /api/{user_id}/tasks
   Headers: Authorization: Bearer <jwt_token>
   Body: {
     "title": "Buy groceries",
     "description": "Milk, eggs, bread"
   }

   Response 201: (same as task object above)

3. Update Task
   PUT /api/{user_id}/tasks/{id}
   Headers: Authorization: Bearer <jwt_token>
   Body: {
     "title": "Updated title",
     "description": "Updated description"
   }

   Response 200: (updated task object)

4. Toggle Complete
   PATCH /api/{user_id}/tasks/{id}/complete
   Headers: Authorization: Bearer <jwt_token>
   Body: (empty - toggles current state)

   Response 200: (task object with toggled completion)

5. Delete Task
   DELETE /api/{user_id}/tasks/{id}
   Headers: Authorization: Bearer <jwt_token>

   Response 204: (no content)
```

### Frontend Component Architecture

```
App Layout (layout.tsx)
│
├── Auth Pages (route group: (auth))
│   ├── Sign In Page
│   │   └── AuthForm (client component)
│   │       ├── Input components
│   │       └── Button component
│   │
│   └── Sign Up Page
│       └── AuthForm (client component)
│
└── Dashboard Pages (route group: (dashboard))
    └── Tasks Page
        ├── TaskList (server component)
        │   ├── Fetches tasks from API
        │   └── Maps to TaskItem components
        │
        ├── TaskItem (client component)
        │   ├── Display task details
        │   ├── Complete toggle button
        │   ├── Edit button → TaskForm modal
        │   └── Delete button → Confirmation
        │
        └── TaskForm (client component)
            ├── Create new task
            ├── Edit existing task
            └── Form validation
```

### Backend Middleware Stack

```
Request Flow:
1. CORS Middleware
   ↓ (validates origin)
2. JWT Middleware
   ↓ (verifies token, extracts user_id)
3. Route Handler
   ↓ (validates user_id match, processes request)
4. SQLModel ORM
   ↓ (executes type-safe query)
5. Database
   ↓ (returns data)
6. Response
```

## Implementation Phases

### Phase 0: Project Setup (Foundation)
**Goal**: Set up monorepo structure, install dependencies, configure tools

**Tasks**:
1. Create monorepo directory structure
2. Initialize frontend (Next.js 16+ with TypeScript)
3. Initialize backend (FastAPI with Python 3.11+)
4. Configure Tailwind CSS in frontend
5. Set up environment variable templates
6. Create CLAUDE.md files for each layer
7. Initialize git repository (if not exists)
8. Set up Neon PostgreSQL database

**Deliverables**:
- Working monorepo structure
- Frontend dev server runs
- Backend dev server runs
- Tailwind CSS configured
- Database connection established

### Phase 1: Backend Foundation (Red-Green-Refactor)
**Goal**: Implement backend API with authentication and task management

**Tasks**:
1. **RED**: Write tests for database models (User, Task)
2. **GREEN**: Implement SQLModel models with relationships
3. **REFACTOR**: Add indexes and constraints
4. **RED**: Write tests for JWT middleware
5. **GREEN**: Implement JWT verification middleware
6. **REFACTOR**: Extract configuration to config.py
7. **RED**: Write tests for task CRUD endpoints
8. **GREEN**: Implement task routes (GET, POST, PUT, DELETE, PATCH)
9. **REFACTOR**: Add error handling and validation
10. **RED**: Write user isolation tests
11. **GREEN**: Implement user_id validation in all endpoints
12. **REFACTOR**: Add logging and monitoring

**Deliverables**:
- All backend tests passing
- All API endpoints functional
- JWT authentication working
- User isolation enforced
- 80%+ test coverage

### Phase 2: Frontend Foundation (Red-Green-Refactor)
**Goal**: Implement frontend UI with authentication and task management

**Tasks**:
1. **RED**: Write tests for Better Auth configuration
2. **GREEN**: Configure Better Auth with JWT
3. **REFACTOR**: Extract auth utilities
4. **RED**: Write tests for API client
5. **GREEN**: Implement API client with JWT headers
6. **REFACTOR**: Add error handling and retries
7. **RED**: Write tests for auth forms
8. **GREEN**: Implement sign in/sign up pages
9. **REFACTOR**: Extract reusable form components
10. **RED**: Write tests for task components
11. **GREEN**: Implement task list, item, and form components
12. **REFACTOR**: Add loading states and error handling

**Deliverables**:
- All frontend tests passing
- Authentication flow working
- Task management UI functional
- Responsive design
- Tailwind CSS styling complete

### Phase 3: Integration & Testing
**Goal**: Ensure frontend and backend work together seamlessly

**Tasks**:
1. Test full authentication flow (signup → signin → JWT → API)
2. Test all task operations end-to-end
3. Test user isolation (cannot access other users' tasks)
4. Test error scenarios (network errors, invalid tokens, etc.)
5. Test CORS configuration
6. Performance testing (API response times)
7. Security testing (JWT validation, SQL injection prevention)
8. Browser compatibility testing

**Deliverables**:
- All integration tests passing
- No security vulnerabilities
- Performance goals met
- Cross-browser compatibility verified

### Phase 4: Deployment
**Goal**: Deploy frontend and backend to production

**Tasks**:
1. Configure environment variables for production
2. Deploy backend to hosting service (Railway/Render)
3. Deploy frontend to Vercel
4. Configure CORS for production origins
5. Test production deployment
6. Document deployment process
7. Create deployment checklist

**Deliverables**:
- Frontend deployed and accessible
- Backend deployed and accessible
- Database connected
- All features working in production
- Deployment documentation complete

## Risk Analysis and Mitigation

### Risk 1: Better Auth JWT Integration Complexity
**Impact**: High | **Probability**: Medium | **Phase**: 1-2

**Description**: Better Auth is a JavaScript library, and integrating its JWT tokens with a Python backend requires careful configuration of the shared secret and token format.

**Mitigation Strategy**:
1. Study Better Auth JWT documentation thoroughly before implementation
2. Implement JWT verification middleware early in Phase 1
3. Create comprehensive tests for token generation and verification
4. Use python-jose library for JWT handling (compatible with Better Auth)
5. Test with actual tokens from Better Auth before proceeding to other features

**Contingency Plan**: If Better Auth integration proves too complex, fall back to custom JWT implementation using FastAPI's OAuth2 with password flow.

### Risk 2: CORS Configuration Issues
**Impact**: Medium | **Probability**: High | **Phase**: 3

**Description**: CORS misconfigurations are common in full-stack applications and can block frontend-backend communication.

**Mitigation Strategy**:
1. Configure CORS in FastAPI from the start of Phase 1
2. Use environment variables for allowed origins
3. Test CORS with actual frontend origin (not just localhost)
4. Document CORS configuration clearly
5. Include CORS testing in integration tests

**Contingency Plan**: Use FastAPI's CORSMiddleware with detailed logging to debug issues. Consider using a proxy in development if CORS becomes blocking.

### Risk 3: User Isolation Vulnerabilities
**Impact**: Critical | **Probability**: Low | **Phase**: 1-3

**Description**: Security vulnerability where users could access other users' tasks through URL manipulation or token tampering.

**Mitigation Strategy**:
1. Implement user_id validation in JWT middleware
2. Verify JWT user_id matches URL user_id on every endpoint
3. Filter all database queries by authenticated user_id
4. Create comprehensive user isolation tests
5. Conduct security review before deployment
6. Use SQLModel's type safety to prevent SQL injection

**Contingency Plan**: If vulnerabilities are found, immediately patch and re-test. Consider adding rate limiting and request logging for security monitoring.

### Risk 4: Database Connection Issues
**Impact**: High | **Probability**: Low | **Phase**: 1, 4

**Description**: Neon database connection failures or performance issues could block development or production.

**Mitigation Strategy**:
1. Test Neon connection early in Phase 0
2. Use connection pooling (SQLModel/SQLAlchemy handles this)
3. Implement retry logic for transient failures
4. Add database health check endpoint
5. Monitor connection pool metrics

**Contingency Plan**: Have backup database option ready (local PostgreSQL for development, alternative cloud provider for production).

### Risk 5: Deployment Configuration Complexity
**Impact**: Medium | **Probability**: Medium | **Phase**: 4

**Description**: Multiple environment variables and configuration differences between development and production can cause deployment failures.

**Mitigation Strategy**:
1. Document all environment variables clearly
2. Create .env.example files for both frontend and backend
3. Use deployment checklists
4. Test deployment process in staging environment first
5. Automate deployment where possible

**Contingency Plan**: Maintain detailed deployment runbook. If automated deployment fails, fall back to manual deployment with step-by-step verification.

## Architectural Decision Records (ADRs) to Consider

Based on the significant architectural decisions in this plan, the following ADRs should be suggested to the user:

1. **ADR: Monorepo vs Separate Repositories**
   - Decision: Use monorepo structure
   - Rationale: Easier for Claude Code to navigate, coordinated versioning, shared documentation
   - Alternatives: Separate repos for frontend/backend
   - Trade-offs: Larger repo size, but better developer experience

2. **ADR: Better Auth vs Custom Authentication**
   - Decision: Use Better Auth for frontend authentication
   - Rationale: Production-ready, JWT support, reduces custom code
   - Alternatives: Custom JWT implementation, Auth0, Clerk
   - Trade-offs: Dependency on external library, but faster implementation

3. **ADR: SQLModel vs Raw SQLAlchemy**
   - Decision: Use SQLModel for ORM
   - Rationale: Type safety, Pydantic integration, simpler than SQLAlchemy
   - Alternatives: Raw SQLAlchemy, Tortoise ORM, Prisma
   - Trade-offs: Less mature than SQLAlchemy, but better DX

4. **ADR: App Router vs Pages Router**
   - Decision: Use Next.js App Router
   - Rationale: Modern approach, server components, better performance
   - Alternatives: Pages Router (older but stable)
   - Trade-offs: Newer API, but future-proof

## Success Metrics

### Technical Metrics
- [ ] All tests passing (unit, integration, E2E)
- [ ] Test coverage >80%
- [ ] API response time <500ms p95
- [ ] Frontend Lighthouse score >80
- [ ] Zero security vulnerabilities
- [ ] TypeScript strict mode with no errors
- [ ] All linting rules passing

### Functional Metrics
- [ ] All 5 basic features implemented and working
- [ ] User authentication flow complete
- [ ] User isolation 100% enforced
- [ ] All API endpoints functional
- [ ] Frontend deployed to Vercel
- [ ] Backend deployed and connected to database
- [ ] CORS properly configured
- [ ] Error handling throughout

### Documentation Metrics
- [ ] README with setup instructions
- [ ] Environment variables documented
- [ ] API documentation complete
- [ ] Deployment guide complete
- [ ] CLAUDE.md files for each layer
- [ ] PHRs created for all work
- [ ] ADRs created for significant decisions

## Next Steps

1. **Review this plan** with the user for approval
2. **Suggest ADRs** for the 4 architectural decisions identified
3. **Create tasks.md** using `/sp.tasks` command to break down implementation into atomic, testable tasks
4. **Begin Phase 0** (Project Setup) once tasks are approved
5. **Follow TDD cycle** (Red-Green-Refactor) for all implementation phases
6. **Create PHRs** after each significant work session
7. **Deploy and verify** in Phase 4

## Complexity Tracking

No constitution violations detected. All architectural decisions align with the established principles and standards.
