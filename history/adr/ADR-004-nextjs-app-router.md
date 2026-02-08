# ADR-004: Next.js App Router for Frontend Routing

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-02-08
- **Feature:** phase-2-web-app
- **Context:** Phase 2 requires a Next.js frontend with routing for authentication pages (signin, signup) and protected dashboard pages (task list). Next.js offers two routing systems: the newer App Router (introduced in Next.js 13, stable in 14+) and the traditional Pages Router. We need to decide which routing system to use for this project.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - affects frontend architecture, component patterns, data fetching
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - App Router vs Pages Router
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - affects all pages, layouts, routing, data fetching patterns
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Use **Next.js App Router** (introduced in Next.js 13, stable in 14+) for frontend routing instead of the traditional Pages Router. The App Router provides a modern, React Server Components-based architecture with improved performance, better developer experience, and future-proof patterns.

**Frontend Routing Stack:**
- **Router**: Next.js App Router (app/ directory)
- **Component Model**: React Server Components (default) + Client Components (when needed)
- **Layouts**: Nested layouts with app/layout.tsx
- **Route Groups**: Organize routes with (auth) and (dashboard) groups
- **Data Fetching**: Server-side by default, async components
- **Loading States**: loading.tsx files for automatic loading UI
- **Error Handling**: error.tsx files for error boundaries

**Directory Structure:**
```
frontend/app/
├── layout.tsx                    # Root layout
├── page.tsx                      # Home page
├── (auth)/                       # Auth route group
│   ├── signin/
│   │   └── page.tsx             # Sign in page
│   └── signup/
│       └── page.tsx             # Sign up page
└── (dashboard)/                  # Protected route group
    └── tasks/
        ├── page.tsx             # Task list page
        ├── loading.tsx          # Loading state
        └── error.tsx            # Error boundary
```

## Consequences

### Positive

- **React Server Components**: Default server-side rendering reduces JavaScript bundle size and improves performance
- **Improved Performance**: Automatic code splitting, streaming, and progressive rendering
- **Better Developer Experience**: Simpler data fetching (async components), no need for getServerSideProps/getStaticProps
- **Nested Layouts**: Shared layouts reduce code duplication and improve UX (persistent navigation)
- **Route Groups**: Organize routes logically without affecting URL structure
- **Built-in Loading States**: loading.tsx provides automatic loading UI during navigation
- **Built-in Error Handling**: error.tsx provides automatic error boundaries
- **Future-Proof**: App Router is the future of Next.js, Pages Router is in maintenance mode
- **Streaming**: Progressive rendering improves perceived performance
- **Simplified API**: Fewer concepts to learn (no getServerSideProps, getStaticProps, getInitialProps)
- **Better TypeScript Support**: Improved type inference for server components

### Negative

- **Newer API**: Less mature than Pages Router, fewer Stack Overflow answers
- **Learning Curve**: Server Components paradigm requires mental model shift
- **Client Component Boundaries**: Must explicitly mark client components with 'use client'
- **Ecosystem Compatibility**: Some libraries don't work well with Server Components yet
- **Debugging Complexity**: Server/client boundary can be confusing for debugging
- **Migration Path**: If we need to migrate to Pages Router later, it would be significant work
- **Documentation Gaps**: Some edge cases not well documented yet
- **Third-Party Libraries**: Some React libraries assume client-side rendering

## Alternatives Considered

### Alternative A: Next.js Pages Router
**Approach**: Use the traditional Pages Router (pages/ directory)

**Pros**:
- More mature and battle-tested (used since Next.js 9)
- Larger community and more Stack Overflow answers
- Better third-party library compatibility
- Simpler mental model (all components are client components)
- More documentation and tutorials available
- Easier to find developers familiar with it
- No server/client component boundary confusion

**Cons**:
- Older architecture, in maintenance mode
- Less performant (larger JavaScript bundles)
- More boilerplate (getServerSideProps, getStaticProps)
- No React Server Components benefits
- No streaming or progressive rendering
- Layouts require custom _app.tsx patterns
- Not the future direction of Next.js
- Missing modern features (route groups, parallel routes)

**Why Rejected**: While Pages Router is more mature, App Router represents the future of Next.js and React. The performance benefits, improved DX, and future-proofing outweigh the maturity advantages. Since this is a new project, we should start with the modern approach rather than using legacy patterns.

### Alternative B: React Router (without Next.js)
**Approach**: Use Create React App or Vite with React Router for client-side routing

**Pros**:
- Full control over routing logic
- No framework lock-in
- Simpler deployment (static files)
- Smaller learning curve for React developers
- More flexible routing patterns

**Cons**:
- No server-side rendering (worse SEO and initial load)
- No automatic code splitting
- Must implement data fetching patterns manually
- No built-in API routes
- More configuration required
- Loses Next.js benefits (image optimization, font optimization, etc.)
- Conflicts with requirement to use Next.js 16+

**Why Rejected**: The project requirements explicitly specify Next.js 16+. Additionally, Next.js provides significant benefits (SSR, automatic code splitting, image optimization) that would be lost with a pure React Router approach.

### Alternative C: Remix
**Approach**: Use Remix framework instead of Next.js

**Pros**:
- Excellent data loading patterns (loaders and actions)
- Built-in form handling
- Progressive enhancement by default
- Great developer experience
- Nested routing with layouts
- Good error handling

**Cons**:
- Conflicts with requirement to use Next.js 16+
- Different ecosystem and deployment targets
- Smaller community than Next.js
- Would require learning a different framework
- Less mature than Next.js

**Why Rejected**: The project requirements explicitly specify Next.js 16+. While Remix is excellent, we must use Next.js for this project.

### Alternative D: App Router with Pages Router Hybrid
**Approach**: Use both App Router and Pages Router in the same project (Next.js supports this)

**Pros**:
- Can use App Router for new features, Pages Router for compatibility
- Gradual migration path
- Best of both worlds

**Cons**:
- Confusing mental model (two routing systems)
- Inconsistent patterns across codebase
- More complex to maintain
- Harder for new developers to understand
- Unnecessary complexity for a new project

**Why Rejected**: For a new project, using a hybrid approach adds unnecessary complexity. We should commit to one routing system. Since App Router is the future, we should use it exclusively.

## References

- Feature Spec: [specs/phase-2-web-app/spec.md](../../specs/phase-2-web-app/spec.md) - Section: User Interface Requirements
- Implementation Plan: [specs/phase-2-web-app/plan.md](../../specs/phase-2-web-app/plan.md) - Section: Frontend Component Architecture
- Related ADRs: ADR-001 (Monorepo Structure)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) - Section I: Technology Stack Standards
- Next.js App Router Documentation: https://nextjs.org/docs/app
- React Server Components: https://react.dev/reference/rsc/server-components
