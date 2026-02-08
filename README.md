# Hackathon Todo Evolution

> Full-stack Todo application with AI chatbot, Docker, Kubernetes, Kafka, and Dapr - Complete cloud-native microservices architecture

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/muhammdadnan/Hackathon-Todo-Evolution)
[![Next.js](https://img.shields.io/badge/Next.js-16-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-blue)](https://kubernetes.io/)

## 🎯 Project Overview

A comprehensive hackathon project demonstrating modern full-stack development with:
- **Phase 2:** Full-stack CRUD application with authentication
- **Phase 3:** AI-powered chatbot for natural language task management
- **Phase 4:** Docker containerization and Kubernetes orchestration
- **Phase 5:** Event-driven architecture with Kafka and Dapr

## ✨ Features

### Phase 2: Todo Application
- ✅ User authentication (JWT-based)
- ✅ Create, read, update, delete tasks
- ✅ Task filtering (all/pending/completed)
- ✅ Responsive UI with Tailwind CSS
- ✅ Mock data mode for demos
- ✅ 65 comprehensive test cases

### Phase 3: AI Chatbot
- 🤖 Natural language task management
- 💬 Create tasks: "Create a task to buy groceries"
- 📋 Query tasks: "Show my pending tasks"
- ✅ Complete tasks: "Mark task 1 as complete"
- 🗑️ Delete tasks: "Delete task 2"
- 🎨 Smooth animations and real-time updates

### Phase 4: Containerization
- 🐳 Production-ready Dockerfiles
- 📦 Multi-stage builds for optimization
- 🎼 Docker Compose for local development
- ☸️ Kubernetes manifests with:
  - Deployments (3 replicas each)
  - Services (LoadBalancer, ClusterIP)
  - StatefulSets for databases
  - ConfigMaps and Secrets
  - Health checks and resource limits

### Phase 5: Event-Driven Architecture
- 📨 Apache Kafka for event streaming
- 🔄 Dapr for microservices patterns
- 💾 Redis for distributed state management
- 📊 Event schemas and flow diagrams
- 🔍 Observability with distributed tracing

## 🚀 Quick Start

### Demo Credentials
```
Email: demo@example.com
Password: demo123
```

### Local Development (Frontend Only)
```bash
cd project/frontend
npm install
npm run dev
# Open http://localhost:3000
```

### Full Stack with Docker
```bash
cd project
docker-compose up -d
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### With Kafka and Dapr
```bash
cd kafka
docker-compose -f docker-compose.kafka.yml up -d
# Kafka UI: http://localhost:8080
```

## 📁 Project Structure

```
├── project/
│   ├── frontend/          # Next.js 16 + TypeScript + Tailwind
│   │   ├── app/          # Pages and routes
│   │   ├── components/   # React components
│   │   │   ├── chat/    # AI chatbot components
│   │   │   └── ui/      # Reusable UI components
│   │   ├── lib/         # Utilities and mock data
│   │   └── Dockerfile   # Frontend container
│   ├── backend/          # FastAPI + SQLModel
│   │   ├── app/         # API routes and models
│   │   ├── tests/       # 65 test cases
│   │   └── Dockerfile   # Backend container
│   └── docker-compose.yml
├── k8s/                  # Kubernetes manifests
│   ├── frontend-deployment.yaml
│   ├── backend-deployment.yaml
│   ├── database-statefulset.yaml
│   └── ...
├── kafka/                # Kafka configuration
│   ├── k8s/
│   └── docker-compose.kafka.yml
├── dapr/                 # Dapr components
│   ├── components/
│   │   ├── pubsub.yaml
│   │   └── statestore.yaml
│   └── config.yaml
├── specs/                # Feature specifications
└── history/              # ADRs and PHRs
```

## 🛠️ Technology Stack

### Frontend
- **Framework:** Next.js 16 (App Router)
- **Language:** TypeScript (strict mode)
- **Styling:** Tailwind CSS 3.x
- **State:** React hooks
- **AI:** Mock pattern matching

### Backend
- **Framework:** FastAPI 0.128
- **ORM:** SQLModel 0.0.32
- **Database:** PostgreSQL 16
- **Auth:** JWT tokens
- **Testing:** pytest (65 tests)

### DevOps
- **Containers:** Docker
- **Orchestration:** Kubernetes
- **Messaging:** Apache Kafka 7.5
- **Microservices:** Dapr
- **State Store:** Redis 7
- **CI/CD:** GitHub Actions ready

## 📚 Documentation

- [Docker Deployment Guide](DOCKER-README.md)
- [Kubernetes Deployment Guide](KUBERNETES-README.md)
- [Kafka + Dapr Guide](KAFKA-DAPR-README.md)
- [Event Architecture](EVENT-ARCHITECTURE.md)
- [Action Items](YOUR-ACTION-ITEMS.md)
- [Final Status](FINAL-HACKATHON-STATUS.md)

## 🎥 Demo Videos

### Phase 2: Todo Application
- User authentication flow
- CRUD operations
- Task filtering
- Responsive design

### Phase 3: AI Chatbot
- Natural language commands
- Task management via chat
- Real-time responses
- Smooth animations

### Phase 4: Docker + Kubernetes
- Container architecture
- Kubernetes deployment
- Scaling and health checks
- Production configuration

### Phase 5: Kafka + Dapr
- Event-driven architecture
- Pub/Sub messaging
- State management
- Distributed tracing

## 🚢 Deployment

### Vercel (Frontend)
```bash
cd project/frontend
npx vercel --prod
```

Or use the Vercel dashboard:
1. Import repository
2. Root directory: `project/frontend`
3. Add env: `NEXT_PUBLIC_USE_MOCK_DATA=true`
4. Deploy

### Kubernetes (Full Stack)
```bash
# Apply all manifests
kubectl apply -f k8s/
kubectl apply -f kafka/k8s/
kubectl apply -f dapr/components/

# Check status
kubectl get all
```

## 🧪 Testing

### Backend Tests
```bash
cd project/backend
pytest tests/ -v
# 65 tests covering all endpoints
```

### Frontend Tests
```bash
cd project/frontend
npm test
```

## 📊 Project Statistics

- **Total Files:** 90+
- **Lines of Code:** ~5,000+
- **Git Commits:** 8
- **Test Cases:** 65
- **Documentation:** 12 guides
- **Docker Images:** 2
- **Kubernetes Resources:** 8
- **Dapr Components:** 3

## 🏗️ Architecture

### System Architecture
```
┌─────────────┐
│  Frontend   │ (Next.js)
│  Port: 3000 │
└──────┬──────┘
       │
┌──────▼──────┐
│  Backend    │ (FastAPI)
│  Port: 8000 │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──▼──┐ ┌─▼────┐
│Redis│ │Postgres│
└─────┘ └──────┘
```

### Event-Driven Architecture
```
Backend → Dapr → Kafka → Subscribers
   ↓
 Redis (State)
   ↓
Postgres (Data)
```

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Muhammad Adnan**
- GitHub: [@muhammdadnan](https://github.com/muhammdadnan)
- Email: adnan892009@gmail.com

## 🙏 Acknowledgments

- Built with Claude Code (Anthropic)
- Next.js and Vercel teams
- FastAPI community
- Kubernetes and CNCF
- Apache Kafka and Confluent
- Dapr project

## 📞 Support

For issues or questions:
1. Check the documentation in the repo
2. Review the comprehensive guides
3. Open an issue on GitHub
4. Check commit history for context

---

**⭐ Star this repo if you find it helpful!**

**🔗 Live Demo:** [Deploy to Vercel to get URL]

**📦 Repository:** https://github.com/muhammdadnan/Hackathon-Todo-Evolution
