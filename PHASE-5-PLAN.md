# Phase 5 - Kafka + Dapr Architecture Plan

## Overview
Add event-driven architecture using Apache Kafka for messaging and Dapr for microservices patterns.

## Architecture

```
┌─────────────┐         ┌─────────────┐
│  Frontend   │────────▶│  Backend    │
│  (Next.js)  │         │  (FastAPI)  │
└─────────────┘         └──────┬──────┘
                               │
                        ┌──────▼──────┐
                        │ Dapr Sidecar│
                        └──────┬──────┘
                               │
                    ┌──────────┼──────────┐
                    │          │          │
            ┌───────▼──┐  ┌────▼────┐  ┌─▼────────┐
            │  Kafka   │  │  Redis  │  │ Postgres │
            │ (PubSub) │  │ (State) │  │  (Data)  │
            └──────────┘  └─────────┘  └──────────┘
```

## Components

### 1. Apache Kafka
- **Purpose**: Event streaming and pub/sub messaging
- **Events**:
  - `task.created`
  - `task.updated`
  - `task.completed`
  - `task.deleted`
  - `user.registered`

### 2. Dapr Runtime
- **Pub/Sub**: Kafka integration
- **State Management**: Redis for caching
- **Service Invocation**: HTTP/gRPC between services
- **Observability**: Distributed tracing

### 3. Redis
- **Purpose**: State store and caching
- **Use Cases**:
  - Session management
  - Task cache
  - Rate limiting

## Event Flow

```
User Action → Backend API → Dapr Sidecar → Kafka Topic → Subscribers
                    ↓
              State Store (Redis)
                    ↓
              Database (Postgres)
```

## Files to Create

### Kafka Setup
1. `kafka/docker-compose.kafka.yml`
2. `kafka/k8s/kafka-deployment.yaml`
3. `kafka/k8s/zookeeper-deployment.yaml`

### Dapr Configuration
1. `dapr/components/pubsub.yaml` (Kafka)
2. `dapr/components/statestore.yaml` (Redis)
3. `dapr/components/secrets.yaml`
4. `dapr/config.yaml`

### Application Integration
1. `project/backend/app/events/` (event handlers)
2. `project/backend/app/dapr/` (Dapr client)

### Documentation
1. `KAFKA-DAPR-README.md`
2. `EVENT-ARCHITECTURE.md`

## Implementation Steps

1. Create Kafka configuration (10 min)
2. Create Dapr components (10 min)
3. Add event handlers to backend (optional - demo only)
4. Create documentation (10 min)

**Total: 30 minutes**

---

**Starting implementation...**
