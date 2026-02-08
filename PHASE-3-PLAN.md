# Phase 3 - AI Chatbot Architecture Plan

## Overview
Add AI chatbot interface to Phase 2 Todo App with full task management integration.

## Design Decisions

### 1. AI Integration: Mock Responses
- Pre-programmed intelligent responses
- Pattern matching for task commands
- No API keys needed
- Instant responses
- Perfect for demo

### 2. Chat Features
- **Create tasks**: "Create a task to buy groceries"
- **Query tasks**: "What are my pending tasks?"
- **Update tasks**: "Mark task 1 as complete"
- **Delete tasks**: "Delete the grocery task"
- **General help**: "What can you do?"

### 3. UI Components
```
ChatPage
├── ChatWindow
│   ├── MessageList
│   │   └── MessageBubble (user/ai)
│   └── MessageInput
└── TaskQuickView (sidebar)
```

### 4. State Management
- Chat messages in component state
- Task operations use existing API
- Real-time task updates reflected in chat

### 5. Mock AI Logic
```typescript
// Pattern matching
"create task" → Parse and create task
"show tasks" → Query and display tasks
"mark complete" → Update task status
"delete task" → Remove task
"help" → Show capabilities
```

## Implementation Steps

### Step 1: Create Chat Components (15 min)
- ChatWindow.tsx
- MessageList.tsx
- MessageBubble.tsx
- MessageInput.tsx

### Step 2: Add Mock AI Service (10 min)
- lib/mockAI.ts
- Pattern matching logic
- Task command parsing
- Response generation

### Step 3: Integrate with Tasks (10 min)
- Connect to existing task API
- Real-time updates
- Error handling

### Step 4: Add Chat Route (5 min)
- app/(dashboard)/chat/page.tsx
- Navigation from tasks page

### Step 5: Deploy to Vercel (5 min)
- Same process as Phase 2
- Separate deployment URL

## File Structure
```
project/frontend/
├── app/(dashboard)/
│   ├── tasks/page.tsx (existing)
│   └── chat/page.tsx (new)
├── components/
│   ├── chat/
│   │   ├── ChatWindow.tsx
│   │   ├── MessageList.tsx
│   │   ├── MessageBubble.tsx
│   │   └── MessageInput.tsx
│   └── (existing components)
└── lib/
    ├── mockAI.ts (new)
    └── (existing libs)
```

## Mock AI Examples

**User:** "Create a task to buy groceries"
**AI:** "✅ I've created a new task: 'Buy groceries'. You can view it in your task list."

**User:** "What are my pending tasks?"
**AI:** "📋 You have 3 pending tasks:
1. Buy groceries
2. Complete Phase 3
3. Test deployment"

**User:** "Mark task 1 as complete"
**AI:** "✅ Great! I've marked 'Buy groceries' as complete."

## Time Estimate
- Planning: 5 min ✅
- Implementation: 40 min
- Testing: 5 min
- Deployment: 5 min
- **Total: 55 min** (within 45-60 min budget)

---

**Starting implementation now...**
