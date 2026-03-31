# Self-Improving Swarm System - Deployment Guide

**Version:** 1.0  
**Date:** 2026-03-28  
**Status:** Initial Draft

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Type Checking Setup (Optional)](#type-checking-setup-optional)
7. [Security Considerations](#security-considerations)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 8 GB | 16+ GB |
| Storage | 20 GB | 50+ GB SSD |
| OS | Windows 10/11 with WSL2, Ubuntu 22.04, macOS 12+ | Ubuntu 22.04 LTS |

### Required Software

- **Python** 3.10+ (3.12 recommended)
- **Node.js** 18+ (for UI)
- **uv** (Python package manager)
- **Git**
- **Docker** (optional, for containerized deployment)

### API Keys (at least one required)

- OpenAI API key
- Anthropic API key
- MiniMax API key
- Or any other supported LLM provider

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/Self_AI.git
cd Self_AI
```

### 2. Python Environment Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv --python 3.12
source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows

# Install base dependencies
uv pip install -e .

# Install with optional extras
uv pip install -e ".[modal]"  # For Modal sandbox support
uv pip install -e ".[prime]" # For Prime sandbox support

# Install dev dependencies
uv pip install -e ".[dev]"
uv pip install -e ".[test]"
```

### 3. UI Setup

```bash
cd ui

# Install Node dependencies
npm install

# Build the UI
npm run build

# Start development server (optional)
npm run dev
```

### 4. Environment Variables

Create a `.env` file in the project root:

```bash
# Required for LLM access (at least one)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
MINIMAX_API_KEY=...

# Optional: Backend selection
DEFAULT_BACKEND=openai

# Optional: Environment mode
ENVIRONMENT=local
LOG_LEVEL=INFO

# Optional: Security
ENABLE_KEY_ENCRYPTION=true
```

### 5. Verify Installation

```bash
# Run tests
uv run pytest

# Run the application (after Phase 1-4 implementation)
python app.py
```

---

## Docker Deployment

### 1. Build the Docker Image

```bash
# Build image
docker build -t self-ai:latest .

# Or use docker-compose for full stack
docker-compose up -d
```

### 2. Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy application files
COPY . .

# Install Python dependencies
RUN uv pip install -e .

# Run the application
CMD ["python", "app.py"]
```

### 3. docker-compose.yml

```yaml
version: '3.8'

services:
  self-ai:
    build: .
    ports:
      - "8000:8000"
      - "8765:8765"  # WebSocket
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DEFAULT_BACKEND=openai
      - ENVIRONMENT=local
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped

  # Optional: Redis for message queue (Phase 6)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

### 4. Run with Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f self-ai

# Stop services
docker-compose down
```

---

## Cloud Deployment

### AWS Deployment

#### ECS/Fargate

```bash
# Build and push to ECR
aws ecr create-repository --repository-name self-ai
docker build -t <account-id>.dkr.ecr.<region>.amazonaws.com/self-ai:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/self-ai:latest

# Create ECS task definition (seeecs-task-definition.json)
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# Run task
aws ecs start-task --cluster self-ai-cluster --task-definition self-ai
```

#### ECS Task Definition Template

```json
{
  "family": "self-ai",
  "cpu": "2048",
  "memory": "4096",
  "containerDefinitions": [{
    "name": "self-ai",
    "image": "<account-id>.dkr.ecr.<region>.amazonaws.com/self-ai:latest",
    "essential": true,
    "portMappings": [
      {"containerPort": 8000},
      {"containerPort": 8765}
    ],
    "environment": [
      {"name": "ENVIRONMENT", "value": "docker"},
      {"name": "DEFAULT_BACKEND", "value": "openai"}
    ],
    "secrets": [
      {"name": "OPENAI_API_KEY", "valueFrom": "arn:aws:secretsmanager:..."}
    ]
  }]
}
```

### Google Cloud Platform

#### Cloud Run

```bash
# Build and push to Artifact Registry
gcloud artifacts repositories create self-ai --repository-format=docker
gcloud builds submit --tag gcr.io/<project>/self-ai:latest

# Deploy to Cloud Run
gcloud run deploy self-ai \
  --image gcr.io/<project>/self-ai:latest \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 2 \
  --port 8000
```

### Azure Container Instances

```bash
# Build and push to ACR
az acr create --resource-group self-ai-rg --name selfairegistry
az acr build --registry selfairegistry --image self-ai:latest .

# Deploy to Container Instances
az container create \
  --resource-group self-ai-rg \
  --name self-ai \
  --image selfairegistry.azurecr.io/self-ai:latest \
  --ports 8000 8765 \
  --environment-variables ENVIRONMENT=docker
```

---

## Environment Configuration

### Configuration File Structure

```
Self_AI/
├── config/
│   ├── default.yaml          # Default settings
│   ├── development.yaml     # Dev overrides
│   ├── production.yaml      # Prod settings
│   ├── type-checking.yaml    # Type checker config (Phase 0)
│   ├── dual-loop.yaml       # Dual-loop config (Phase 6)
│   ├── backend-routing.yaml # Backend routing rules (Phase 8)
│   └── environment-routing.yaml # Env routing rules (Phase 8)
├── app.py
└── rlm/
    └── ...
```

### Configuration Options

#### Backend Routing (`config/backend-routing.yaml`)

```yaml
version: "0.1"
backends:
  rlm_internal:
    provider: "openai"
    description: "Internal RLM-backed model"
  claude_agent:
    provider: "anthropic"
    description: "Claude Agent SDK"

defaults:
  fallback_backend: "rlm_internal"
  global_cost_priority: "medium"
  global_quality_priority: "high"

rules:
  - name: "cheap_simple_research"
    when:
      intent: "web_research"
      complexity_score: "<0.4"
    choose:
      backend: "rlm_internal"

  - name: "deep_research_claude"
    when:
      intent: "web_research"
      complexity_score: ">=0.4"
    choose:
      backend: "claude_agent"
```

#### Environment Routing (`config/environment-routing.yaml`)

```yaml
version: "0.1"
environments:
  local:
    type: "local"
    description: "Local REPL execution"
  docker:
    type: "docker"
    description: "Docker containerized execution"
  modal:
    type: "modal"
    description: "Modal cloud sandbox"

defaults:
  fallback_environment: "local"
  security_level: "medium"

rules:
  - name: "internet_required"
    when:
      needs_internet: true
    choose:
      environment: "docker"

  - name: "sandbox_required"
    when:
      needs_docker_isolation: true
    choose:
      environment: "docker"

  - name: "lean_verification"
    when:
      needs_lean_access: true
    choose:
      environment: "local"
```

### Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes* | - | OpenAI API key |
| `ANTHROPIC_API_KEY` | Yes* | - | Anthropic API key |
| `MINIMAX_API_KEY` | Yes* | - | MiniMax API key |
| `DEFAULT_BACKEND` | No | `openai` | Default LLM backend |
| `ENVIRONMENT` | No | `local` | Default execution environment |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `ENABLE_KEY_ENCRYPTION` | No | `true` | Enable key encryption |
| `REDIS_URL` | No | - | Redis URL for message queue |
| `MODAL_TOKEN_ID` | No | - | Modal API token |
| `PRIME_API_KEY` | No | - | Prime Intellect API key |

*At least one API key is required.

---

## Type Checking Setup (Optional)

### Haskell Type Checking (GHC)

#### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install -y ghc libghc-dimensions-dev
```

#### macOS

```bash
brew install ghc cabal-install
cabal update
cabal install dimensions
```

#### Verify GHC Installation

```bash
ghc --version
# Should output: The Glorious Glasgow Haskell Compilation System, version x.x.x
```

### Lean 4 Verification (Lake)

#### Ubuntu/Debian

```bash
# Install Elan (Lean version manager)
curl -fsSL https://github.com/leanprover/elan/releases/download/elan-v3.0.0/elan-x86_64-unknown-linux-gnu.tar.gz | tar xz
sudo mv elan /usr/local/bin/

# Install Lean 4
elan toolchain install leanprover/lean4:v4.8.0
elan default leanprover/lean4:v4.8.0
```

#### macOS

```bash
brew install leanprover/lean/elan
elan toolchain install leanprover/lean4:v4.8.0
elan default leanprover/lean4:v4.8.0
```

#### Windows

```powershell
# Install via scoop
scoop install elan
elan toolchain install leanprover/lean4:v4.8.0
elan default leanprover/lean4:v4.8.0
```

#### Verify Lake Installation

```bash
lake --version
# Should output: Lake version x.x.x
```

### Type Checking Configuration

```yaml
# config/type-checking.yaml
haskell:
  enabled: true
  ghc_path: "ghc"
  timeout_seconds: 30

lean:
  enabled: true
  lake_path: "lake"
  mathlib: true
  timeout_seconds: 60
```

---

## Security Considerations

### API Key Management

1. **Never commit API keys** to version control
2. **Use environment variables** or secrets management
3. **Enable encryption** for stored keys
4. **Rotate keys regularly**

### Docker Security

```dockerfile
# Run as non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Read-only filesystem (if possible)
ReadonlyRootfs: true

# No privilege escalation
NoNewPrivileges: true
```

### Network Security

- Use TLS for all API communications
- Restrict access to WebSocket ports
- Implement rate limiting
- Use network segmentation in production

### Sandbox Security

- Enable Docker isolation for untrusted code
- Use cloud sandboxes (Modal, Prime) for production
- Implement resource quotas
- Monitor for suspicious activity

---

## Troubleshooting

### Common Issues

#### Import Errors

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
uv pip install -e .
```

#### WebSocket Connection Issues

```bash
# Check port availability
lsof -i :8765

# Verify firewall rules
sudo ufw allow 8765
```

#### Docker Build Failures

```bash
# Clear Docker cache
docker builder prune

# Build with no cache
docker build --no-cache -t self-ai:latest .
```

#### Type Checking Not Working

```bash
# Verify GHC installation
ghc --version

# Verify Lake installation
lake --version

# Check configuration
cat config/type-checking.yaml
```

### Logs

Application logs are written to:
- Development: `logs/` directory
- Docker: Use `docker logs <container>`
- Cloud: Check cloud logging service

### Getting Help

1. Check the [implementation plan](plans/IMPLEMENTATION_PLAN.md)
2. Review [existing issues](https://github.com/your-org/Self_AI/issues)
3. Submit a new issue with:
   - System information
   - Steps to reproduce
   - Expected vs actual behavior
   - Relevant logs

---

## Next Steps

After deployment, refer to the [Implementation Plan](plans/IMPLEMENTATION_PLAN.md) for:

- **Phase 0**: Type Checking System setup
- **Phase 1-4**: Core runtime deployment
- **Phase 6+**: Dual-Loop and advanced features
- **Phase 16**: Production hardening

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-28 | 1.0 | Initial deployment guide |
