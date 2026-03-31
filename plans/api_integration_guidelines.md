# API Endpoints and Integration Guidelines for Self-Improving Swarm System

## Overview

This document provides comprehensive API endpoints and integration guidelines for the Self-Improving Swarm System. It covers all the necessary interfaces for interacting with the system, managing agents, monitoring progress, and integrating with external systems.

## API Architecture

### RESTful API Design Principles
- Consistent URL structure
- Standard HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Proper status codes
- JSON request/response format
- Versioned endpoints (v1, v2, etc.)

### Authentication and Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- API keys for programmatic access
- OAuth 2.0 support for third-party integrations

## Core API Endpoints

### 1. Swarm Management Endpoints

#### `/api/v1/swarm/status`
- **Method**: GET
- **Description**: Get overall swarm status and health
- **Authentication**: Required
- **Response**:
```json
{
  "status": "running",
  "activeAgents": 12,
  "totalTasks": 25,
  "completedTasks": 18,
  "failedTasks": 2,
  "systemMetrics": {
    "cpuUsage": 45.2,
    "memoryUsage": 67.8,
    "activeConnections": 8,
    "messageThroughput": 120
  },
  "uptime": 3600000
}
```

#### `/api/v1/swarm/start`
- **Method**: POST
- **Description**: Start the swarm system
- **Authentication**: Required (admin)
- **Request Body**:
```json
{
  "initialTask": "Process complex data analysis",
  "maxAgents": 10,
  "resourceLimits": {
    "cpu": 80,
    "memory": 8000,
    "tokens": 100000
  }
}
```

#### `/api/v1/swarm/stop`
- **Method**: POST
- **Description**: Stop the swarm system gracefully
- **Authentication**: Required (admin)

#### `/api/v1/swarm/pause`
- **Method**: POST
- **Description**: Pause all agent activities
- **Authentication**: Required (admin)

#### `/api/v1/swarm/resume`
- **Method**: POST
- **Description**: Resume all agent activities
- **Authentication**: Required (admin)

### 2. Agent Management Endpoints

#### `/api/v1/agents`
- **Method**: GET
- **Description**: List all agents in the swarm
- **Authentication**: Required
- **Query Parameters**:
  - `status`: Filter by agent status (idle, executing, paused, etc.)
  - `type`: Filter by agent type (main, spawned)
  - `limit`: Number of results to return
  - `offset`: Offset for pagination
- **Response**:
```json
{
  "agents": [
    {
      "id": "agent-123",
      "parentId": null,
      "type": "main",
      "status": "executing",
      "task": "Data analysis task",
      "createdAt": "2023-10-01T10:00:00Z",
      "lastUpdate": "2023-10-01T10:05:30Z",
      "backendClient": "openai-gpt-4",
      "executionEnvironment": "local",
      "resources": {
        "cpuLimit": 50,
        "memoryLimit": 2048,
        "tokenLimit": 10000
      }
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10
}
```

#### `/api/v1/agents/{agentId}`
- **Method**: GET
- **Description**: Get details of a specific agent
- **Authentication**: Required
- **Response**:
```json
{
  "id": "agent-123",
  "parentId": null,
  "type": "main",
  "status": "executing",
  "task": "Data analysis task",
  "createdAt": "2023-10-01T10:00:00Z",
  "lastUpdate": "2023-10-01T10:05:30Z",
  "logs": [
    {
      "timestamp": "2023-10-01T10:00:01Z",
      "level": "info",
      "message": "Agent initialized"
    }
  ],
  "capabilities": {
    "supportedLanguages": ["python", "javascript"],
    "availableTools": ["data_loader", "analyzer"],
    "maxDepth": 3
  },
  "resources": {
    "cpuLimit": 50,
    "memoryLimit": 2048,
    "tokenLimit": 10000
  }
}
```

#### `/api/v1/agents`
- **Method**: POST
- **Description**: Create a new agent (spawning)
- **Authentication**: Required
- **Request Body**:
```json
{
  "task": "Perform statistical analysis on dataset",
  "backendClient": "openai-gpt-4",
  "executionEnvironment": "docker",
  "parentId": "main-instance-456",
  "resources": {
    "cpuLimit": 30,
    "memoryLimit": 1024
  },
  "capabilities": {
    "supportedLanguages": ["python"],
    "maxDepth": 2
  }
}
```

#### `/api/v1/agents/{agentId}/pause`
- **Method**: POST
- **Description**: Pause a specific agent
- **Authentication**: Required

#### `/api/v1/agents/{agentId}/resume`
- **Method**: POST
- **Description**: Resume a specific agent
- **Authentication**: Required

#### `/api/v1/agents/{agentId}/terminate`
- **Method**: DELETE
- **Description**: Terminate a specific agent
- **Authentication**: Required (admin)

#### `/api/v1/agents/{agentId}/send-message`
- **Method**: POST
- **Description**: Send a message to a specific agent
- **Authentication**: Required
- **Request Body**:
```json
{
  "type": "command",
  "content": {
    "title": "Pause and report status",
    "body": "Please pause your current task and report your progress"
  },
  "priority": "high"
}
```

### 3. Task Management Endpoints

#### `/api/v1/tasks`
- **Method**: GET
- **Description**: List all tasks in the system
- **Authentication**: Required
- **Query Parameters**:
  - `status`: Filter by task status
  - `assignedTo`: Filter by agent ID
  - `limit`: Number of results
  - `offset`: Pagination offset
- **Response**:
```json
{
  "tasks": [
    {
      "id": "task-789",
      "description": "Analyze sales data for Q3",
      "assignedTo": "agent-123",
      "status": "in-progress",
      "priority": 2,
      "dependencies": [],
      "estimatedComplexity": 7,
      "createdAt": "2023-10-01T09:00:00Z",
      "startedAt": "2023-10-01T09:05:00Z",
      "result": null,
      "error": null
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10
}
```

#### `/api/v1/tasks`
- **Method**: POST
- **Description**: Submit a new task to the system
- **Authentication**: Required
- **Request Body**:
```json
{
  "description": "Process customer feedback data",
  "priority": 3,
  "estimatedComplexity": 5,
  "constraints": {
    "deadline": "2023-10-02T10:00:00Z",
    "maxTokens": 50000,
    "maxCost": 10.00
  }
}
```

#### `/api/v1/tasks/{taskId}`
- **Method**: GET
- **Description**: Get details of a specific task
- **Authentication**: Required

#### `/api/v1/tasks/{taskId}/assign`
- **Method**: POST
- **Description**: Assign a task to a specific agent
- **Authentication**: Required
- **Request Body**:
```json
{
  "agentId": "agent-456"
}
```

### 4. Communication Endpoints

#### `/api/v1/messages`
- **Method**: GET
- **Description**: Get message history
- **Authentication**: Required
- **Query Parameters**:
  - `sender`: Filter by sender ID
  - `recipient`: Filter by recipient ID
  - `type`: Filter by message type
  - `since`: Filter messages since timestamp
  - `limit`: Number of results
- **Response**:
```json
{
  "messages": [
    {
      "id": "msg-101",
      "sender": "agent-123",
      "recipients": ["agent-456"],
      "type": "status-update",
      "content": {
        "title": "Task Progress Update",
        "body": "Completed 75% of data processing"
      },
      "timestamp": "2023-10-01T10:15:00Z",
      "priority": "normal",
      "status": "read"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10
}
```

#### `/api/v1/messages`
- **Method**: POST
- **Description**: Send a new message
- **Authentication**: Required
- **Request Body**:
```json
{
  "recipients": ["agent-123", "agent-456"],
  "type": "broadcast",
  "content": {
    "title": "System Alert",
    "body": "Resource usage approaching limits"
  },
  "priority": "high"
}
```

#### `/api/v1/messages/{messageId}/read`
- **Method**: POST
- **Description**: Mark a message as read
- **Authentication**: Required

### 5. Tool Management Endpoints

#### `/api/v1/tools`
- **Method**: GET
- **Description**: List all available tools
- **Authentication**: Required
- **Response**:
```json
{
  "tools": [
    {
      "name": "data_analyzer",
      "description": "Analyzes structured data",
      "parameters": [
        {
          "name": "dataset",
          "type": "string",
          "required": true,
          "description": "Path to the dataset"
        }
      ],
      "creator": "agent-123",
      "createdAt": "2023-10-01T08:00:00Z",
      "lastUsed": "2023-10-01T10:00:00Z",
      "usageCount": 45,
      "approved": true
    }
  ]
}
```

#### `/api/v1/tools`
- **Method**: POST
- **Description**: Create a new tool
- **Authentication**: Required
- **Request Body**:
```json
{
  "name": "custom_visualizer",
  "description": "Creates custom data visualizations",
  "implementation": "def custom_visualizer(data, chart_type='bar'): ...",
  "parameters": [
    {
      "name": "data",
      "type": "string",
      "required": true,
      "description": "Data to visualize"
    }
  ]
}
```

#### `/api/v1/tools/{toolName}/approve`
- **Method**: POST
- **Description**: Approve a tool for system-wide use
- **Authentication**: Required (admin)

#### `/api/v1/tools/{toolName}/share`
- **Method**: POST
- **Description**: Share a tool with specific agents
- **Authentication**: Required
- **Request Body**:
```json
{
  "agentIds": ["agent-123", "agent-456"]
}
```

### 6. Improvement Management Endpoints

#### `/api/v1/improvements`
- **Method**: GET
- **Description**: List all system improvements
- **Authentication**: Required
- **Query Parameters**:
  - `status`: Filter by improvement status
  - `creator`: Filter by creator ID
  - `type`: Filter by improvement type
- **Response**:
```json
{
  "improvements": [
    {
      "id": "imp-201",
      "title": "Optimized data loading algorithm",
      "description": "Improved data loading speed by 40%",
      "type": "optimization",
      "category": "efficiency",
      "creator": "agent-789",
      "createdAt": "2023-10-01T07:00:00Z",
      "appliedAt": "2023-10-01T08:00:00Z",
      "status": "applied",
      "impact": "high",
      "affectedComponents": ["data_loader"],
      "testResults": {
        "automatedTestsPassed": 12,
        "automatedTestsTotal": 12,
        "performanceImpact": {
          "before": {"speed": 100},
          "after": {"speed": 140}
        }
      }
    }
  ]
}
```

#### `/api/v1/improvements`
- **Method**: POST
- **Description**: Propose a new improvement
- **Authentication**: Required
- **Request Body**:
```json
{
  "title": "New caching mechanism",
  "description": "Implement LRU caching for frequently accessed data",
  "type": "optimization",
  "category": "efficiency",
  "implementation": {
    "type": "code-change",
    "target": "cache_manager",
    "changes": ["Add LRU cache implementation"],
    "rollbackPlan": "Remove cache and revert to previous implementation"
  },
  "impact": "high",
  "affectedComponents": ["cache_manager", "data_loader"]
}
```

#### `/api/v1/improvements/{improvementId}/approve`
- **Method**: POST
- **Description**: Approve an improvement
- **Authentication**: Required (admin)

#### `/api/v1/improvements/{improvementId}/apply`
- **Method**: POST
- **Description**: Apply an approved improvement
- **Authentication**: Required (admin)

### 7. Real-time WebSocket Endpoints

#### `/ws/v1/notifications`
- **Description**: WebSocket endpoint for real-time notifications
- **Authentication**: Required (via query parameter or header)
- **Message Types**:
  - `agent_status_change`: Agent status update
  - `task_progress`: Task progress update
  - `system_alert`: System alerts
  - `new_message`: New message received
  - `resource_update`: Resource usage update

#### `/ws/v1/agent/{agentId}/terminal`
- **Description**: WebSocket for real-time terminal output of an agent
- **Authentication**: Required

## Integration Guidelines

### 1. Client SDK Development

#### JavaScript/Node.js SDK
```javascript
// Example SDK usage
import { SwarmClient } from '@self-improving-swarm/client';

const client = new SwarmClient({
  baseUrl: 'https://api.swarm-system.com',
  apiKey: 'your-api-key'
});

// Submit a task
const task = await client.tasks.create({
  description: 'Analyze customer data',
  priority: 3
});

// Monitor task progress
client.notifications.subscribe('task_progress', (data) => {
  console.log(`Task ${data.taskId} progress: ${data.progress}%`);
});
```

#### Python SDK
```python
from self_improving_swarm import SwarmClient

client = SwarmClient(base_url='https://api.swarm-system.com', api_key='your-api-key')

# Submit a task
task = client.tasks.create(description='Process large dataset', priority=2)

# Get agent information
agents = client.agents.list(status='executing')
```

### 2. Third-Party Integration Patterns

#### Webhook Integration
```json
{
  "url": "https://your-app.com/webhooks/swarm-events",
  "events": ["task_completed", "agent_failed", "system_alert"],
  "secret": "your-webhook-secret"
}
```

#### Event Subscription
```javascript
// Subscribe to specific events
client.events.subscribe(['agent_status_change', 'task_progress'], (event) => {
  // Handle the event
  processEvent(event);
});
```

### 3. Security Best Practices

#### API Key Management
- Rotate API keys regularly
- Use different keys for different applications
- Restrict key permissions based on need
- Monitor key usage patterns

#### Rate Limiting
- Implement client-side rate limiting
- Use exponential backoff for retries
- Respect server rate limit headers
- Implement circuit breakers for failed requests

#### Data Protection
- Encrypt sensitive data in transit (TLS 1.3+)
- Sanitize input data to prevent injection attacks
- Validate all API responses
- Implement proper error handling without exposing internals

### 4. Error Handling

#### Common Error Responses
```json
{
  "error": {
    "code": "RESOURCE_EXHAUSTED",
    "message": "Insufficient resources to create new agent",
    "details": {
      "availableCpu": 10,
      "requiredCpu": 30,
      "availableMemory": 512,
      "requiredMemory": 1024
    }
  }
}
```

#### HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `429`: Too Many Requests
- `500`: Internal Server Error

### 5. Monitoring and Observability

#### Metrics Collection
- Request rates and response times
- Error rates and types
- Resource utilization
- Agent performance metrics

#### Logging Standards
- Structured logging (JSON format)
- Consistent field naming
- Appropriate log levels
- Sensitive data filtering

#### Health Checks
- System status endpoints
- Dependency health checks
- Performance thresholds
- Automated alerting

### 6. Migration and Versioning

#### API Versioning Strategy
- URL-based versioning (`/api/v1/`, `/api/v2/`)
- Backward compatibility commitments
- Deprecation policies
- Migration guides

#### Breaking Change Management
- Advance notice for breaking changes
- Parallel version support during transition
- Automated migration tools when possible
- Comprehensive documentation updates

This API specification provides a comprehensive interface for interacting with the Self-Improving Swarm System, enabling seamless integration with external applications and services.