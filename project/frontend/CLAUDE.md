# Frontend Development Guide

## Context
This is the Next.js 16+ frontend for the Todo Evolution Phase 2 project. It uses the App Router, TypeScript, Tailwind CSS, and Better Auth for authentication.

## Technology Stack
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS 3.x
- **Authentication**: Better Auth with JWT tokens
- **HTTP Client**: fetch API (native)
- **State Management**: React hooks and Server Components

## Project Structure
```
frontend/
├── app/                      # Next.js App Router
│   ├── (auth)/              # Auth route group (signin, signup)
│   ├── (dashboard)/         # Protected route group (tasks)
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Home page
├── components/              # React components
│   ├── ui/                  # Reusable UI components
│   ├── TaskList.tsx
│   ├── TaskItem.tsx
│   ├── TaskForm.tsx
│   └── AuthForm.tsx
├── lib/                     # Utilities and services
│   ├── api.ts              # API client for backend
│   ├── auth.ts             # Better Auth configuration
│   └── types.ts            # TypeScript types
└── public/                 # Static assets
```

## Development Commands
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint

# Run type checking
npx tsc --noEmit

# Run tests
npm test
```

## Environment Variables
Copy `.env.local.example` to `.env.local` and configure:
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)
- `BETTER_AUTH_SECRET`: Shared secret for JWT (must match backend)
- `BETTER_AUTH_URL`: Frontend URL (default: http://localhost:3000)

## Code Standards

### Component Patterns
- **Server Components**: Default for all components (no 'use client')
- **Client Components**: Only when needed (interactivity, hooks, browser APIs)
- Mark client components with 'use client' directive at top of file
- Prefer composition over prop drilling

### Styling
- Use Tailwind CSS classes exclusively (no inline styles, no CSS modules)
- Follow mobile-first responsive design
- Use semantic color names from Tailwind palette
- Extract repeated patterns into reusable components

### TypeScript
- Strict mode enabled - all types must be explicit
- No `any` types (use `unknown` if truly dynamic)
- Define interfaces for all props and API responses
- Use type inference where possible

### API Integration
- All API calls go through `lib/api.ts` client
- Include JWT token in Authorization header
- Handle loading states and errors gracefully
- Show user-friendly error messages

### Authentication
- Better Auth handles signup, signin, signout
- JWT tokens stored in HTTP-only cookies
- Protected routes check authentication status
- Redirect to signin if not authenticated

## Testing Strategy
- Unit tests for utility functions
- Component tests with React Testing Library
- Integration tests for authentication flow
- E2E tests with Playwright for critical paths

## Common Tasks

### Adding a New Page
1. Create page.tsx in appropriate route group
2. Use Server Component by default
3. Add loading.tsx for loading state
4. Add error.tsx for error boundary

### Adding a New Component
1. Create component file in components/
2. Add 'use client' if needs interactivity
3. Define TypeScript interface for props
4. Use Tailwind CSS for styling
5. Export as default or named export

### Making API Calls
1. Import API client from lib/api.ts
2. Use async/await pattern
3. Handle loading and error states
4. Update UI based on response

## Constitution Compliance
- Follow all standards in `.specify/memory/constitution.md`
- Ensure user isolation (users only see their own data)
- No hardcoded secrets or credentials
- Minimum 80% test coverage
- All changes must be minimal and focused

## Related Documentation
- Root: `../CLAUDE.md`
- Backend: `../backend/CLAUDE.md`
- Specification: `../specs/phase-2-web-app/spec.md`
- Implementation Plan: `../specs/phase-2-web-app/plan.md`
- Tasks: `../specs/phase-2-web-app/tasks.md`
