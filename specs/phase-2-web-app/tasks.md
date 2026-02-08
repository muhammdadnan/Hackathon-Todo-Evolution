---
description: "Task list for Phase 2 - Full-Stack Web Application implementation"
---

# Tasks: Phase 2 - Full-Stack Web Application

**Input**: Design documents from `/specs/phase-2-web-app/`
**Prerequisites**: plan.md (completed), spec.md (completed), constitution.md (completed)

**Tests**: Tests are MANDATORY per constitution - TDD approach with Red-Green-Refactor cycle

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/app/`, `frontend/app/`, `frontend/components/`
- Tests: `backend/tests/`, `frontend/__tests__/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create monorepo directory structure per plan.md (project/frontend/, project/backend/, project/specs/, project/history/)
- [ ] T002 Initialize Next.js 16+ frontend with TypeScript in project/frontend/ (npx create-next-app@latest)
- [ ] T003 [P] Initialize FastAPI backend with Python 3.11+ in project/backend/ (create pyproject.toml, requirements.txt)
- [ ] T004 [P] Configure Tailwind CSS in project/frontend/ (tailwind.config.js, globals.css)
- [ ] T005 [P] Create environment variable templates (.env.example for backend, .env.local.example for frontend)
- [ ] T006 [P] Create CLAUDE.md files (project/CLAUDE.md, project/frontend/CLAUDE.md, project/backend/CLAUDE.md)
- [ ] T007 [P] Create README.md files with setup instructions (project/README.md, project/frontend/README.md, project/backend/README.md)
- [ ] T008 Set up Neon PostgreSQL database and obtain connection string

**Checkpoint**: Project structure ready, dev servers can start

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [ ] T009 Create database configuration in project/backend/app/config.py (load env vars, validate settings)
- [ ] T010 Create database connection setup in project/backend/app/database.py (SQLModel engine, session management)
- [ ] T011 [P] Create base User model in project/backend/app/models/user.py (id, email, password, timestamps)
- [ ] T012 [P] Create base Task model in project/backend/app/models/task.py (id, user_id, title, description, completed, timestamps)
- [ ] T013 Create database initialization script in project/backend/app/database.py (create_db_and_tables function)
- [ ] T014 Create JWT utilities in project/backend/app/middleware/auth.py (verify_token, get_current_user functions)
- [ ] T015 Create JWT middleware in project/backend/app/middleware/auth.py (JWTBearer dependency)
- [ ] T016 Configure CORS middleware in project/backend/app/main.py (allow frontend origin)
- [ ] T017 Create FastAPI app instance in project/backend/app/main.py (with middleware, health check endpoint)
- [ ] T018 Create Pydantic schemas in project/backend/app/schemas/task.py (TaskCreate, TaskUpdate, TaskResponse)

### Frontend Foundation

- [ ] T019 [P] Configure Better Auth in project/frontend/lib/auth.ts (JWT plugin, shared secret)
- [ ] T020 [P] Create API client in project/frontend/lib/api.ts (axios/fetch with JWT headers, error handling)
- [ ] T021 [P] Create TypeScript types in project/frontend/lib/types.ts (User, Task, ApiResponse types)
- [ ] T022 [P] Create reusable UI components in project/frontend/components/ui/ (Button.tsx, Input.tsx, Card.tsx, Modal.tsx)
- [ ] T023 Create root layout in project/frontend/app/layout.tsx (Better Auth provider, Tailwind setup)
- [ ] T024 Create landing page in project/frontend/app/page.tsx (redirect to signin or tasks based on auth)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication and Session Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to sign up, sign in, and maintain authenticated sessions with JWT tokens

**Independent Test**: Create account → Sign in → Receive JWT token → Token included in API requests

### Tests for User Story 1 (RED - Write First, Ensure FAIL)

- [ ] T025 [P] [US1] Write test for user signup in project/backend/tests/test_auth.py (test_signup_success, test_signup_duplicate_email)
- [ ] T026 [P] [US1] Write test for user signin in project/backend/tests/test_auth.py (test_signin_success, test_signin_invalid_credentials)
- [ ] T027 [P] [US1] Write test for JWT token verification in project/backend/tests/test_auth.py (test_verify_valid_token, test_verify_invalid_token)
- [ ] T028 [P] [US1] Write test for protected endpoint access in project/backend/tests/test_auth.py (test_protected_endpoint_with_token, test_protected_endpoint_without_token)

**Checkpoint**: All tests written and FAILING (RED phase complete)

### Implementation for User Story 1 (GREEN - Make Tests Pass)

- [ ] T029 [US1] Implement password hashing utilities in project/backend/app/middleware/auth.py (hash_password, verify_password using passlib)
- [ ] T030 [US1] Implement JWT token generation in project/backend/app/middleware/auth.py (create_access_token function)
- [ ] T031 [US1] Create auth routes in project/backend/app/routes/auth.py (POST /api/auth/signup, POST /api/auth/signin)
- [ ] T032 [US1] Register auth routes in project/backend/app/main.py (include_router for auth)
- [ ] T033 [US1] Verify all US1 backend tests pass (GREEN phase complete)

- [ ] T034 [P] [US1] Create AuthForm component in project/frontend/components/AuthForm.tsx (reusable for signin/signup)
- [ ] T035 [P] [US1] Create signin page in project/frontend/app/(auth)/signin/page.tsx (use AuthForm, call Better Auth)
- [ ] T036 [P] [US1] Create signup page in project/frontend/app/(auth)/signup/page.tsx (use AuthForm, call Better Auth)
- [ ] T037 [US1] Implement auth state management in project/frontend/lib/auth.ts (useAuth hook, getSession function)
- [ ] T038 [US1] Test full authentication flow manually (signup → signin → JWT token → stored in session)

**Checkpoint**: User Story 1 fully functional - users can sign up, sign in, and receive JWT tokens

### Refactor for User Story 1 (REFACTOR - Improve Code Quality)

- [ ] T039 [US1] Extract validation logic to separate utilities in project/backend/app/utils/validation.py
- [ ] T040 [US1] Add error handling and user-friendly messages in project/frontend/components/AuthForm.tsx
- [ ] T041 [US1] Add loading states to auth forms in project/frontend/components/AuthForm.tsx

---

## Phase 4: User Story 2 - View Task List (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to view all their tasks in a list

**Independent Test**: Sign in → Navigate to tasks page → See list of tasks (or empty state)

### Tests for User Story 2 (RED - Write First, Ensure FAIL)

- [ ] T042 [P] [US2] Write test for GET /api/{user_id}/tasks in project/backend/tests/test_tasks.py (test_list_tasks_success, test_list_tasks_empty)
- [ ] T043 [P] [US2] Write test for user isolation in project/backend/tests/test_isolation.py (test_user_cannot_list_other_users_tasks)
- [ ] T044 [P] [US2] Write test for unauthorized access in project/backend/tests/test_tasks.py (test_list_tasks_without_token)

**Checkpoint**: All tests written and FAILING (RED phase complete)

### Implementation for User Story 2 (GREEN - Make Tests Pass)

- [ ] T045 [US2] Implement GET /api/{user_id}/tasks endpoint in project/backend/app/routes/tasks.py (list all tasks for user)
- [ ] T046 [US2] Add user_id validation in project/backend/app/routes/tasks.py (verify JWT user_id matches path user_id)
- [ ] T047 [US2] Register task routes in project/backend/app/main.py (include_router for tasks)
- [ ] T048 [US2] Verify all US2 backend tests pass (GREEN phase complete)

- [ ] T049 [P] [US2] Create TaskItem component in project/frontend/components/TaskItem.tsx (display single task)
- [ ] T050 [P] [US2] Create TaskList component in project/frontend/components/TaskList.tsx (map tasks to TaskItem)
- [ ] T051 [US2] Create tasks page in project/frontend/app/(dashboard)/tasks/page.tsx (fetch and display tasks)
- [ ] T052 [US2] Add empty state UI in project/frontend/components/TaskList.tsx (when no tasks exist)
- [ ] T053 [US2] Test task list display manually (create tasks in DB, verify they appear)

**Checkpoint**: User Story 2 fully functional - users can view their task list

### Refactor for User Story 2 (REFACTOR - Improve Code Quality)

- [ ] T054 [US2] Add loading skeleton in project/frontend/components/TaskList.tsx
- [ ] T055 [US2] Add error handling for API failures in project/frontend/app/(dashboard)/tasks/page.tsx
- [ ] T056 [US2] Extract task filtering logic to utility function in project/backend/app/routes/tasks.py

---

## Phase 5: User Story 3 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to create new tasks

**Independent Test**: Sign in → Click "Add Task" → Enter title/description → Task appears in list

### Tests for User Story 3 (RED - Write First, Ensure FAIL)

- [ ] T057 [P] [US3] Write test for POST /api/{user_id}/tasks in project/backend/tests/test_tasks.py (test_create_task_success, test_create_task_without_title)
- [ ] T058 [P] [US3] Write test for task validation in project/backend/tests/test_tasks.py (test_create_task_title_too_long, test_create_task_description_too_long)
- [ ] T059 [P] [US3] Write test for user isolation in project/backend/tests/test_isolation.py (test_task_created_with_correct_user_id)

**Checkpoint**: All tests written and FAILING (RED phase complete)

### Implementation for User Story 3 (GREEN - Make Tests Pass)

- [ ] T060 [US3] Implement POST /api/{user_id}/tasks endpoint in project/backend/app/routes/tasks.py (create new task)
- [ ] T061 [US3] Add input validation in project/backend/app/routes/tasks.py (title required, length limits)
- [ ] T062 [US3] Verify all US3 backend tests pass (GREEN phase complete)

- [ ] T063 [P] [US3] Create TaskForm component in project/frontend/components/TaskForm.tsx (create/edit form)
- [ ] T064 [US3] Add "Add Task" button and modal in project/frontend/app/(dashboard)/tasks/page.tsx
- [ ] T065 [US3] Implement form submission in project/frontend/components/TaskForm.tsx (call API, refresh list)
- [ ] T066 [US3] Add form validation in project/frontend/components/TaskForm.tsx (title required, length limits)
- [ ] T067 [US3] Test task creation manually (create task, verify it appears in list)

**Checkpoint**: User Story 3 fully functional - users can create new tasks

### Refactor for User Story 3 (REFACTOR - Improve Code Quality)

- [ ] T068 [US3] Add loading state during task creation in project/frontend/components/TaskForm.tsx
- [ ] T069 [US3] Add success/error toast notifications in project/frontend/components/TaskForm.tsx
- [ ] T070 [US3] Extract form validation to reusable utility in project/frontend/lib/validation.ts

---

## Phase 6: User Story 4 - Mark Task as Complete/Incomplete (Priority: P2)

**Goal**: Enable users to toggle task completion status

**Independent Test**: Sign in → View tasks → Click completion toggle → Status changes and persists

### Tests for User Story 4 (RED - Write First, Ensure FAIL)

- [ ] T071 [P] [US4] Write test for PATCH /api/{user_id}/tasks/{id}/complete in project/backend/tests/test_tasks.py (test_toggle_complete_success)
- [ ] T072 [P] [US4] Write test for user isolation in project/backend/tests/test_isolation.py (test_user_cannot_toggle_other_users_task)
- [ ] T073 [P] [US4] Write test for task not found in project/backend/tests/test_tasks.py (test_toggle_complete_task_not_found)

**Checkpoint**: All tests written and FAILING (RED phase complete)

### Implementation for User Story 4 (GREEN - Make Tests Pass)

- [ ] T074 [US4] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in project/backend/app/routes/tasks.py (toggle completion)
- [ ] T075 [US4] Add task ownership verification in project/backend/app/routes/tasks.py (ensure task belongs to user)
- [ ] T076 [US4] Verify all US4 backend tests pass (GREEN phase complete)

- [ ] T077 [US4] Add completion toggle UI in project/frontend/components/TaskItem.tsx (checkbox or button)
- [ ] T078 [US4] Implement toggle handler in project/frontend/components/TaskItem.tsx (call API, update UI)
- [ ] T079 [US4] Add visual distinction for completed tasks in project/frontend/components/TaskItem.tsx (strikethrough, opacity)
- [ ] T080 [US4] Test completion toggle manually (toggle task, refresh page, verify persistence)

**Checkpoint**: User Story 4 fully functional - users can mark tasks complete/incomplete

### Refactor for User Story 4 (REFACTOR - Improve Code Quality)

- [ ] T081 [US4] Add optimistic UI updates in project/frontend/components/TaskItem.tsx (update UI before API response)
- [ ] T082 [US4] Add error rollback in project/frontend/components/TaskItem.tsx (revert UI if API fails)

---

## Phase 7: User Story 5 - Update Task Details (Priority: P2)

**Goal**: Enable users to edit task title and description

**Independent Test**: Sign in → View tasks → Click "Edit" → Modify details → Changes saved

### Tests for User Story 5 (RED - Write First, Ensure FAIL)

- [ ] T083 [P] [US5] Write test for PUT /api/{user_id}/tasks/{id} in project/backend/tests/test_tasks.py (test_update_task_success)
- [ ] T084 [P] [US5] Write test for validation in project/backend/tests/test_tasks.py (test_update_task_empty_title)
- [ ] T085 [P] [US5] Write test for user isolation in project/backend/tests/test_isolation.py (test_user_cannot_update_other_users_task)

**Checkpoint**: All tests written and FAILING (RED phase complete)

### Implementation for User Story 5 (GREEN - Make Tests Pass)

- [ ] T086 [US5] Implement PUT /api/{user_id}/tasks/{id} endpoint in project/backend/app/routes/tasks.py (update task)
- [ ] T087 [US5] Add input validation in project/backend/app/routes/tasks.py (same as create)
- [ ] T088 [US5] Add task ownership verification in project/backend/app/routes/tasks.py
- [ ] T089 [US5] Verify all US5 backend tests pass (GREEN phase complete)

- [ ] T090 [US5] Add "Edit" button in project/frontend/components/TaskItem.tsx
- [ ] T091 [US5] Implement edit mode in project/frontend/components/TaskForm.tsx (pre-fill with existing data)
- [ ] T092 [US5] Implement update submission in project/frontend/components/TaskForm.tsx (call PUT endpoint)
- [ ] T093 [US5] Test task editing manually (edit task, verify changes persist)

**Checkpoint**: User Story 5 fully functional - users can edit task details

### Refactor for User Story 5 (REFACTOR - Improve Code Quality)

- [ ] T094 [US5] Add cancel button in edit mode in project/frontend/components/TaskForm.tsx
- [ ] T095 [US5] Add confirmation for unsaved changes in project/frontend/components/TaskForm.tsx

---

## Phase 8: User Story 6 - Delete Task (Priority: P3)

**Goal**: Enable users to delete tasks

**Independent Test**: Sign in → View tasks → Click "Delete" → Confirm → Task removed

### Tests for User Story 6 (RED - Write First, Ensure FAIL)

- [ ] T096 [P] [US6] Write test for DELETE /api/{user_id}/tasks/{id} in project/backend/tests/test_tasks.py (test_delete_task_success)
- [ ] T097 [P] [US6] Write test for user isolation in project/backend/tests/test_isolation.py (test_user_cannot_delete_other_users_task)
- [ ] T098 [P] [US6] Write test for task not found in project/backend/tests/test_tasks.py (test_delete_task_not_found)

**Checkpoint**: All tests written and FAILING (RED phase complete)

### Implementation for User Story 6 (GREEN - Make Tests Pass)

- [ ] T099 [US6] Implement DELETE /api/{user_id}/tasks/{id} endpoint in project/backend/app/routes/tasks.py (delete task)
- [ ] T100 [US6] Add task ownership verification in project/backend/app/routes/tasks.py
- [ ] T101 [US6] Verify all US6 backend tests pass (GREEN phase complete)

- [ ] T102 [US6] Add "Delete" button in project/frontend/components/TaskItem.tsx
- [ ] T103 [US6] Implement delete confirmation modal in project/frontend/components/TaskItem.tsx
- [ ] T104 [US6] Implement delete handler in project/frontend/components/TaskItem.tsx (call API, remove from list)
- [ ] T105 [US6] Test task deletion manually (delete task, verify it's removed)

**Checkpoint**: User Story 6 fully functional - users can delete tasks

### Refactor for User Story 6 (REFACTOR - Improve Code Quality)

- [ ] T106 [US6] Add undo functionality (optional enhancement) in project/frontend/components/TaskItem.tsx
- [ ] T107 [US6] Add bulk delete functionality (optional enhancement) in project/frontend/app/(dashboard)/tasks/page.tsx

---

## Phase 9: Integration & Testing

**Purpose**: Ensure all components work together seamlessly

- [ ] T108 [P] Run full test suite for backend (pytest project/backend/tests/)
- [ ] T109 [P] Run full test suite for frontend (npm test in project/frontend/)
- [ ] T110 Test complete user journey (signup → signin → create task → view → edit → complete → delete)
- [ ] T111 Test user isolation thoroughly (create two users, verify complete separation)
- [ ] T112 Test error scenarios (network errors, invalid tokens, expired tokens)
- [ ] T113 Test CORS configuration (verify frontend can communicate with backend)
- [ ] T114 [P] Run performance tests (API response times, frontend Lighthouse score)
- [ ] T115 [P] Run security tests (JWT validation, SQL injection prevention, XSS prevention)
- [ ] T116 Test browser compatibility (Chrome, Firefox, Safari)
- [ ] T117 Test responsive design (mobile, tablet, desktop)
- [ ] T118 Verify test coverage >80% (pytest-cov for backend, jest coverage for frontend)

**Checkpoint**: All integration tests passing, system ready for deployment

---

## Phase 10: Deployment Preparation

**Purpose**: Prepare application for production deployment

- [ ] T119 [P] Document all environment variables in project/README.md
- [ ] T120 [P] Create deployment checklist in project/docs/deployment-checklist.md
- [ ] T121 Configure production environment variables for backend (.env.production)
- [ ] T122 Configure production environment variables for frontend (.env.production)
- [ ] T123 Test backend deployment locally (Docker or similar)
- [ ] T124 Test frontend build (npm run build in project/frontend/)
- [ ] T125 Deploy backend to hosting service (Railway, Render, or Fly.io)
- [ ] T126 Deploy frontend to Vercel
- [ ] T127 Configure CORS for production frontend origin
- [ ] T128 Test production deployment (full user journey on deployed app)
- [ ] T129 Set up monitoring and logging (optional but recommended)
- [ ] T130 Create deployment documentation in project/README.md

**Checkpoint**: Application deployed and fully functional in production

---

## Phase 11: Polish & Documentation

**Purpose**: Final improvements and comprehensive documentation

- [ ] T131 [P] Update project README.md with complete setup instructions
- [ ] T132 [P] Update frontend README.md with development guide
- [ ] T133 [P] Update backend README.md with API documentation
- [ ] T134 [P] Create API documentation (OpenAPI/Swagger for FastAPI)
- [ ] T135 Add code comments for complex logic
- [ ] T136 Run code formatting (black for Python, prettier for TypeScript)
- [ ] T137 Run linting (ruff for Python, eslint for TypeScript)
- [ ] T138 Create demo video (under 90 seconds per hackathon requirements)
- [ ] T139 Prepare GitHub repository for submission (clean commit history, clear README)
- [ ] T140 Final review against constitution and spec requirements

**Checkpoint**: Project complete and ready for submission

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1 (Auth) must complete before US2-6 (requires authentication)
  - US2-6 can proceed sequentially in priority order after US1
- **Integration (Phase 9)**: Depends on all desired user stories being complete
- **Deployment (Phase 10)**: Depends on Integration phase passing
- **Polish (Phase 11)**: Depends on Deployment being successful

### User Story Dependencies

- **User Story 1 (P1 - Auth)**: Can start after Foundational (Phase 2) - BLOCKS all other stories
- **User Story 2 (P1 - View)**: Depends on US1 completion - Can proceed independently after
- **User Story 3 (P1 - Add)**: Depends on US1 completion - Can proceed independently after
- **User Story 4 (P2 - Complete)**: Depends on US1, US2, US3 - Enhances existing functionality
- **User Story 5 (P2 - Update)**: Depends on US1, US2, US3 - Enhances existing functionality
- **User Story 6 (P3 - Delete)**: Depends on US1, US2, US3 - Enhances existing functionality

### Within Each User Story

- Tests (RED) MUST be written and FAIL before implementation
- Implementation (GREEN) makes tests pass
- Refactor (REFACTOR) improves code quality without changing behavior
- Backend before frontend (API must exist before UI can call it)
- Core implementation before integration

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- All tests for a user story marked [P] can run in parallel
- Backend and frontend work can proceed in parallel once API contract is defined
- Integration tests marked [P] can run in parallel
- Documentation tasks marked [P] can run in parallel

---

## Implementation Strategy

### MVP First (Minimum Viable Product)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 2 (View Tasks)
5. Complete Phase 5: User Story 3 (Add Tasks)
6. **STOP and VALIDATE**: Test MVP (auth + view + add)
7. Deploy MVP if ready

### Full Feature Set

1. Complete MVP (Phases 1-5)
2. Add Phase 6: User Story 4 (Mark Complete)
3. Add Phase 7: User Story 5 (Update Tasks)
4. Add Phase 8: User Story 6 (Delete Tasks)
5. Complete Phase 9: Integration Testing
6. Complete Phase 10: Deployment
7. Complete Phase 11: Polish & Documentation

### TDD Workflow (Red-Green-Refactor)

For each user story:
1. **RED**: Write tests first, ensure they FAIL
2. **GREEN**: Write minimal code to make tests PASS
3. **REFACTOR**: Improve code quality while keeping tests GREEN
4. Commit after each cycle
5. Move to next user story

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [US#] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail (RED) before implementing (GREEN)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Follow constitution requirements strictly (security, testing, code quality)
- All API endpoints require JWT authentication
- User isolation must be enforced on every endpoint
- Minimum 80% test coverage required
- No hardcoded secrets allowed

---

## Estimated Effort

- **Phase 1 (Setup)**: 2-3 hours
- **Phase 2 (Foundational)**: 4-6 hours
- **Phase 3 (US1 - Auth)**: 6-8 hours
- **Phase 4 (US2 - View)**: 3-4 hours
- **Phase 5 (US3 - Add)**: 3-4 hours
- **Phase 6 (US4 - Complete)**: 2-3 hours
- **Phase 7 (US5 - Update)**: 2-3 hours
- **Phase 8 (US6 - Delete)**: 2-3 hours
- **Phase 9 (Integration)**: 3-4 hours
- **Phase 10 (Deployment)**: 2-3 hours
- **Phase 11 (Polish)**: 2-3 hours

**Total Estimated Effort**: 30-45 hours for complete implementation

**MVP Effort** (Phases 1-5): 18-25 hours
