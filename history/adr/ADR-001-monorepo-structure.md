# ADR-001: Monorepo Structure for Full-Stack Application

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-02-08
- **Feature:** phase-2-web-app
- **Context:** Phase 2 requires both a Next.js frontend and FastAPI backend. We need to decide whether to organize these as separate repositories (polyrepo) or a single repository (monorepo).

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - affects development workflow, deployment, versioning
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - monorepo vs polyrepo vs submodules
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - affects entire project organization
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Use a **monorepo structure** with separate `frontend/` and `backend/` directories at the project root, along with shared `specs/`, `history/`, and `.specify/` directories for documentation and specifications.

**Structure:**
```
project/
├── .specify/           # Spec-Kit configuration (shared)
├── specs/              # Feature specifications (shared)
├── history/            # PHRs and ADRs (shared)
├── frontend/           # Next.js application
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── package.json
├── backend/            # FastAPI application
│   ├── app/
│   ├── tests/
│   └── requirements.txt
├── CLAUDE.md           # Root instructions
└── README.md           # Project overview
```

**Rationale:**
- Single source of truth for all project code and documentation
- Easier for Claude Code to navigate and understand full context
- Coordinated versioning and releases
- Shared documentation (specs, ADRs, PHRs) in one place
- Simplified dependency management for shared tooling
- Atomic commits that span frontend and backend changes

## Consequences

### Positive

- **Unified Development Experience**: Developers (and Claude Code) can work on frontend and backend in a single workspace without switching repositories
- **Coordinated Changes**: API contract changes can be implemented in both frontend and backend in a single commit, ensuring consistency
- **Shared Documentation**: Specifications, ADRs, and PHRs are co-located with the code they describe, improving discoverability
- **Simplified Onboarding**: New developers clone one repository and have access to the entire system
- **Easier Refactoring**: Cross-cutting changes (e.g., renaming an API endpoint) can be done atomically across both layers
- **Single Issue Tracker**: All issues, PRs, and discussions happen in one place
- **Spec-Kit Integration**: All Spec-Driven Development artifacts (constitution, specs, plans, tasks, PHRs, ADRs) are naturally co-located

### Negative

- **Larger Repository Size**: Single repo contains all code, which may grow large over time (mitigated by Git's efficiency)
- **Build Complexity**: Need to manage separate build processes for frontend and backend (mitigated by clear directory separation)
- **Deployment Coordination**: Must deploy frontend and backend separately despite being in same repo (requires clear deployment scripts)
- **Access Control Limitations**: Cannot grant different teams access to only frontend or backend (not a concern for this project)
- **CI/CD Complexity**: Need to detect which part changed to run appropriate tests (mitigated by path-based CI triggers)

## Alternatives Considered

### Alternative A: Polyrepo (Separate Repositories)
**Structure**: `todo-frontend` and `todo-backend` as separate repositories

**Pros**:
- Clear separation of concerns
- Independent versioning and release cycles
- Smaller individual repositories
- Easier to grant different access permissions
- Simpler CI/CD (each repo has its own pipeline)

**Cons**:
- Harder for Claude Code to maintain context across repositories
- Coordinating changes requires multiple PRs and careful synchronization
- Shared documentation must be duplicated or live in a third repo
- More complex onboarding (clone multiple repos, understand relationships)
- API contract changes require coordination across repos
- Spec-Kit Plus documentation would be fragmented

**Why Rejected**: The coordination overhead and context-switching cost outweigh the benefits for a project of this size. Claude Code works more effectively with all context in one place.

### Alternative B: Git Submodules
**Structure**: Main repo with frontend and backend as submodules

**Pros**:
- Combines benefits of monorepo (single entry point) and polyrepo (independent repos)
- Can version frontend and backend independently
- Shared documentation in parent repo

**Cons**:
- Submodules are notoriously difficult to work with (complex Git commands)
- Easy to get into inconsistent states
- Poor developer experience
- Claude Code would struggle with submodule navigation
- Adds significant complexity for minimal benefit

**Why Rejected**: Submodules add complexity without solving the core coordination problem. The developer experience is poor, and the benefits don't justify the cost.

### Alternative C: Monorepo with Workspaces (Yarn/npm workspaces)
**Structure**: Monorepo with package manager workspaces for shared dependencies

**Pros**:
- All benefits of monorepo
- Can share JavaScript/TypeScript packages between frontend and backend
- Unified dependency management

**Cons**:
- Backend is Python, not JavaScript, so workspace benefits don't apply
- Adds unnecessary complexity for this project
- Requires additional tooling configuration

**Why Rejected**: Workspaces are designed for JavaScript monorepos with shared packages. Since our backend is Python, we don't benefit from workspace features. Simple directory separation is sufficient.

## References

- Feature Spec: [specs/phase-2-web-app/spec.md](../../specs/phase-2-web-app/spec.md)
- Implementation Plan: [specs/phase-2-web-app/plan.md](../../specs/phase-2-web-app/plan.md)
- Related ADRs: None (foundational decision)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) - Section VII: Monorepo Organization
