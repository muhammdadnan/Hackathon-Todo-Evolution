# Docker Deployment Guide

## Overview
This guide explains how to build and run the Todo Evolution application using Docker and Docker Compose.

## Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

## Quick Start

### 1. Build and Run with Docker Compose

```bash
# Navigate to project directory
cd project

# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: localhost:5432

### 2. Build Individual Images

**Frontend:**
```bash
cd project/frontend
docker build -t todo-frontend:latest .
```

**Backend:**
```bash
cd project/backend
docker build -t todo-backend:latest .
```

### 3. Run Individual Containers

**Database:**
```bash
docker run -d \
  --name todo-database \
  -e POSTGRES_USER=todouser \
  -e POSTGRES_PASSWORD=todopassword \
  -e POSTGRES_DB=tododb \
  -p 5432:5432 \
  postgres:16-alpine
```

**Backend:**
```bash
docker run -d \
  --name todo-backend \
  -e DATABASE_URL=postgresql+asyncpg://todouser:todopassword@database:5432/tododb \
  -e JWT_SECRET=your-secret-key \
  -p 8000:8000 \
  --link todo-database:database \
  todo-backend:latest
```

**Frontend:**
```bash
docker run -d \
  --name todo-frontend \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  -p 3000:3000 \
  --link todo-backend:backend \
  todo-frontend:latest
```

## Docker Compose Configuration

The `docker-compose.yml` file defines three services:

### Services

1. **database** (PostgreSQL 16)
   - Port: 5432
   - Volume: postgres_data
   - Health check enabled

2. **backend** (FastAPI)
   - Port: 8000
   - Depends on: database
   - Auto-restart enabled

3. **frontend** (Next.js)
   - Port: 3000
   - Depends on: backend
   - Auto-restart enabled

### Environment Variables

**Backend:**
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT tokens
- `JWT_ALGORITHM`: HS256
- `JWT_EXPIRATION_MINUTES`: 1440 (24 hours)

**Frontend:**
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_USE_MOCK_DATA`: false (use real backend)

## Development Workflow

### Hot Reload Development

For development with hot reload, use volume mounts:

```yaml
# Add to docker-compose.yml services
backend:
  volumes:
    - ./backend:/app
  command: uvicorn app.main:app --reload --host 0.0.0.0

frontend:
  volumes:
    - ./frontend:/app
    - /app/node_modules
  command: npm run dev
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f database
```

### Execute Commands in Containers

```bash
# Backend shell
docker-compose exec backend bash

# Run database migrations
docker-compose exec backend python -m alembic upgrade head

# Frontend shell
docker-compose exec frontend sh

# Database shell
docker-compose exec database psql -U todouser -d tododb
```

## Production Deployment

### Build for Production

```bash
# Build with specific tags
docker build -t your-registry/todo-frontend:v1.0.0 ./frontend
docker build -t your-registry/todo-backend:v1.0.0 ./backend

# Push to registry
docker push your-registry/todo-frontend:v1.0.0
docker push your-registry/todo-backend:v1.0.0
```

### Security Best Practices

1. **Use secrets management:**
   ```bash
   docker secret create jwt_secret jwt_secret.txt
   docker secret create db_password db_password.txt
   ```

2. **Run as non-root user** (already configured in Dockerfiles)

3. **Use specific image tags** (not `latest`)

4. **Scan images for vulnerabilities:**
   ```bash
   docker scan todo-frontend:latest
   docker scan todo-backend:latest
   ```

## Troubleshooting

### Container won't start

```bash
# Check container status
docker-compose ps

# View container logs
docker-compose logs backend

# Inspect container
docker inspect todo-backend
```

### Database connection issues

```bash
# Check database is running
docker-compose ps database

# Test database connection
docker-compose exec database psql -U todouser -d tododb -c "SELECT 1"

# Check backend can reach database
docker-compose exec backend ping database
```

### Port conflicts

If ports are already in use, modify `docker-compose.yml`:

```yaml
services:
  frontend:
    ports:
      - "3001:3000"  # Use different host port
```

## Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove volumes (deletes database data)
docker-compose down -v

# Remove images
docker rmi todo-frontend:latest todo-backend:latest

# Remove all unused Docker resources
docker system prune -a
```

## Next Steps

- See [KUBERNETES-README.md](../KUBERNETES-README.md) for Kubernetes deployment
- Configure CI/CD pipeline for automated builds
- Set up monitoring with Prometheus/Grafana
- Implement backup strategy for database

## Support

For issues or questions:
- Check logs: `docker-compose logs`
- Verify environment variables
- Ensure all ports are available
- Check Docker daemon is running
