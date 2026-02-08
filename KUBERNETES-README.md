# Kubernetes Deployment Guide

## Overview
This guide explains how to deploy the Todo Evolution application to a Kubernetes cluster.

## Prerequisites
- Kubernetes cluster (1.24+)
- kubectl configured
- Docker images built and pushed to registry

## Architecture

```
┌──────────────────────────────────┐
│         LoadBalancer             │
│      (frontend-service)          │
└────────────┬─────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────────┐  ┌────▼──────┐
│ Frontend   │  │ Backend   │
│ Pods (x3)  │  │ Pods (x3) │
└────────────┘  └────┬──────┘
                     │
                ┌────▼──────┐
                │PostgreSQL │
                │StatefulSet│
                └───────────┘
```

## Quick Start

### 1. Apply All Manifests

```bash
# Create namespace (optional)
kubectl create namespace todo-app

# Apply configurations
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/database-statefulset.yaml
kubectl apply -f k8s/database-service.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml

# Or apply all at once
kubectl apply -f k8s/
```

### 2. Verify Deployment

```bash
# Check all resources
kubectl get all

# Check pods status
kubectl get pods

# Check services
kubectl get services

# Check persistent volumes
kubectl get pvc
```

### 3. Access the Application

```bash
# Get frontend service external IP
kubectl get service frontend-service

# Wait for EXTERNAL-IP to be assigned
# Then access: http://<EXTERNAL-IP>
```

## Detailed Setup

### Step 1: Prepare Docker Images

Build and push images to your container registry:

```bash
# Build images
docker build -t your-registry/todo-frontend:v1.0.0 ./project/frontend
docker build -t your-registry/todo-backend:v1.0.0 ./project/backend

# Push to registry
docker push your-registry/todo-frontend:v1.0.0
docker push your-registry/todo-backend:v1.0.0
```

### Step 2: Update Image References

Edit deployment files to use your registry:

```yaml
# k8s/frontend-deployment.yaml
spec:
  containers:
  - name: frontend
    image: your-registry/todo-frontend:v1.0.0

# k8s/backend-deployment.yaml
spec:
  containers:
  - name: backend
    image: your-registry/todo-backend:v1.0.0
```

### Step 3: Configure Secrets

**Option A: Update secrets.yaml**
```bash
# Edit k8s/secrets.yaml with your values
# Then apply
kubectl apply -f k8s/secrets.yaml
```

**Option B: Create from command line**
```bash
kubectl create secret generic todo-secrets \
  --from-literal=POSTGRES_PASSWORD='your-secure-password' \
  --from-literal=JWT_SECRET='your-jwt-secret-key' \
  --from-literal=DATABASE_URL='postgresql+asyncpg://todouser:your-password@database-service:5432/tododb'
```

### Step 4: Deploy Database

```bash
# Apply database resources
kubectl apply -f k8s/database-statefulset.yaml
kubectl apply -f k8s/database-service.yaml

# Wait for database to be ready
kubectl wait --for=condition=ready pod -l app=database --timeout=300s

# Verify database is running
kubectl get statefulset database
kubectl get pods -l app=database
```

### Step 5: Deploy Backend

```bash
# Apply backend resources
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml

# Wait for backend to be ready
kubectl wait --for=condition=ready pod -l app=backend --timeout=300s

# Check backend logs
kubectl logs -l app=backend --tail=50
```

### Step 6: Deploy Frontend

```bash
# Apply frontend resources
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml

# Wait for frontend to be ready
kubectl wait --for=condition=ready pod -l app=frontend --timeout=300s

# Get external IP
kubectl get service frontend-service
```

## Kubernetes Resources

### ConfigMap (configmap.yaml)
- Frontend API URL
- Backend JWT settings
- Database connection parameters

### Secrets (secrets.yaml)
- Database password
- JWT secret key
- Database connection string

### StatefulSet (database-statefulset.yaml)
- PostgreSQL 16
- 1 replica
- Persistent volume (1Gi)
- Health checks

### Deployments
- **Frontend**: 3 replicas, resource limits, health checks
- **Backend**: 3 replicas, resource limits, health checks

### Services
- **frontend-service**: LoadBalancer (port 80 → 3000)
- **backend-service**: ClusterIP (port 8000)
- **database-service**: Headless (port 5432)

## Scaling

### Manual Scaling

```bash
# Scale frontend
kubectl scale deployment frontend --replicas=5

# Scale backend
kubectl scale deployment backend --replicas=5
```

### Horizontal Pod Autoscaler

```bash
# Create HPA for backend
kubectl autoscale deployment backend \
  --cpu-percent=70 \
  --min=3 \
  --max=10

# Create HPA for frontend
kubectl autoscale deployment frontend \
  --cpu-percent=70 \
  --min=3 \
  --max=10

# Check HPA status
kubectl get hpa
```

## Monitoring

### View Logs

```bash
# Frontend logs
kubectl logs -l app=frontend --tail=100 -f

# Backend logs
kubectl logs -l app=backend --tail=100 -f

# Database logs
kubectl logs -l app=database --tail=100 -f

# All pods
kubectl logs -l app=backend --all-containers=true
```

### Check Resource Usage

```bash
# Pod resource usage
kubectl top pods

# Node resource usage
kubectl top nodes
```

### Describe Resources

```bash
# Describe pod
kubectl describe pod <pod-name>

# Describe service
kubectl describe service frontend-service

# Describe deployment
kubectl describe deployment backend
```

## Database Management

### Access Database

```bash
# Connect to database pod
kubectl exec -it database-0 -- psql -U todouser -d tododb

# Run SQL commands
kubectl exec -it database-0 -- psql -U todouser -d tododb -c "SELECT * FROM users;"
```

### Backup Database

```bash
# Create backup
kubectl exec database-0 -- pg_dump -U todouser tododb > backup.sql

# Restore backup
kubectl exec -i database-0 -- psql -U todouser tododb < backup.sql
```

### Database Migrations

```bash
# Run migrations from backend pod
kubectl exec -it <backend-pod-name> -- python -m alembic upgrade head
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods

# Describe pod to see events
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Check previous logs if pod restarted
kubectl logs <pod-name> --previous
```

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints

# Test service from within cluster
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- http://backend-service:8000/health

# Check service configuration
kubectl describe service backend-service
```

### Database Connection Issues

```bash
# Check database pod is running
kubectl get pods -l app=database

# Test database connection
kubectl exec -it database-0 -- pg_isready -U todouser

# Check backend can reach database
kubectl exec -it <backend-pod> -- ping database-service

# Verify secrets are mounted
kubectl exec -it <backend-pod> -- env | grep DATABASE
```

### Image Pull Errors

```bash
# Check image pull secrets
kubectl get secrets

# Create image pull secret if needed
kubectl create secret docker-registry regcred \
  --docker-server=<your-registry> \
  --docker-username=<username> \
  --docker-password=<password>

# Add to deployment
spec:
  imagePullSecrets:
  - name: regcred
```

## Updates and Rollbacks

### Rolling Update

```bash
# Update image
kubectl set image deployment/backend backend=your-registry/todo-backend:v1.1.0

# Check rollout status
kubectl rollout status deployment/backend

# View rollout history
kubectl rollout history deployment/backend
```

### Rollback

```bash
# Rollback to previous version
kubectl rollout undo deployment/backend

# Rollback to specific revision
kubectl rollout undo deployment/backend --to-revision=2
```

## Production Best Practices

### 1. Use Namespaces

```bash
kubectl create namespace production
kubectl apply -f k8s/ -n production
```

### 2. Resource Limits

Already configured in deployments:
- Memory: 256Mi request, 512Mi limit
- CPU: 250m request, 500m limit

### 3. Health Checks

Already configured:
- Liveness probes
- Readiness probes

### 4. Security

```bash
# Use network policies
kubectl apply -f k8s/network-policy.yaml

# Enable RBAC
kubectl apply -f k8s/rbac.yaml

# Use Pod Security Standards
kubectl label namespace default pod-security.kubernetes.io/enforce=baseline
```

### 5. Monitoring

```bash
# Install Prometheus
helm install prometheus prometheus-community/prometheus

# Install Grafana
helm install grafana grafana/grafana
```

## Cleanup

```bash
# Delete all resources
kubectl delete -f k8s/

# Delete namespace (if used)
kubectl delete namespace todo-app

# Delete persistent volumes
kubectl delete pvc --all
```

## Cloud Provider Specific

### AWS EKS

```bash
# Use EBS for persistent volumes
# Update storage class in database-statefulset.yaml
storageClassName: gp3

# Use ALB for LoadBalancer
# Add annotations to frontend-service.yaml
metadata:
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
```

### Google GKE

```bash
# Use GCE persistent disks
storageClassName: standard

# Use GCP Load Balancer (automatic)
```

### Azure AKS

```bash
# Use Azure Disk
storageClassName: managed-premium

# Use Azure Load Balancer (automatic)
```

## Next Steps

- Set up Ingress controller for HTTPS
- Configure cert-manager for SSL certificates
- Implement GitOps with ArgoCD or Flux
- Set up monitoring with Prometheus/Grafana
- Configure log aggregation with ELK stack
- Implement backup strategy

## Support

For issues:
1. Check pod logs: `kubectl logs <pod-name>`
2. Describe resources: `kubectl describe <resource> <name>`
3. Check events: `kubectl get events --sort-by='.lastTimestamp'`
4. Verify configurations: `kubectl get configmap todo-config -o yaml`
