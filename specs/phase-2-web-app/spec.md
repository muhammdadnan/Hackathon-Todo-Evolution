# Feature Specification: Phase 2 - Full-Stack Web Application

**Feature Branch**: `phase-2-web-app`
**Created**: 2026-02-08
**Status**: Draft
**Input**: User description: "Implement Phase 2 of the Hackathon II 'Evolution of Todo' project - a full-stack web application with Next.js 16+ (App Router) with Tailwind CSS frontend, Python FastAPI backend, SQLModel ORM, Neon Serverless PostgreSQL database, and Better Auth with JWT tokens. Implement all 5 basic features: Add Task, Delete Task, Update Task, View Task List, and Mark as Complete."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Authentication and Session Management (Priority: P1)

As a user, I need to sign up and sign in to the application so that I can securely access my personal todo list and ensure my tasks are private.

**Why this priority**: Authentication is foundational - without it, no other features can work properly. User isolation depends on authentication being implemented first.

**Independent Test**: Can be fully tested by creating an account, signing in, receiving a JWT token, and verifying the token is included in subsequent API requests. Delivers secure access to the application.

**Acceptance Scenarios**:

1. **Given** I am a new user, **When** I provide valid email and password on the signup page, **Then** my account is created and I am automatically signed in with a valid JWT token
2. **Given** I am an existing user, **When** I provide correct credentials on the signin page, **Then** I receive a valid JWT token and am redirected to my task list
3. **Given** I am signed in, **When** my JWT token expires, **Then** I am prompted to sign in again
4. **Given** I provide invalid credentials, **When** I attempt to sign in, **Then** I see an error message and remain on the signin page
5. **Given** I am signed in, **When** I sign out, **Then** my JWT token is invalidated and I am redirected to the signin page

---

### User Story 2 - View Task List (Priority: P1)

As a user, I need to view all my tasks in a list so that I can see what I need to do and track my progress.

**Why this priority**: Viewing tasks is the core read operation and must work before any other task operations make sense. This is the primary interface users interact with.

**Independent Test**: Can be fully tested by signing in and viewing the task list page, which displays all tasks belonging to the authenticated user. Delivers immediate value by showing the user's current tasks.

**Acceptance Scenarios**:

1. **Given** I am signed in with tasks in my list, **When** I navigate to the task list page, **Then** I see all my tasks displayed with title, description, completion status, and creation date
2. **Given** I am signed in with no tasks, **When** I navigate to the task list page, **Then** I see an empty state message prompting me to create my first task
3. **Given** I am signed in, **When** I view my task list, **Then** I only see tasks that belong to me (user isolation enforced)
4. **Given** I have both completed and pending tasks, **When** I view my task list, **Then** I can visually distinguish between completed and pending tasks
5. **Given** I am not signed in, **When** I attempt to access the task list page, **Then** I am redirected to the signin page

---

### User Story 3 - Add New Task (Priority: P1)

As a user, I need to create new tasks so that I can capture things I need to do.

**Why this priority**: Creating tasks is the primary write operation and essential for the application to be useful. Without this, users cannot populate their task list.

**Independent Test**: Can be fully tested by signing in, clicking "Add Task", entering task details, and verifying the new task appears in the list. Delivers immediate value by allowing users to capture their todos.

**Acceptance Scenarios**:

1. **Given** I am signed in, **When** I click "Add Task" and enter a title, **Then** a new task is created and appears in my task list
2. **Given** I am creating a task, **When** I provide both title and description, **Then** both are saved and displayed
3. **Given** I am creating a task, **When** I provide only a title (no description), **Then** the task is created successfully with an empty description
4. **Given** I am creating a task, **When** I submit without a title, **Then** I see a validation error and the task is not created
5. **Given** I am signed in, **When** I create a task, **Then** it is automatically associated with my user account and only I can see it

---

### User Story 4 - Mark Task as Complete/Incomplete (Priority: P2)

As a user, I need to mark tasks as complete or incomplete so that I can track my progress and know what I've accomplished.

**Why this priority**: Toggling completion status is a core todo list feature that provides immediate feedback and satisfaction. It's the primary way users interact with existing tasks.

**Independent Test**: Can be fully tested by creating a task, clicking the completion toggle, and verifying the task's visual state changes and the status persists. Delivers value by allowing users to track progress.

**Acceptance Scenarios**:

1. **Given** I have a pending task, **When** I click the completion checkbox/button, **Then** the task is marked as complete and visually updated
2. **Given** I have a completed task, **When** I click the completion checkbox/button, **Then** the task is marked as pending and visually updated
3. **Given** I toggle a task's completion status, **When** I refresh the page, **Then** the completion status persists
4. **Given** I mark a task as complete, **When** I view my task list, **Then** completed tasks are visually distinct from pending tasks
5. **Given** I am not the owner of a task, **When** I attempt to toggle its completion status, **Then** the operation is rejected (403 Forbidden)

---

### User Story 5 - Update Task Details (Priority: P2)

As a user, I need to edit my tasks so that I can correct mistakes or update information as my plans change.

**Why this priority**: Editing tasks is important for maintaining accurate information but is less critical than creating and viewing tasks. Users can work around this by deleting and recreating tasks if needed.

**Independent Test**: Can be fully tested by creating a task, clicking "Edit", modifying the title or description, and verifying the changes are saved. Delivers value by allowing users to maintain accurate task information.

**Acceptance Scenarios**:

1. **Given** I have a task, **When** I click "Edit" and modify the title, **Then** the updated title is saved and displayed
2. **Given** I have a task, **When** I click "Edit" and modify the description, **Then** the updated description is saved and displayed
3. **Given** I am editing a task, **When** I clear the title field, **Then** I see a validation error and the changes are not saved
4. **Given** I am editing a task, **When** I cancel the edit, **Then** my changes are discarded and the original task data is preserved
5. **Given** I am not the owner of a task, **When** I attempt to edit it, **Then** the operation is rejected (403 Forbidden)

---

### User Story 6 - Delete Task (Priority: P3)

As a user, I need to delete tasks so that I can remove items I no longer need and keep my list clean.

**Why this priority**: Deleting tasks is useful for list maintenance but is the least critical feature. Users can simply ignore tasks they no longer need if deletion isn't available.

**Independent Test**: Can be fully tested by creating a task, clicking "Delete", confirming the deletion, and verifying the task is removed from the list. Delivers value by allowing users to maintain a clean task list.

**Acceptance Scenarios**:

1. **Given** I have a task, **When** I click "Delete" and confirm, **Then** the task is permanently removed from my list
2. **Given** I click "Delete" on a task, **When** I cancel the confirmation dialog, **Then** the task is not deleted
3. **Given** I delete a task, **When** I refresh the page, **Then** the deleted task does not reappear
4. **Given** I am not the owner of a task, **When** I attempt to delete it, **Then** the operation is rejected (403 Forbidden)
5. **Given** I have multiple tasks, **When** I delete one task, **Then** only that specific task is removed and others remain

---

### Edge Cases

- What happens when a user's JWT token expires while they are actively using the application?
- How does the system handle concurrent updates to the same task from multiple browser tabs?
- What happens when the backend API is unreachable or returns an error?
- How does the system handle very long task titles or descriptions (e.g., 10,000 characters)?
- What happens when a user attempts to access another user's task by manipulating the URL?
- How does the system handle database connection failures?
- What happens when a user signs up with an email that already exists?
- How does the frontend handle slow network connections or API timeouts?

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication & Authorization
- **FR-001**: System MUST provide user signup functionality with email and password
- **FR-002**: System MUST provide user signin functionality with email and password
- **FR-003**: System MUST issue JWT tokens upon successful authentication using Better Auth
- **FR-004**: System MUST verify JWT tokens on all protected API endpoints
- **FR-005**: System MUST enforce user isolation - users can only access their own tasks
- **FR-006**: System MUST reject requests with missing or invalid JWT tokens (401 Unauthorized)
- **FR-007**: System MUST reject requests where JWT user_id does not match URL user_id (403 Forbidden)

#### Task Management
- **FR-008**: System MUST allow authenticated users to create new tasks with title (required) and description (optional)
- **FR-009**: System MUST allow authenticated users to view all their tasks
- **FR-010**: System MUST allow authenticated users to update task title and description
- **FR-011**: System MUST allow authenticated users to toggle task completion status
- **FR-012**: System MUST allow authenticated users to delete tasks
- **FR-013**: System MUST validate task title is not empty (1-200 characters)
- **FR-014**: System MUST limit task description to maximum 1000 characters
- **FR-015**: System MUST automatically set created_at timestamp when task is created
- **FR-016**: System MUST automatically update updated_at timestamp when task is modified

#### API Endpoints
- **FR-017**: System MUST provide GET /api/{user_id}/tasks endpoint to list all user's tasks
- **FR-018**: System MUST provide POST /api/{user_id}/tasks endpoint to create new task
- **FR-019**: System MUST provide GET /api/{user_id}/tasks/{id} endpoint to retrieve task details
- **FR-020**: System MUST provide PUT /api/{user_id}/tasks/{id} endpoint to update task
- **FR-021**: System MUST provide DELETE /api/{user_id}/tasks/{id} endpoint to delete task
- **FR-022**: System MUST provide PATCH /api/{user_id}/tasks/{id}/complete endpoint to toggle completion

#### Data Persistence
- **FR-023**: System MUST persist all task data to Neon Serverless PostgreSQL database
- **FR-024**: System MUST persist user authentication data using Better Auth
- **FR-025**: System MUST maintain referential integrity between users and tasks
- **FR-026**: System MUST ensure task data survives application restarts

#### User Interface
- **FR-027**: Frontend MUST be built with Next.js 16+ using App Router
- **FR-028**: Frontend MUST use Tailwind CSS for all styling (no inline styles)
- **FR-029**: Frontend MUST display loading states during API operations
- **FR-030**: Frontend MUST display error messages when operations fail
- **FR-031**: Frontend MUST provide visual distinction between completed and pending tasks
- **FR-032**: Frontend MUST be responsive and work on mobile and desktop devices

### Key Entities

- **User**: Represents an authenticated user of the system. Managed by Better Auth. Key attributes: user_id (unique identifier), email (unique), password (hashed), created_at timestamp.

- **Task**: Represents a todo item belonging to a user. Key attributes: id (unique identifier), user_id (foreign key to User), title (required, 1-200 chars), description (optional, max 1000 chars), completed (boolean, default false), created_at timestamp, updated_at timestamp. Relationship: Many tasks belong to one user.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete the full signup → signin → create task → view task → mark complete → delete task flow in under 3 minutes
- **SC-002**: All API endpoints respond within 500ms under normal load (single user)
- **SC-003**: User isolation is 100% enforced - no user can access another user's tasks through any means
- **SC-004**: All 5 basic features (Add, Delete, Update, View, Mark Complete) are fully functional and tested
- **SC-005**: Frontend successfully deploys to Vercel without errors
- **SC-006**: Backend successfully deploys and connects to Neon database without errors
- **SC-007**: JWT authentication flow works end-to-end with no security vulnerabilities
- **SC-008**: Application handles network errors gracefully with user-friendly error messages
- **SC-009**: All tests pass with minimum 80% code coverage
- **SC-010**: Application works correctly in Chrome, Firefox, and Safari browsers

### Technical Validation

- **TV-001**: All API endpoints return proper HTTP status codes (200, 201, 400, 401, 403, 404, 500)
- **TV-002**: Database schema includes proper indexes on user_id and frequently queried fields
- **TV-003**: No secrets or credentials are hardcoded in source code
- **TV-004**: CORS is properly configured to allow frontend origin
- **TV-005**: JWT tokens expire after reasonable time period (e.g., 7 days)
- **TV-006**: All database operations use SQLModel for type safety
- **TV-007**: All API requests/responses use proper Pydantic models for validation
- **TV-008**: Frontend uses TypeScript strict mode with no type errors
- **TV-009**: Tailwind CSS is properly configured and all styles use Tailwind classes
- **TV-010**: Better Auth is properly configured with shared secret between frontend and backend

## API Specification

### Authentication Endpoints (Managed by Better Auth)

Better Auth provides these endpoints automatically:
- POST /api/auth/signup - Create new user account
- POST /api/auth/signin - Authenticate user and receive JWT token
- POST /api/auth/signout - Invalidate JWT token

### Task Management Endpoints

#### GET /api/{user_id}/tasks
**Description**: List all tasks for authenticated user

**Authentication**: Required (JWT token in Authorization header)

**Path Parameters**:
- user_id (string): User identifier from JWT token

**Query Parameters**: None

**Response 200 OK**:
```json
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
```

**Response 401 Unauthorized**: Missing or invalid JWT token

**Response 403 Forbidden**: JWT user_id does not match path user_id

---

#### POST /api/{user_id}/tasks
**Description**: Create new task

**Authentication**: Required (JWT token in Authorization header)

**Path Parameters**:
- user_id (string): User identifier from JWT token

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response 201 Created**:
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-02-08T10:00:00Z",
  "updated_at": "2026-02-08T10:00:00Z"
}
```

**Response 400 Bad Request**: Invalid request body (e.g., missing title)

**Response 401 Unauthorized**: Missing or invalid JWT token

**Response 403 Forbidden**: JWT user_id does not match path user_id

---

#### GET /api/{user_id}/tasks/{id}
**Description**: Get task details

**Authentication**: Required (JWT token in Authorization header)

**Path Parameters**:
- user_id (string): User identifier from JWT token
- id (integer): Task identifier

**Response 200 OK**: Same as POST response

**Response 401 Unauthorized**: Missing or invalid JWT token

**Response 403 Forbidden**: JWT user_id does not match path user_id or task does not belong to user

**Response 404 Not Found**: Task does not exist

---

#### PUT /api/{user_id}/tasks/{id}
**Description**: Update task details

**Authentication**: Required (JWT token in Authorization header)

**Path Parameters**:
- user_id (string): User identifier from JWT token
- id (integer): Task identifier

**Request Body**:
```json
{
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples, bananas"
}
```

**Response 200 OK**: Updated task object

**Response 400 Bad Request**: Invalid request body

**Response 401 Unauthorized**: Missing or invalid JWT token

**Response 403 Forbidden**: JWT user_id does not match path user_id or task does not belong to user

**Response 404 Not Found**: Task does not exist

---

#### DELETE /api/{user_id}/tasks/{id}
**Description**: Delete task

**Authentication**: Required (JWT token in Authorization header)

**Path Parameters**:
- user_id (string): User identifier from JWT token
- id (integer): Task identifier

**Response 204 No Content**: Task successfully deleted

**Response 401 Unauthorized**: Missing or invalid JWT token

**Response 403 Forbidden**: JWT user_id does not match path user_id or task does not belong to user

**Response 404 Not Found**: Task does not exist

---

#### PATCH /api/{user_id}/tasks/{id}/complete
**Description**: Toggle task completion status

**Authentication**: Required (JWT token in Authorization header)

**Path Parameters**:
- user_id (string): User identifier from JWT token
- id (integer): Task identifier

**Request Body**: None (toggles current state)

**Response 200 OK**: Updated task object with toggled completion status

**Response 401 Unauthorized**: Missing or invalid JWT token

**Response 403 Forbidden**: JWT user_id does not match path user_id or task does not belong to user

**Response 404 Not Found**: Task does not exist

## Database Schema

### users table (Managed by Better Auth)
- id: string (primary key)
- email: string (unique, not null)
- password: string (hashed, not null)
- name: string (nullable)
- created_at: timestamp (not null)
- updated_at: timestamp (not null)

### tasks table
- id: integer (primary key, auto-increment)
- user_id: string (foreign key → users.id, not null)
- title: string (not null, max 200 chars)
- description: text (nullable, max 1000 chars)
- completed: boolean (not null, default false)
- created_at: timestamp (not null, default current_timestamp)
- updated_at: timestamp (not null, default current_timestamp, auto-update)

**Indexes**:
- tasks.user_id (for filtering by user)
- tasks.completed (for filtering by status)
- tasks.created_at (for sorting by date)

**Constraints**:
- Foreign key: tasks.user_id references users.id (on delete cascade)
- Check: length(title) >= 1 AND length(title) <= 200
- Check: description IS NULL OR length(description) <= 1000

## Non-Functional Requirements

### Performance
- **NFR-001**: API endpoints must respond within 500ms under normal load
- **NFR-002**: Frontend must achieve Lighthouse performance score > 80
- **NFR-003**: Database queries must use indexes for user_id filtering

### Security
- **NFR-004**: All passwords must be hashed using bcrypt or similar
- **NFR-005**: JWT tokens must be signed with strong secret (min 32 characters)
- **NFR-006**: HTTPS must be used in production
- **NFR-007**: CORS must be configured to allow only frontend origin
- **NFR-008**: SQL injection must be prevented through parameterized queries (SQLModel handles this)

### Reliability
- **NFR-009**: Application must handle database connection failures gracefully
- **NFR-010**: Application must handle network errors gracefully
- **NFR-011**: Application must validate all user inputs
- **NFR-012**: Application must log errors for debugging

### Usability
- **NFR-013**: UI must be responsive and work on mobile devices (min width 320px)
- **NFR-014**: Error messages must be user-friendly and actionable
- **NFR-015**: Loading states must be shown during async operations
- **NFR-016**: UI must follow consistent design patterns

## Out of Scope

The following features are explicitly out of scope for Phase 2:
- Task filtering and sorting
- Task priorities and tags
- Due dates and reminders
- Recurring tasks
- Task search functionality
- Multi-language support
- Voice commands
- Real-time collaboration
- Task sharing between users
- Email notifications
- Mobile native apps
- Offline support
- Task attachments
- Task comments
- Task history/audit log

## Dependencies

### External Services
- Neon Serverless PostgreSQL (database hosting)
- Vercel (frontend hosting - recommended)
- Better Auth (authentication library)

### Technology Stack
- Frontend: Next.js 16+, React, TypeScript, Tailwind CSS, Better Auth
- Backend: Python 3.11+, FastAPI, SQLModel, Pydantic, python-jose (JWT), passlib (password hashing)
- Database: PostgreSQL (via Neon)
- Development: Node.js 18+, Python 3.11+, npm/pnpm, pip/uv

## Risks and Mitigations

### Risk 1: Better Auth JWT Integration Complexity
**Impact**: High
**Probability**: Medium
**Mitigation**: Follow Better Auth documentation carefully, implement JWT verification middleware early, test authentication flow thoroughly before implementing other features.

### Risk 2: CORS Configuration Issues
**Impact**: Medium
**Probability**: High
**Mitigation**: Configure CORS properly in FastAPI from the start, test with actual frontend origin, document CORS settings clearly.

### Risk 3: User Isolation Vulnerabilities
**Impact**: Critical
**Probability**: Low
**Mitigation**: Implement comprehensive tests for user isolation, verify JWT user_id matches path user_id on every endpoint, conduct security review before deployment.

### Risk 4: Database Connection Issues
**Impact**: High
**Probability**: Low
**Mitigation**: Use connection pooling, implement retry logic, handle connection errors gracefully, test with Neon database early.

### Risk 5: Deployment Configuration
**Impact**: Medium
**Probability**: Medium
**Mitigation**: Document all environment variables clearly, test deployment process early, use deployment checklists.

## Acceptance Checklist

- [ ] All 5 basic features implemented and working
- [ ] User authentication with Better Auth and JWT tokens working
- [ ] All API endpoints implemented and tested
- [ ] User isolation enforced and tested
- [ ] Frontend deployed to Vercel successfully
- [ ] Backend deployed and connected to Neon database
- [ ] All tests passing with >80% coverage
- [ ] No hardcoded secrets in source code
- [ ] README with setup instructions complete
- [ ] Environment variables documented
- [ ] CORS properly configured
- [ ] Error handling implemented throughout
- [ ] Loading states implemented in UI
- [ ] Responsive design working on mobile and desktop
- [ ] Tailwind CSS properly configured
- [ ] TypeScript strict mode enabled with no errors
