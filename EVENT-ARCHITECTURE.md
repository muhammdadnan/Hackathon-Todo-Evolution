# Event-Driven Architecture Overview

## Introduction

This document describes the event-driven architecture implemented in the Todo Evolution application using Apache Kafka and Dapr.

## Why Event-Driven Architecture?

### Benefits

1. **Loose Coupling**: Services communicate through events, not direct calls
2. **Scalability**: Easy to add new event consumers without modifying producers
3. **Resilience**: Services can fail independently without affecting others
4. **Audit Trail**: All events are logged and can be replayed
5. **Real-time Processing**: Events are processed as they occur

### Use Cases

- **Notifications**: Send email/SMS when tasks are created or completed
- **Analytics**: Track user behavior and task patterns
- **Integrations**: Sync tasks with external systems (Slack, Jira, etc.)
- **Caching**: Update cache when data changes
- **Audit Logging**: Record all user actions for compliance

## Event Types

### 1. Task Events

#### task.created
Triggered when a new task is created.

**Payload:**
```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "task.created",
  "timestamp": "2026-02-08T10:30:00Z",
  "version": "1.0",
  "data": {
    "task_id": 123,
    "user_id": "user-456",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-02-08T10:30:00Z"
  }
}
```

**Consumers:**
- Notification service (send confirmation)
- Analytics service (track task creation rate)
- Search indexer (update search index)

#### task.updated
Triggered when a task is modified.

**Payload:**
```json
{
  "event_id": "uuid",
  "event_type": "task.updated",
  "timestamp": "2026-02-08T11:00:00Z",
  "version": "1.0",
  "data": {
    "task_id": 123,
    "user_id": "user-456",
    "changes": {
      "title": {
        "old": "Buy groceries",
        "new": "Buy groceries and cook dinner"
      },
      "description": {
        "old": "Milk, eggs, bread",
        "new": "Milk, eggs, bread, chicken"
      }
    },
    "updated_at": "2026-02-08T11:00:00Z"
  }
}
```

**Consumers:**
- Cache invalidation service
- Activity log service
- Sync service (external integrations)

#### task.completed
Triggered when a task is marked as complete.

**Payload:**
```json
{
  "event_id": "uuid",
  "event_type": "task.completed",
  "timestamp": "2026-02-08T12:00:00Z",
  "version": "1.0",
  "data": {
    "task_id": 123,
    "user_id": "user-456",
    "title": "Buy groceries and cook dinner",
    "completed_at": "2026-02-08T12:00:00Z",
    "duration_minutes": 90
  }
}
```

**Consumers:**
- Notification service (send congratulations)
- Analytics service (track completion rate)
- Gamification service (award points)

#### task.deleted
Triggered when a task is deleted.

**Payload:**
```json
{
  "event_id": "uuid",
  "event_type": "task.deleted",
  "timestamp": "2026-02-08T13:00:00Z",
  "version": "1.0",
  "data": {
    "task_id": 123,
    "user_id": "user-456",
    "title": "Buy groceries and cook dinner",
    "deleted_at": "2026-02-08T13:00:00Z",
    "reason": "user_requested"
  }
}
```

**Consumers:**
- Cache invalidation service
- Audit log service
- Cleanup service (remove related data)

### 2. User Events

#### user.registered
Triggered when a new user signs up.

**Payload:**
```json
{
  "event_id": "uuid",
  "event_type": "user.registered",
  "timestamp": "2026-02-08T09:00:00Z",
  "version": "1.0",
  "data": {
    "user_id": "user-456",
    "email": "user@example.com",
    "name": "John Doe",
    "registered_at": "2026-02-08T09:00:00Z",
    "source": "web"
  }
}
```

**Consumers:**
- Welcome email service
- Analytics service (track signups)
- Onboarding service (create sample tasks)

## Event Flow Patterns

### Pattern 1: Command-Event Pattern

```
User Action → API Command → Database Update → Event Published
```

**Example: Create Task**
1. User clicks "Create Task" in UI
2. Frontend sends POST /api/tasks
3. Backend validates and saves to database
4. Backend publishes task.created event
5. Event consumers process asynchronously

### Pattern 2: Event Sourcing

```
Events → Event Store → Current State
```

All state changes are stored as events. Current state is derived by replaying events.

**Benefits:**
- Complete audit trail
- Time travel (view state at any point)
- Event replay for debugging

### Pattern 3: CQRS (Command Query Responsibility Segregation)

```
Commands → Write Model → Events → Read Model
```

Separate models for writes and reads, synchronized via events.

**Benefits:**
- Optimized read and write models
- Better scalability
- Flexible querying

## Implementation with Dapr

### Publishing Events

```python
from dapr.clients import DaprClient

async def create_task(task_data):
    # Save to database
    task = await db.save_task(task_data)

    # Publish event
    async with DaprClient() as client:
        await client.publish_event(
            pubsub_name="pubsub",
            topic_name="task.created",
            data={
                "event_id": str(uuid.uuid4()),
                "event_type": "task.created",
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0",
                "data": task.dict()
            }
        )

    return task
```

### Subscribing to Events

```python
from fastapi import FastAPI
from dapr.ext.fastapi import DaprApp

app = FastAPI()
dapr_app = DaprApp(app)

@dapr_app.subscribe(pubsub="pubsub", topic="task.created")
async def task_created_handler(event_data: dict):
    """Handle task.created events"""
    task_id = event_data["data"]["task_id"]

    # Send notification
    await send_notification(task_id)

    # Update cache
    await cache.set(f"task:{task_id}", event_data["data"])

    # Log analytics
    await analytics.track("task_created", event_data["data"])

    return {"success": True}
```

## Error Handling

### Retry Strategy

```yaml
# Dapr resiliency configuration
apiVersion: dapr.io/v1alpha1
kind: Resiliency
metadata:
  name: myresiliency
spec:
  policies:
    retries:
      pubsubRetry:
        policy: exponential
        maxRetries: 5
        initialInterval: 1s
        maxInterval: 60s
```

### Dead Letter Queue

Failed events are sent to a dead letter topic for manual review:

```
task.created → Processing Failed → task.created.dlq
```

## Monitoring and Observability

### Metrics to Track

1. **Event Volume**: Events published per second
2. **Processing Latency**: Time from publish to consume
3. **Error Rate**: Failed event processing percentage
4. **Consumer Lag**: Backlog of unprocessed events

### Distributed Tracing

Dapr automatically adds trace IDs to events:

```json
{
  "traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
  "event_data": {...}
}
```

View traces in Zipkin or Jaeger.

## Best Practices

### 1. Event Schema Versioning

```json
{
  "version": "1.0",
  "event_type": "task.created",
  ...
}
```

Always include version to handle schema evolution.

### 2. Idempotency

Ensure event handlers are idempotent:

```python
async def task_created_handler(event_data: dict):
    event_id = event_data["event_id"]

    # Check if already processed
    if await cache.exists(f"processed:{event_id}"):
        return {"success": True, "already_processed": True}

    # Process event
    await process_task_created(event_data)

    # Mark as processed
    await cache.set(f"processed:{event_id}", "1", ttl=86400)
```

### 3. Event Ordering

Use partition keys to maintain order:

```python
await client.publish_event(
    pubsub_name="pubsub",
    topic_name="task.created",
    data=event_data,
    metadata={"partitionKey": user_id}  # Same user = same partition
)
```

### 4. Event Size

Keep events small (<1MB):
- Include only essential data
- Store large payloads separately
- Reference by ID if needed

## Security

### 1. Authentication

```yaml
# Kafka SASL authentication
metadata:
- name: authType
  value: "password"
- name: saslUsername
  secretKeyRef:
    name: kafka-secrets
    key: username
```

### 2. Authorization

```yaml
# Dapr access control
accessControl:
  defaultAction: deny
  trustDomain: "public"
  policies:
  - appId: backend
    operations:
    - name: /task.created
      action: allow
```

### 3. Encryption

```yaml
# Enable TLS
metadata:
- name: enableTLS
  value: "true"
- name: caCert
  secretKeyRef:
    name: kafka-certs
    key: ca.crt
```

## Testing

### Unit Tests

```python
async def test_task_created_event():
    # Arrange
    task_data = {"title": "Test task"}

    # Act
    await create_task(task_data)

    # Assert
    published_events = await get_published_events()
    assert len(published_events) == 1
    assert published_events[0]["event_type"] == "task.created"
```

### Integration Tests

```python
async def test_event_flow():
    # Publish event
    await publish_event("task.created", task_data)

    # Wait for processing
    await asyncio.sleep(1)

    # Verify side effects
    notification = await get_last_notification()
    assert notification["task_id"] == task_data["task_id"]
```

## Conclusion

Event-driven architecture provides:
-  Scalability through loose coupling
- ✅ Resilience through async processing
- ✅ Flexibility to add new features
- ✅ Complete audit trail
- ✅ Real-time data processing

The combination of Kafka and Dapr makes it easy to implement these patterns in a cloud-native way.
