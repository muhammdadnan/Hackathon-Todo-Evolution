# ADR-002: Better Auth for Authentication with JWT Tokens

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-02-08
- **Feature:** phase-2-web-app
- **Context:** Phase 2 requires secure user authentication with session management. Users must sign up, sign in, and maintain authenticated sessions. The backend API must verify user identity on every request. We need to decide on an authentication strategy that works across Next.js frontend and FastAPI backend.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - security-critical, affects all protected endpoints
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - Better Auth vs custom JWT vs Auth0 vs Clerk
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - affects frontend, backend, database, all API endpoints
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Use **Better Auth** on the Next.js frontend for user authentication with **JWT tokens** for API authorization. Better Auth handles user signup, signin, password hashing, and JWT token generation. The FastAPI backend verifies JWT tokens using a shared secret (BETTER_AUTH_SECRET) and extracts user identity for authorization.

**Authentication Stack:**
- **Frontend**: Better Auth library with JWT plugin
- **Token Format**: JWT (JSON Web Tokens) signed with HS256
- **Token Storage**: HTTP-only cookies (managed by Better Auth)
- **Backend Verification**: python-jose library for JWT validation
- **Password Hashing**: bcrypt (handled by Better Auth)
- **Shared Secret**: BETTER_AUTH_SECRET environment variable (minimum 32 characters)

**Authentication Flow:**
1. User submits credentials to Better Auth on frontend
2. Better Auth validates credentials, hashes password (signup) or verifies hash (signin)
3. Better Auth generates JWT token signed with BETTER_AUTH_SECRET
4. Frontend includes JWT in Authorization header for API requests
5. Backend middleware verifies JWT signature using same BETTER_AUTH_SECRET
6. Backend extracts user_id from JWT and enforces authorization

## Consequences

### Positive

- **Production-Ready**: Better Auth is a mature, well-tested authentication library with security best practices built-in
- **JWT Standard**: Industry-standard token format, widely supported, stateless authentication
- **Cross-Platform**: JWT tokens work seamlessly between JavaScript frontend and Python backend
- **Reduced Custom Code**: Don't need to implement password hashing, token generation, session management from scratch
- **Type Safety**: Better Auth provides TypeScript types for authentication state
- **Flexible**: Can add OAuth providers (Google, GitHub) later without major refactoring
- **Stateless Backend**: Backend doesn't need to store sessions, improving scalability
- **User Isolation**: JWT contains user_id, enabling strict user isolation on backend
- **Developer Experience**: Better Auth provides hooks and utilities for common auth patterns

### Negative

- **External Dependency**: Relying on Better Auth library for critical security functionality
- **Learning Curve**: Team must learn Better Auth API and configuration
- **JavaScript-Python Bridge**: Requires careful configuration to ensure JWT format is compatible between Better Auth (JS) and python-jose (Python)
- **Shared Secret Management**: BETTER_AUTH_SECRET must be kept secure and synchronized between frontend and backend
- **Token Expiration Handling**: Must implement token refresh logic if sessions need to last longer than token expiry
- **Limited Backend Control**: Backend cannot invalidate tokens (stateless JWT limitation) without additional infrastructure
- **Migration Risk**: If Better Auth is discontinued or has breaking changes, migration could be costly

## Alternatives Considered

### Alternative A: Custom JWT Implementation
**Approach**: Implement JWT generation and verification from scratch using libraries like jsonwebtoken (frontend) and python-jose (backend)

**Pros**:
- Full control over authentication logic
- No external authentication library dependency
- Can customize every aspect of token generation and validation
- Simpler mental model (just JWT, no abstraction layer)

**Cons**:
- Must implement password hashing, validation, session management manually
- Higher risk of security vulnerabilities (easy to get wrong)
- More code to write, test, and maintain
- Need to implement common patterns (password reset, email verification) from scratch
- Slower development time
- No built-in TypeScript types or React hooks

**Why Rejected**: Security is critical, and authentication is complex. Better Auth provides battle-tested implementations of security best practices. The time saved and reduced security risk outweigh the benefits of full control.

### Alternative B: Auth0 (Third-Party SaaS)
**Approach**: Use Auth0 for authentication, which handles everything in the cloud

**Pros**:
- Fully managed authentication service
- Enterprise-grade security and compliance
- Built-in OAuth providers, MFA, password reset, etc.
- No authentication code to maintain
- Excellent documentation and support
- Advanced features (anomaly detection, breached password detection)

**Cons**:
- External service dependency (requires internet, subject to outages)
- Cost (free tier limited, paid plans can be expensive)
- Vendor lock-in (hard to migrate away)
- Adds latency (extra network hop for authentication)
- Overkill for this project's requirements
- Requires Auth0 account and configuration
- Less control over user data

**Why Rejected**: Auth0 is excellent for production applications with complex requirements, but it's overkill for this hackathon project. The external dependency, cost, and setup complexity don't justify the benefits for our use case.

### Alternative C: Clerk (Third-Party SaaS)
**Approach**: Use Clerk for authentication, similar to Auth0 but more developer-friendly

**Pros**:
- Modern developer experience with great Next.js integration
- Beautiful pre-built UI components
- Generous free tier
- Excellent documentation
- Built-in user management dashboard
- Easy to set up

**Cons**:
- External service dependency
- Vendor lock-in
- Requires Clerk account
- Less control over authentication flow
- May have usage limits on free tier
- Adds external API calls to critical path

**Why Rejected**: While Clerk has excellent DX, it's still an external service with vendor lock-in. For a hackathon project where we want to demonstrate full-stack skills, using a self-hosted solution like Better Auth is more appropriate.

### Alternative D: NextAuth.js
**Approach**: Use NextAuth.js (now Auth.js) for authentication

**Pros**:
- Designed specifically for Next.js
- Open source and widely used
- Supports many OAuth providers
- Good documentation
- Active community

**Cons**:
- Primarily designed for OAuth, less ideal for email/password
- Requires database adapter configuration
- More complex setup than Better Auth
- Heavier abstraction layer
- May be overkill for simple email/password auth

**Why Rejected**: NextAuth.js is excellent for OAuth-heavy applications, but Better Auth is simpler and more focused for our email/password use case. Better Auth has a lighter footprint and easier configuration.

### Alternative E: Supabase Auth
**Approach**: Use Supabase for authentication and database

**Pros**:
- Integrated authentication and database
- Good developer experience
- Generous free tier
- Built-in row-level security

**Cons**:
- Would require switching from Neon to Supabase for database
- External service dependency
- Vendor lock-in
- Less control over backend implementation
- Conflicts with requirement to use FastAPI backend

**Why Rejected**: Supabase is a full backend-as-a-service, which conflicts with our requirement to build a FastAPI backend. We need a solution that works with our existing architecture.

## References

- Feature Spec: [specs/phase-2-web-app/spec.md](../../specs/phase-2-web-app/spec.md) - Section: Authentication Requirements
- Implementation Plan: [specs/phase-2-web-app/plan.md](../../specs/phase-2-web-app/plan.md) - Section: Authentication Flow
- Related ADRs: ADR-001 (Monorepo Structure)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) - Section II: Security-First Development
- Better Auth Documentation: https://www.better-auth.com/
- python-jose Documentation: https://python-jose.readthedocs.io/
