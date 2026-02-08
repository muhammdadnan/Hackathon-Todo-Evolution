#!/bin/bash

# Video Recording Guide and Scripts
# Use this as a reference when recording your demo videos

echo "==================================="
echo "Hackathon Demo Video Scripts"
echo "==================================="
echo ""

# Video 1: Phase 2 Demo (5 minutes)
cat << 'EOF'

VIDEO 1: PHASE 2 - TODO APPLICATION (5 min)
============================================

INTRO (30 sec):
"Hi, I'm demonstrating Phase 2 of my hackathon project - a full-stack Todo application built with Next.js and FastAPI."

DEMO FLOW:

1. Landing Page (30 sec)
   - Show homepage
   - Explain features
   - Click "Get Started"

2. Sign Up (1 min)
   - Click "Sign Up"
   - Enter: test@example.com / password123
   - Show successful registration
   - Redirect to tasks page

3. Create Tasks (1 min)
   - Click "Add Task"
   - Create: "Buy groceries"
   - Create: "Complete hackathon"
   - Create: "Deploy to production"
   - Show tasks appearing in list

4. Task Operations (1.5 min)
   - Mark "Buy groceries" as complete
   - Edit "Complete hackathon" → "Complete hackathon project"
   - Show filtering: All → Pending → Completed
   - Delete "Buy groceries"

5. Responsive Design (30 sec)
   - Resize browser window
   - Show mobile view
   - Show tablet view

OUTRO (30 sec):
"This demonstrates a complete CRUD application with authentication, built with Next.js 16, TypeScript, Tailwind CSS, and FastAPI with PostgreSQL."

EOF

echo ""
echo "-----------------------------------"
echo ""

# Video 2: Phase 3 Demo (5 minutes)
cat << 'EOF'

VIDEO 2: PHASE 3 - AI CHATBOT (5 min)
======================================

INTRO (30 sec):
"Phase 3 adds an AI-powered chatbot that lets you manage tasks using natural language."

DEMO FLOW:

1. Navigate to Chat (30 sec)
   - From tasks page, click "AI Chat"
   - Show chat interface
   - Read greeting message

2. Create Task via Chat (1 min)
   - Type: "Create a task to buy groceries"
   - Show AI response
   - Type: "Add a task to call mom"
   - Show AI response

3. Query Tasks (1 min)
   - Type: "Show my pending tasks"
   - Show AI listing tasks
   - Type: "What are my tasks?"
   - Show AI response

4. Complete Task via Chat (1 min)
   - Type: "Mark task 1 as complete"
   - Show AI confirmation
   - Navigate to tasks page
   - Show task is marked complete

5. Delete Task via Chat (30 sec)
   - Back to chat
   - Type: "Delete task 2"
   - Show AI confirmation

6. Help Command (30 sec)
   - Type: "What can you help me with?"
   - Show AI capabilities list

OUTRO (30 sec):
"The chatbot uses pattern matching to understand natural language and integrates seamlessly with the task management system."

EOF

echo ""
echo "-----------------------------------"
echo ""

# Video 3: Phase 4 Demo (5 minutes)
cat << 'EOF'

VIDEO 3: PHASE 4 - DOCKER + KUBERNETES (5 min)
===============================================

INTRO (30 sec):
"Phase 4 demonstrates containerization with Docker and orchestration with Kubernetes."

DEMO FLOW:

1. Docker Files (1.5 min)
   - Open: project/frontend/Dockerfile
   - Explain: Multi-stage build
   - Show: Node base, dependencies, build, production
   - Open: project/backend/Dockerfile
   - Explain: Python image, dependencies, non-root user

2. Docker Compose (1 min)
   - Open: project/docker-compose.yml
   - Show: 3 services (frontend, backend, database)
   - Explain: Networks, volumes, health checks
   - Show: Environment variables

3. Kubernetes Manifests (2 min)
   - Open: k8s/frontend-deployment.yaml
   - Show: 3 replicas, resource limits
   - Show: Liveness and readiness probes
   - Open: k8s/backend-deployment.yaml
   - Show: Similar configuration
   - Open: k8s/database-statefulset.yaml
   - Show: Persistent volume claims

4. Services (30 sec)
   - Open: k8s/frontend-service.yaml
   - Show: LoadBalancer type
   - Open: k8s/backend-service.yaml
   - Show: ClusterIP type

OUTRO (30 sec):
"This provides production-ready containerization with Docker and scalable orchestration with Kubernetes."

EOF

echo ""
echo "-----------------------------------"
echo ""

# Video 4: Phase 5 Demo (5 minutes)
cat << 'EOF'

VIDEO 4: PHASE 5 - KAFKA + DAPR (5 min)
========================================

INTRO (30 sec):
"Phase 5 implements event-driven architecture using Apache Kafka and Dapr."

DEMO FLOW:

1. Kafka Configuration (1.5 min)
   - Open: kafka/docker-compose.kafka.yml
   - Show: Zookeeper service
   - Show: Kafka broker configuration
   - Show: Redis for state management
   - Show: Kafka UI for monitoring

2. Dapr Components (1.5 min)
   - Open: dapr/components/pubsub.yaml
   - Explain: Kafka integration
   - Show: Broker connection, consumer group
   - Open: dapr/components/statestore.yaml
   - Explain: Redis state store
   - Show: Connection configuration

3. Event Architecture (1.5 min)
   - Open: EVENT-ARCHITECTURE.md
   - Show: Event flow diagram
   - Explain: task.created event
   - Explain: task.updated event
   - Show: Event payload examples

4. Kubernetes Deployment (30 sec)
   - Open: kafka/k8s/kafka-deployment.yaml
   - Show: StatefulSet configuration
   - Show: Persistent volumes

OUTRO (30 sec):
"This demonstrates a scalable, event-driven microservices architecture ready for production deployment."

EOF

echo ""
echo "-----------------------------------"
echo ""

# Video 5: Project Overview (5 minutes)
cat << 'EOF'

VIDEO 5: PROJECT OVERVIEW (5 min)
==================================

INTRO (30 sec):
"This is a complete overview of my hackathon project - a cloud-native todo application with AI, containers, and event-driven architecture."

DEMO FLOW:

1. Project Structure (1 min)
   - Open VS Code
   - Show: project/ folder
   - Show: k8s/ folder
   - Show: kafka/ folder
   - Show: dapr/ folder
   - Show: Documentation files

2. Technology Stack (1 min)
   - Frontend: Next.js 16, TypeScript, Tailwind
   - Backend: FastAPI, SQLModel, PostgreSQL
   - Containers: Docker, Kubernetes
   - Messaging: Kafka, Dapr
   - State: Redis

3. Key Features (1.5 min)
   - Full CRUD operations
   - JWT authentication
   - AI chatbot
   - Natural language processing
   - Docker containerization
   - Kubernetes orchestration
   - Event-driven architecture
   - Distributed state management

4. Git History (30 sec)
   - Show: git log
   - Explain: 8 commits
   - Show: Clean commit messages

5. Documentation (30 sec)
   - Show: 12 comprehensive guides
   - Show: Architecture diagrams
   - Show: Deployment instructions

OUTRO (30 sec):
"This project demonstrates modern full-stack development with cloud-native technologies, ready for production deployment."

EOF

echo ""
echo "==================================="
echo "Recording Tips:"
echo "==================================="
echo "1. Use 1920x1080 resolution"
echo "2. Close unnecessary applications"
echo "3. Clear browser history/cache"
echo "4. Use incognito mode for clean demo"
echo "5. Speak clearly and at moderate pace"
echo "6. Pause between sections"
echo "7. Show, don't just tell"
echo "8. Keep videos under 5 minutes each"
echo ""
echo "Tools:"
echo "- Windows: Game Bar (Win+G)"
echo "- OBS Studio (free)"
echo "- Loom (web-based)"
echo "- Camtasia (paid)"
echo ""
echo "==================================="
