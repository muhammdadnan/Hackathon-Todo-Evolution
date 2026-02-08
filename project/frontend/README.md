# Frontend - Next.js Todo Application

Modern Next.js 16+ frontend with App Router, TypeScript, Tailwind CSS, and Better Auth authentication.

## Technology Stack

- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS 3.x
- **Authentication**: Better Auth with JWT tokens
- **HTTP Client**: Native fetch API
- **State Management**: React hooks and Server Components

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running (see `../backend/README.md`)

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.local.example .env.local

# Edit .env.local with your configuration
# IMPORTANT: BETTER_AUTH_SECRET must match backend
```

### Environment Variables

Create `.env.local` with the following variables:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-long
BETTER_AUTH_URL=http://localhost:3000

# Environment
NEXT_PUBLIC_ENVIRONMENT=development
```

### Development

```bash
# Run development server
npm run dev

# Open browser
# http://localhost:3000
```

### Build for Production

```bash
# Build application
npm run build

# Start production server
npm start
```

## Project Structure

```
frontend/
├── app/                      # Next.js App Router
│   ├── (auth)/              # Auth route group
│   │   ├── signin/          # Sign in page
│   │   └── signup/          # Sign up page
│   ├── (dashboard)/         # Protected route group
│   │   └── tasks/           # Task list page
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Home page
├── components/              # React components
│   ├── ui/                  # Reusable UI components
│   ├── TaskList.tsx
│   ├── TaskItem.tsx
│   ├── TaskForm.tsx
│   └── AuthForm.tsx
├── lib/                     # Utilities and services
│   ├── api.ts              # API client
│   ├── auth.ts             # Better Auth config
│   └── types.ts            # TypeScript types
└── public/                 # Static assets
```

## Available Scripts

```bash
# Development
npm run dev              # Start dev server
npm run build            # Build for production
npm start                # Start production server

# Code Quality
npm run lint             # Run ESLint
npx tsc --noEmit        # Type checking

# Testing
npm test                 # Run tests
npm run test:watch      # Run tests in watch mode
npm run test:coverage   # Run tests with coverage
```

## Features

- User authentication (signup, signin, signout)
- Task list view with real-time updates
- Create new tasks
- Edit existing tasks
- Mark tasks as complete/incomplete
- Delete tasks
- Responsive design (mobile and desktop)
- Loading states and error handling
- Type-safe API integration

## Code Standards

### Component Patterns

- **Server Components**: Default for all components
- **Client Components**: Only when needed (mark with 'use client')
- Use TypeScript interfaces for all props
- Prefer composition over prop drilling

### Styling

- Use Tailwind CSS classes exclusively
- No inline styles or CSS modules
- Follow mobile-first responsive design
- Extract repeated patterns into reusable components

### TypeScript

- Strict mode enabled
- No `any` types
- Define interfaces for all props and API responses
- Use type inference where possible

## API Integration

All API calls go through the `lib/api.ts` client:

```typescript
import { api } from '@/lib/api';

// List tasks
const tasks = await api.tasks.list(userId);

// Create task
const task = await api.tasks.create(userId, { title, description });

// Update task
const updated = await api.tasks.update(userId, taskId, { title, description });

// Toggle completion
const toggled = await api.tasks.toggleComplete(userId, taskId);

// Delete task
await api.tasks.delete(userId, taskId);
```

## Authentication Flow

1. User signs up or signs in via Better Auth
2. Better Auth generates JWT token
3. Token stored in HTTP-only cookie
4. Token included in Authorization header for API requests
5. Backend verifies token and extracts user_id

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
# - NEXT_PUBLIC_API_URL
# - BETTER_AUTH_SECRET
# - BETTER_AUTH_URL
```

### Other Platforms

Build the application and deploy the `.next` directory:

```bash
npm run build
# Deploy .next/ directory to your hosting platform
```

## Troubleshooting

### CORS Errors

Ensure backend CORS configuration includes your frontend URL:
```bash
# In backend/.env
CORS_ORIGINS=http://localhost:3000
```

### Authentication Issues

1. Verify `BETTER_AUTH_SECRET` matches between frontend and backend
2. Check JWT token is included in Authorization header
3. Verify backend is running and accessible

### Build Errors

```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Rebuild
npm run build
```

## Related Documentation

- Root README: `../README.md`
- Backend README: `../backend/README.md`
- Development Guide: `CLAUDE.md`
- Specification: `../specs/phase-2-web-app/spec.md`

## Support

For issues or questions, refer to the project documentation in `../specs/` and `../history/` directories.
