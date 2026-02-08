# ADR-003: SQLModel for Type-Safe ORM

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-02-08
- **Feature:** phase-2-web-app
- **Context:** Phase 2 backend requires database operations for user and task management. We need an ORM (Object-Relational Mapping) solution that provides type safety, integrates well with FastAPI, supports async operations, and works with PostgreSQL. The solution must enable efficient queries while preventing SQL injection and providing good developer experience.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - affects all database operations, data layer architecture
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - SQLModel vs SQLAlchemy vs Tortoise ORM vs Prisma
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - affects all models, queries, migrations, testing
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Use **SQLModel** as the ORM for the FastAPI backend. SQLModel combines SQLAlchemy's power with Pydantic's validation, providing type-safe database operations with excellent FastAPI integration.

**Data Layer Stack:**
- **ORM**: SQLModel 0.0.14+
- **Database Engine**: SQLAlchemy 2.x (SQLModel's foundation)
- **Database Driver**: asyncpg (async PostgreSQL driver)
- **Validation**: Pydantic 2.x (built into SQLModel)
- **Migrations**: Alembic (SQLAlchemy's migration tool)
- **Type Checking**: mypy with SQLModel plugin

**Key Features Used:**
- SQLModel models serve as both ORM models and Pydantic schemas
- Async session support for non-blocking database operations
- Automatic Pydantic validation on model creation
- Type hints for IDE autocomplete and static analysis
- Relationship definitions with type safety
- Query builder with type checking

## Consequences

### Positive

- **Type Safety**: Full type hints throughout data layer, catching errors at development time
- **Pydantic Integration**: Models automatically validate data, reducing boilerplate validation code
- **FastAPI Native**: Designed specifically for FastAPI, seamless integration with request/response models
- **Single Source of Truth**: One model definition serves as both database schema and API schema
- **Developer Experience**: Excellent IDE autocomplete, inline documentation, and error detection
- **Async Support**: Native async/await support for non-blocking database operations
- **SQL Injection Prevention**: Parameterized queries prevent SQL injection attacks
- **Simpler Than SQLAlchemy**: Cleaner API while maintaining SQLAlchemy's power under the hood
- **Migration Path**: Built on SQLAlchemy, so can drop down to raw SQLAlchemy when needed
- **Active Development**: Maintained by the FastAPI creator (Sebastián Ramírez)

### Negative

- **Younger Library**: Less mature than SQLAlchemy (v0.0.x), potential for breaking changes
- **Smaller Community**: Fewer Stack Overflow answers and third-party resources than SQLAlchemy
- **Limited Documentation**: Documentation is good but not as comprehensive as SQLAlchemy's
- **Learning Curve**: Developers must understand both SQLModel and underlying SQLAlchemy concepts
- **Abstraction Leaks**: Sometimes need to understand SQLAlchemy internals for complex queries
- **Migration Tooling**: Must use Alembic (SQLAlchemy's tool), which requires additional setup
- **Performance Overhead**: Pydantic validation adds slight overhead compared to raw SQLAlchemy
- **Relationship Complexity**: Complex relationships may require dropping down to SQLAlchemy

## Alternatives Considered

### Alternative A: Raw SQLAlchemy 2.x
**Approach**: Use SQLAlchemy directly without SQLModel abstraction

**Pros**:
- Most mature and battle-tested Python ORM
- Comprehensive documentation and large community
- Maximum flexibility and control
- No abstraction overhead
- Extensive ecosystem of plugins and extensions
- Well-understood by most Python developers

**Cons**:
- More boilerplate code (separate ORM models and Pydantic schemas)
- No automatic Pydantic validation
- Less type-safe (requires manual type hints)
- More verbose model definitions
- Steeper learning curve for complex features
- Need to manually sync ORM models with API schemas

**Why Rejected**: SQLModel provides all of SQLAlchemy's power with better type safety and less boilerplate. For a FastAPI project, SQLModel's integration benefits outweigh the maturity advantages of raw SQLAlchemy.

### Alternative B: Tortoise ORM
**Approach**: Use Tortoise ORM, an async-first ORM inspired by Django ORM

**Pros**:
- Designed for async from the ground up
- Django-like API (familiar to Django developers)
- Good performance with async operations
- Built-in migration support
- Simpler API than SQLAlchemy for basic operations

**Cons**:
- Smaller community than SQLAlchemy
- Less mature and fewer features
- Not as well integrated with FastAPI
- Separate Pydantic schemas still needed
- Less flexible for complex queries
- Fewer database backends supported
- No Pydantic integration

**Why Rejected**: Tortoise ORM doesn't provide the Pydantic integration that SQLModel offers. The Django-like API is nice, but the lack of FastAPI-specific features and Pydantic integration makes it less suitable for our use case.

### Alternative C: Prisma (Python Client)
**Approach**: Use Prisma ORM with Python client

**Pros**:
- Excellent developer experience
- Type-safe queries with autocomplete
- Automatic migrations from schema changes
- Great tooling (Prisma Studio for database browsing)
- Modern approach to ORM design
- Cross-language support (TypeScript, Python, Go)

**Cons**:
- Requires Node.js for Prisma CLI (adds dependency)
- Python client is less mature than TypeScript version
- Schema defined in separate Prisma schema language
- Less control over raw SQL when needed
- Larger runtime footprint
- Not as well integrated with FastAPI ecosystem
- Additional build step required

**Why Rejected**: Prisma is excellent, but requiring Node.js for a Python project adds unnecessary complexity. The separate schema language and less mature Python client make it less ideal than SQLModel for our FastAPI backend.

### Alternative D: Django ORM (with FastAPI)
**Approach**: Use Django ORM with FastAPI (possible but unusual)

**Pros**:
- Most mature Python ORM
- Excellent migration system
- Comprehensive documentation
- Large community
- Built-in admin interface

**Cons**:
- Designed for Django, not FastAPI
- Requires Django installation (heavy dependency)
- Synchronous by default (async support is limited)
- Not designed for FastAPI's async patterns
- Overkill for non-Django projects
- Awkward integration with FastAPI

**Why Rejected**: Django ORM is excellent within Django, but using it with FastAPI is awkward and adds unnecessary dependencies. It's not designed for FastAPI's async-first approach.

### Alternative E: Raw SQL with asyncpg
**Approach**: Write raw SQL queries using asyncpg driver directly

**Pros**:
- Maximum performance (no ORM overhead)
- Full control over SQL
- Simple mental model
- No ORM learning curve
- Smallest dependency footprint

**Cons**:
- No type safety for queries
- Manual SQL injection prevention
- Must write all CRUD operations manually
- No automatic schema migrations
- Verbose and repetitive code
- Error-prone (typos in SQL strings)
- No validation layer
- Must manually map SQL results to Python objects

**Why Rejected**: Raw SQL sacrifices too much developer experience and safety for marginal performance gains. The lack of type safety, validation, and migration tooling makes it unsuitable for a modern application.

## References

- Feature Spec: [specs/phase-2-web-app/spec.md](../../specs/phase-2-web-app/spec.md) - Section: Database Schema
- Implementation Plan: [specs/phase-2-web-app/plan.md](../../specs/phase-2-web-app/plan.md) - Section: Database Schema Design
- Related ADRs: ADR-001 (Monorepo Structure), ADR-002 (Better Auth)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) - Section V: Database Design Principles
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
