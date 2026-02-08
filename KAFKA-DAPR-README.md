# Kafka + Dapr Deployment Guide

## Overview
This guide explains how to deploy the Todo Evolution application with event-driven architecture using Apache Kafka and Dapr.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (Next.js)                │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│              Backend (FastAPI)                      │
│              + Dapr Sidecar                         │
└──────┬──────────────┬──────────────┬────────────────┘
       │              │              │
   ┌───▼───┐     ┌────▼────┐    ┌───▼────┐
   │ Kafka │     │  Redis  │    │Postgres│
   │PubSub │     │  State  │    │  Data  │
   └───────┘     └─────────┘    └────────┘
```

## Components

### 1. Apache Kafka
- **Purpose**: Event streaming platform
- **Topics**:
  - `task.created` - New task events
  - `task.updated` - Task modification events
  - `task.completed` - Task completion events
  - `task.deleted` - Task deletion events
  - `user.registered` - New user events

### 2. Dapr Runtime
- **Pub/Sub**: Kafka integration for event publishing/subscribing
- **State Store**: Redis for distributed caching
- **Service Invocation**: HTTP/gRPC communication
- **Observability**: Distributed tracing with Zipkin

### 3. Redis
- **Purpose**: Distributed state store
- **Use Cases**:
  - Session caching
  - Task data caching
  - Rate limiting
  - Temporary data storage

## Quick Start

### Option 1: Docker Compose (Local Development)

```bash
# Start Kafka, Zookeeper, and Redis
cd kafka
docker-compose -f docker-compose.kafka.yml up -d

# Verify services are running
docker-compose -f docker-compose.kafka.yml ps

# View Kafka UI (optional)
# Open http://localhost:8080
```

### Option 2: Kubernetes Deployment

```bash
# Deploy Zookeeper
kubectl apply -f kafka/k8s/zookeeper-deployment.yaml

# Deploy Kafka
kubectl apply -f kafka/k8s/kafka-deployment.yaml

# Deploy Redis
kubectl apply -f dapr/k8s/redis-deployment.yaml

# Install Dapr on Kubernetes
dapr init -k

# Apply Dapr components
kubectl apply -f dapr/components/
kubectl apply -f dapr/config.yaml

# Verify Dapr installation
dapr status -k
```

## Dapr Components

### 1. Pub/Sub Component (pubsub.yaml)

Connects to Kafka for event publishing and subscribing:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.kafka
  metadata:
  - name: brokers
    value: "kafka-service:9092"
  - name: consumerGroup
    value: "todo-app-group"
```

**Usage in Backend:**
```python
# Publish event
await dapr_client.publish_event(
    pubsub_name="pubsub",
    topic_name="task.created",
    data={"task_id": 123, "title": "Buy groceries"}
)

# Subscribe to events
@app.post('/dapr/subscribe')
def subscribe():
    return [{
        "pubsubname": "pubsub",
        "topic": "task.created",
        "route": "/events/task-created"
    }]
```

### 2. State Store Component (statestore.yaml)

Uses Redis for distributed state management:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  metadata:
  - name: redisHost
    value: "redis-service:6379"
```

**Usage in Backend:**
```python
# Save state
await dapr_client.save_state(
    store_name="statestore",
    key="task:123",
    value={"title": "Buy groceries", "completed": False}
)

# Get state
state = await dapr_client.get_state(
    store_name="statestore",
    key="task:123"
)
```

### 3. Configuration (config.yaml)

Global Dapr configuration for tracing, metrics, and API access.

## Event Flow Examples

### Task Creation Flow

```
1. User creates task in Frontend
   ↓
2. Frontend sends POST to Backend API
   ↓
3. Backend saves task to PostgreSQL
   ↓
4. Backend publishes "task.created" event via Dapr
   ↓
5. Dapr sends event to Kafka topic
   ↓
6. Subscribers receive event (analytics, notifications, etc.)
   ↓
7. Backend caches task in Redis via Dapr state store
```

### Task Update Flow

```
1. User updates task
   ↓
2. Backend updates PostgreSQL
   ↓
3. Backend publishes "task.updated" event
   ↓
4. Backend invalidates cache in Redis
   ↓
5. Subscribers process update event
```

## Kafka Topics

### Topic: task.created
```json
{
  "event_id": "uuid",
  "timestamp": "2026-02-08T10:00:00Z",
  "user_id": "user-123",
  "task": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false
  }
}
```

### Topic: task.completed
```json
{
  "event_id": "uuid",
  "timestamp": "2026-02-08T11:00:00Z",
  "user_id": "user-123",
  "task_id": 1,
  "completed_at": "2026-02-08T11:00:00Z"
}
```

## Monitoring

### Kafka UI

Access Kafka UI at http://localhost:8080 (Docker Compose) to:
- View topics and messages
- Monitor consumer groups
- Check broker health
- Inspect message content

### Dapr Dashboard

```bash
# Install Dapr dashboard
dapr dashboard -k

# Access at http://localhost:8080
```

Features:
- View Dapr components
- Monitor service invocations
- Check pub/sub subscriptions
- View distributed traces

### Redis CLI

```bash
# Connect to Redis
docker exec -it redis redis-cli

# Or in Kubernetes
kubectl exec -it <redis-pod> -- redis-cli

# View all keys
KEYS *

# Get specific key
GET task:123

# Monitor commands
MONITOR
```

## Testing Events

### Publish Test Event

```bash
# Using Dapr CLI
dapr publish --publish-app-id backend \
  --pubsub pubsub \
  --topic task.created \
  --data '{"task_id": 123, "title": "Test task"}'

# Using curl
curl -X POST http://localhost:3500/v1.0/publish/pubsub/task.created \
  -H "Content-Type: application/json" \
  -d '{"task_id": 123, "title": "Test task"}'
```

### Subscribe to Events

```bash
# View Kafka messages
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic task.created \
  --from-beginning
```

## Production Deployment

### 1. Kafka Cluster

For production, use a managed Kafka service:
- **AWS**: Amazon MSK
- **Azure**: Azure Event Hubs (Kafka-compatible)
- **GCP**: Confluent Cloud on GCP
- **Confluent Cloud**: Fully managed Kafka

### 2. Redis Cluster

Use managed Redis:
- **AWS**: Amazon ElastiCache
- **Azure**: Azure Cache for Redis
- **GCP**: Google Cloud Memorystore

### 3. Dapr Configuration

Update component files with production endpoints:

```yaml
# pubsub.yaml
metadata:
- name: brokers
  value: "your-kafka-cluster:9092"
- name: authType
  value: "password"
- name: saslUsername
  secretKeyRef:
    name: kafka-secrets
    key: username
- name: saslPassword
  secretKeyRef:
    name: kafka-secrets
    key: password
```

### 4. Security

```bash
# Create Kubernetes secrets
kubectl create secret generic kafka-secrets \
  --from-literal=username='your-username' \
  --from-literal=password='your-password'

kubectl create secret generic redis-secrets \
  --from-literal=password='your-redis-password'
```

## Troubleshooting

### Kafka Not Starting

```bash
# Check Zookeeper is running
docker-compose -f docker-compose.kafka.yml logs zookeeper

# Check Kafka logs
docker-compose -f docker-compose.kafka.yml logs kafka

# Verify Zookeeper connection
docker exec -it kafka kafka-broker-api-versions \
  --bootstrap-server localhost:9092
```

### Dapr Sidecar Issues

```bash
# Check Dapr sidecar logs
kubectl logs <pod-name> -c daprd

# Verify Dapr components
dapr components -k

# Check Dapr configuration
kubectl get configuration dapr-config -o yaml
```

### Events Not Publishing

```bash
# Check Dapr pub/sub component
kubectl describe component pubsub

# Verify Kafka topic exists
docker exec -it kafka kafka-topics \
  --bootstrap-server localhost:9092 \
  --list

# Check application logs
kubectl logs <backend-pod> -c backend
```

### Redis Connection Issues

```bash
# Test Redis connection
docker exec -it redis redis-cli ping

# Check Redis logs
docker-compose -f docker-compose.kafka.yml logs redis

# Verify Dapr state store component
kubectl describe component statestore
```

## Performance Tuning

### Kafka Configuration

```yaml
# Increase partitions for parallelism
KAFKA_NUM_PARTITIONS: "10"

# Adjust retention
KAFKA_LOG_RETENTION_HOURS: "168"  # 7 days

# Increase buffer size
KAFKA_SOCKET_SEND_BUFFER_BYTES: "102400"
KAFKA_SOCKET_RECEIVE_BUFFER_BYTES: "102400"
```

### Redis Configuration

```yaml
# Increase connection pool
- name: poolSize
  value: "50"

# Adjust timeouts
- name: dialTimeout
  value: "10s"
- name: readTimeout
  value: "5s"
```

### Dapr Configuration

```yaml
# Adjust tracing sample rate
tracing:
  samplingRate: "0.1"  # 10% sampling

# Configure retries
spec:
  resiliency:
    retries:
      retryForever: false
      maxRetries: 3
      retryDelay: "1s"
```

## Cleanup

```bash
# Docker Compose
cd kafka
docker-compose -f docker-compose.kafka.yml down -v

# Kubernetes
kubectl delete -f kafka/k8s/
kubectl delete -f dapr/k8s/
kubectl delete -f dapr/components/
dapr uninstall -k
```

## Next Steps

- Implement event handlers in backend
- Add event-driven notifications
- Set up monitoring with Prometheus
- Configure distributed tracing
- Implement event replay for debugging
- Add event schema validation

## Resources

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Dapr Documentation](https://docs.dapr.io/)
- [Dapr Pub/Sub](https://docs.dapr.io/developing-applications/building-blocks/pubsub/)
- [Dapr State Management](https://docs.dapr.io/developing-applications/building-blocks/state-management/)
- [Kafka with Dapr](https://docs.dapr.io/reference/components-reference/supported-pubsub/setup-apache-kafka/)
