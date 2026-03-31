# Backend Diversity and Environment Flexibility Plan

## Overview

The Self-Improving Swarm System must support diverse backend clients and execution environments to maximize the effectiveness of the agent swarm. This plan outlines how different agents can leverage different backends and environments based on their specific task requirements.

## Backend Client Support

### Current Supported Backends
From the existing RLM system, we have support for:
- OpenAI
- Anthropic
- Google Gemini
- Azure OpenAI
- LiteLLM
- Portkey
- OpenRouter
- Vercel
- vLLM

### Backend Selection Criteria

Each agent can select the most appropriate backend based on:

#### 1. Task Type Matching
- **Code Generation**: OpenAI GPT-4, Claude-3, or similar
- **Mathematical Reasoning**: Models with strong reasoning capabilities
- **Creative Tasks**: Models with creative strengths
- **Factual Queries**: Models with knowledge cutoff dates appropriate for the query
- **Multimodal Tasks**: Models supporting image/text inputs

#### 2. Performance Characteristics
- **Speed**: Fast models for time-sensitive tasks
- **Accuracy**: High-precision models for critical tasks
- **Cost**: Economical models for routine tasks
- **Reliability**: Stable models for mission-critical tasks

#### 3. Capability Requirements
- **Context Window**: Long-context models for tasks requiring extensive memory
- **Function Calling**: Models supporting tool use
- **Code Interpreter**: Models with code execution capabilities
- **Specialized Skills**: Domain-specific fine-tuned models

### Dynamic Backend Assignment

#### Agent Decision Process
```python
def select_optimal_backend(self, task_description: str) -> str:
    """
    Select the most appropriate backend for a given task.
    """
    # Analyze task requirements
    task_analysis = self.analyze_task_requirements(task_description)
    
    # Match requirements to backend capabilities
    suitable_backends = self.match_backends_to_requirements(task_analysis)
    
    # Score backends based on multiple factors
    scored_backends = self.score_backends(suitable_backends, task_analysis)
    
    # Select optimal backend
    optimal_backend = max(scored_backends, key=lambda x: x['score'])
    
    return optimal_backend['backend_id']
```

#### Backend Profiling
Maintain profiles for each backend including:
- Performance metrics for different task types
- Cost characteristics
- Availability and reliability data
- Specialized capabilities
- Current load and response times

## Execution Environment Support

### Current Environment Types
From the existing RLM system:
- Local REPL
- Docker REPL
- Modal REPL
- Prime REPL
- Daytona REPL
- E2B REPL

### Environment Selection Criteria

#### 1. Security Requirements
- **Sandboxed**: E2B, Docker for untrusted code
- **Restricted**: Limited permissions for safety
- **Privileged**: Full system access when needed

#### 2. Resource Requirements
- **Lightweight**: Local REPL for simple tasks
- **Scalable**: Cloud environments for intensive computation
- **GPU Access**: Specialized environments for ML tasks
- **Memory Intensive**: High-memory environments

#### 3. Dependency Management
- **Pre-installed Packages**: Environments with specific libraries
- **Custom Images**: Tailored environments for domain tasks
- **Isolated**: Clean environments for reproducible results

### Dynamic Environment Assignment

#### Agent Decision Process
```python
def select_optimal_environment(self, task_requirements: dict) -> str:
    """
    Select the most appropriate execution environment for a task.
    """
    # Analyze task requirements
    env_requirements = self.extract_env_requirements(task_requirements)
    
    # Find suitable environments
    suitable_envs = self.find_suitable_environments(env_requirements)
    
    # Score environments based on fit
    scored_envs = self.score_environments(suitable_envs, env_requirements)
    
    # Select optimal environment
    optimal_env = max(scored_envs, key=lambda x: x['score'])
    
    return optimal_env['env_id']
```

## Implementation Architecture

### Backend Abstraction Layer

```python
# backends/abstraction.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time


class BackendInterface(ABC):
    """
    Abstract interface for all backend clients.
    """
    
    @abstractmethod
    async def completion(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Generate completion for the given prompt.
        """
        pass
    
    @abstractmethod
    async def get_token_usage(self) -> Dict[str, int]:
        """
        Get current token usage statistics.
        """
        pass
    
    @abstractmethod
    def get_model_capabilities(self) -> Dict[str, Any]:
        """
        Get the capabilities of the model.
        """
        pass


class BackendManager:
    """
    Manager for handling multiple backend clients.
    """
    
    def __init__(self):
        self.backends: Dict[str, BackendInterface] = {}
        self.backend_profiles: Dict[str, BackendProfile] = {}
        self.load_balancer = LoadBalancer()
    
    def register_backend(self, backend_id: str, backend: BackendInterface, profile: BackendProfile):
        """
        Register a new backend with its profile.
        """
        self.backends[backend_id] = backend
        self.backend_profiles[backend_id] = profile
    
    async def route_request(self, task_description: str, request_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route a request to the most appropriate backend.
        """
        # Determine optimal backend for this request
        optimal_backend_id = await self.select_optimal_backend(task_description)
        
        # Route the request
        backend = self.backends[optimal_backend_id]
        result = await backend.completion(**request_params)
        
        # Update performance metrics
        await self.update_performance_metrics(optimal_backend_id, result)
        
        return result
    
    async def select_optimal_backend(self, task_description: str) -> str:
        """
        Select the optimal backend for a given task.
        """
        # Analyze task requirements
        task_type = self.classify_task(task_description)
        
        # Get backends suitable for this task type
        suitable_backends = [
            bid for bid, profile in self.backend_profiles.items()
            if task_type in profile.supported_tasks
        ]
        
        # Score backends based on current conditions
        scores = {}
        for backend_id in suitable_backends:
            score = await self.calculate_backend_score(backend_id, task_type)
            scores[backend_id] = score
        
        # Return the highest-scoring backend
        return max(scores, key=scores.get) if scores else list(self.backends.keys())[0]
    
    async def calculate_backend_score(self, backend_id: str, task_type: str) -> float:
        """
        Calculate a score for a backend given a task type.
        """
        profile = self.backend_profiles[backend_id]
        current_load = await self.get_current_load(backend_id)
        
        # Calculate score based on multiple factors
        capability_score = profile.capability_scores.get(task_type, 0.0)
        performance_score = profile.performance_metrics.get(task_type, {}).get('avg_response_time', float('inf'))
        cost_score = profile.cost_per_thousand_tokens
        availability_score = profile.availability
        
        # Normalize and combine scores
        normalized_perf_score = 1.0 / (1.0 + performance_score / 1000)  # Lower response time is better
        normalized_cost_score = 1.0 / (1.0 + cost_score)  # Lower cost is better
        
        # Weighted combination (weights can be adjusted based on priorities)
        final_score = (
            0.4 * capability_score +
            0.3 * normalized_perf_score +
            0.2 * availability_score +
            0.1 * normalized_cost_score
        )
        
        # Adjust for current load
        load_factor = 1.0 - min(current_load, 1.0)  # Higher load reduces score
        final_score *= load_factor
        
        return final_score
```

### Environment Abstraction Layer

```python
# environments/abstraction.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio


class EnvironmentInterface(ABC):
    """
    Abstract interface for all execution environments.
    """
    
    @abstractmethod
    async def execute_code(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute code in the environment.
        """
        pass
    
    @abstractmethod
    async def install_package(self, package_name: str) -> bool:
        """
        Install a package in the environment.
        """
        pass
    
    @abstractmethod
    async def get_resource_usage(self) -> Dict[str, Any]:
        """
        Get current resource usage of the environment.
        """
        pass


class EnvironmentManager:
    """
    Manager for handling multiple execution environments.
    """
    
    def __init__(self):
        self.environments: Dict[str, EnvironmentInterface] = {}
        self.env_profiles: Dict[str, EnvironmentProfile] = {}
    
    def register_environment(self, env_id: str, environment: EnvironmentInterface, profile: EnvironmentProfile):
        """
        Register a new environment with its profile.
        """
        self.environments[env_id] = environment
        self.env_profiles[env_id] = profile
    
    async def execute_in_optimal_env(self, code: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute code in the most appropriate environment.
        """
        # Determine optimal environment for this code
        optimal_env_id = await self.select_optimal_environment(requirements)
        
        # Execute in the selected environment
        env = self.environments[optimal_env_id]
        result = await env.execute_code(code)
        
        return result
    
    async def select_optimal_environment(self, requirements: Dict[str, Any]) -> str:
        """
        Select the optimal environment based on requirements.
        """
        # Filter environments based on hard requirements
        suitable_envs = [
            eid for eid, profile in self.env_profiles.items()
            if self.meets_hard_requirements(profile, requirements)
        ]
        
        if not suitable_envs:
            # Fallback to any environment if no suitable ones found
            return list(self.environments.keys())[0] if self.environments else None
        
        # Score suitable environments
        scores = {}
        for env_id in suitable_envs:
            score = await self.calculate_env_score(env_id, requirements)
            scores[env_id] = score
        
        # Return the highest-scoring environment
        return max(scores, key=scores.get) if scores else suitable_envs[0]
    
    def meets_hard_requirements(self, profile: EnvironmentProfile, requirements: Dict[str, Any]) -> bool:
        """
        Check if an environment meets hard requirements.
        """
        # Check security requirements
        if requirements.get('secure_execution') and not profile.is_sandboxed:
            return False
        
        # Check resource requirements
        if requirements.get('gpu_required') and not profile.has_gpu:
            return False
        
        # Check memory requirements
        if requirements.get('min_memory_gb', 0) > profile.memory_gb:
            return False
        
        # Check package requirements
        required_packages = requirements.get('required_packages', [])
        if not all(pkg in profile.installed_packages for pkg in required_packages):
            return False
        
        return True
    
    async def calculate_env_score(self, env_id: str, requirements: Dict[str, Any]) -> float:
        """
        Calculate a score for an environment given requirements.
        """
        profile = self.env_profiles[env_id]
        
        # Calculate score based on how well the environment matches requirements
        score = 0.0
        
        # Resource adequacy
        if requirements.get('min_memory_gb', 0) <= profile.memory_gb:
            score += 20  # Adequate memory
        
        if requirements.get('min_cpu_cores', 0) <= profile.cpu_cores:
            score += 15  # Adequate CPU
        
        if requirements.get('gpu_required', False) == profile.has_gpu:
            score += 25  # GPU requirement matched
        
        # Security match
        if requirements.get('secure_execution', False) == profile.is_sandboxed:
            score += 30  # Security requirement matched
        
        # Package availability
        required_packages = requirements.get('required_packages', [])
        available_packages = set(profile.installed_packages)
        required_set = set(required_packages)
        
        if required_set.issubset(available_packages):
            score += 10  # All packages available
        else:
            # Partial match - score based on coverage
            coverage = len(required_set.intersection(available_packages)) / len(required_set) if required_set else 1.0
            score += coverage * 10
        
        # Performance factor
        avg_response_time = profile.avg_response_time
        if avg_response_time:
            # Lower response time gets higher score
            score += max(0, 20 - (avg_response_time / 100))  # Scale appropriately
        
        return score
```

## Agent-Level Backend and Environment Selection

### Enhanced Agent Class

```python
# agents/intelligent_agent.py
from agents.base_agent import BaseAgent, AgentConfig
from backends.abstraction import BackendManager
from environments.abstraction import EnvironmentManager


class IntelligentAgent(BaseAgent):
    """
    An agent that can intelligently select backends and environments.
    """
    
    def __init__(self, agent_id: str, config: AgentConfig, parent_id: Optional[str] = None):
        super().__init__(agent_id, config, parent_id)
        
        # Reference to global managers (these would be singleton instances)
        self.backend_manager = BackendManager.get_instance()
        self.env_manager = EnvironmentManager.get_instance()
        
        # Agent-specific preferences and learned behaviors
        self.preference_model = AgentPreferenceModel()
    
    async def execute_task_with_optimal_resources(self, task_description: str) -> Any:
        """
        Execute a task using optimally selected backend and environment.
        """
        # Analyze the task to determine requirements
        task_analysis = await self.analyze_task(task_description)
        
        # Select optimal backend
        optimal_backend = await self.select_optimal_backend(task_analysis)
        
        # Select optimal environment
        optimal_env = await self.select_optimal_environment(task_analysis)
        
        # Update the agent's RLM to use the selected backend
        self.rlm = self._create_rlm_with_backend(optimal_backend)
        
        # Execute the task
        result = await self.execute_task(task_description)
        
        # Learn from the experience
        await self.learn_from_experience(task_analysis, optimal_backend, optimal_env, result)
        
        return result
    
    async def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """
        Analyze a task to determine its requirements.
        """
        # Use the current RLM to analyze the task
        analysis_prompt = f"""
        Analyze the following task and determine its requirements:

        Task: {task_description}

        Provide your analysis in the following format:
        {{
            "task_type": "classification of the task (e.g., 'code_generation', 'mathematical_reasoning', 'creative_writing')",
            "complexity_level": "simple, medium, complex, or expert",
            "security_requirements": "low, medium, high (whether code execution needs to be sandboxed)",
            "resource_requirements": {{
                "estimated_memory_gb": "estimated memory needed",
                "estimated_compute_minutes": "estimated compute time",
                "gpu_needed": "true or false"
            }},
            "special_requirements": ["list of special requirements like 'long_context', 'multimodal', etc."]
        }}
        """
        
        analysis_result = self.rlm.completion(analysis_prompt)
        
        try:
            import json
            analysis = json.loads(analysis_result.response)
        except:
            # Fallback if JSON parsing fails
            analysis = {
                "task_type": "general",
                "complexity_level": "medium",
                "security_requirements": "medium",
                "resource_requirements": {
                    "estimated_memory_gb": 1,
                    "estimated_compute_minutes": 5,
                    "gpu_needed": False
                },
                "special_requirements": []
            }
        
        return analysis
    
    async def select_optimal_backend(self, task_analysis: Dict[str, Any]) -> str:
        """
        Select the optimal backend for the task.
        """
        # First try to use learned preferences
        preferred_backend = self.preference_model.get_preferred_backend(
            task_analysis['task_type'],
            task_analysis['complexity_level']
        )
        
        if preferred_backend and preferred_backend in self.backend_manager.backends:
            return preferred_backend
        
        # Fall back to manager's selection
        return await self.backend_manager.select_optimal_backend(
            f"Task type: {task_analysis['task_type']}, Complexity: {task_analysis['complexity_level']}"
        )
    
    async def select_optimal_environment(self, task_analysis: Dict[str, Any]) -> str:
        """
        Select the optimal environment for the task.
        """
        # Prepare requirements dict
        requirements = {
            'secure_execution': task_analysis['security_requirements'] in ['high', 'medium'],
            'min_memory_gb': task_analysis['resource_requirements'].get('estimated_memory_gb', 1),
            'min_cpu_cores': 1,  # Basic assumption
            'gpu_required': task_analysis['resource_requirements'].get('gpu_needed', False),
            'required_packages': self._infer_required_packages(task_analysis)
        }
        
        # First try to use learned preferences
        preferred_env = self.preference_model.get_preferred_environment(
            task_analysis['task_type'],
            requirements
        )
        
        if preferred_env and preferred_env in self.env_manager.environments:
            return preferred_env
        
        # Fall back to manager's selection
        return await self.env_manager.select_optimal_environment(requirements)
    
    def _infer_required_packages(self, task_analysis: Dict[str, Any]) -> list:
        """
        Infer what packages might be needed based on task analysis.
        """
        task_type = task_analysis['task_type']
        
        package_map = {
            'code_generation': ['python'],
            'data_analysis': ['pandas', 'numpy', 'matplotlib'],
            'machine_learning': ['scikit-learn', 'tensorflow', 'pytorch'],
            'web_development': ['flask', 'django', 'requests'],
            'mathematical_reasoning': ['sympy', 'numpy', 'scipy']
        }
        
        return package_map.get(task_type, [])
    
    async def learn_from_experience(self, task_analysis: Dict[str, Any], 
                                    backend_used: str, env_used: str, result: Any):
        """
        Learn from the experience to improve future selections.
        """
        # Evaluate the quality of the result
        success_metric = await self.evaluate_result_quality(result)
        
        # Update preference model
        self.preference_model.update_preferences(
            task_type=task_analysis['task_type'],
            complexity=task_analysis['complexity_level'],
            backend_used=backend_used,
            env_used=env_used,
            success_metric=success_metric
        )
    
    async def evaluate_result_quality(self, result: Any) -> float:
        """
        Evaluate the quality of a result (returns a score between 0 and 1).
        """
        # This is a simplified evaluation - in practice, this could be much more sophisticated
        if result and str(result).strip():
            # Simple heuristic: non-empty results get higher scores
            return min(1.0, len(str(result).strip()) / 100.0)
        return 0.0
    
    def _create_rlm_with_backend(self, backend_id: str):
        """
        Create a new RLM instance with the specified backend.
        """
        # Get backend configuration
        backend_config = self.backend_manager.get_backend_config(backend_id)
        
        # Create new RLM with the backend
        return RLM(
            backend=backend_config['type'],
            backend_kwargs=backend_config['kwargs'],
            environment=self.config.environment,
            environment_kwargs=self.config.environment_kwargs,
            depth=self.config.depth if hasattr(self.config, 'depth') else 0,
            max_depth=self.config.max_depth,
            max_iterations=self.config.max_iterations,
            max_budget=self.config.max_budget,
            max_timeout=self.config.max_timeout,
            max_tokens=self.config.max_tokens,
            max_errors=self.config.max_errors,
            custom_system_prompt=self.config.custom_system_prompt,
            logger=self.rlm.logger if self.rlm else None,
            verbose=False,
            persistent=False,
            custom_tools=self.config.custom_tools,
            custom_sub_tools=self.config.custom_sub_tools,
            compaction=self.config.compaction,
            compaction_threshold_pct=self.config.compaction_threshold_pct,
        )
```

## System-Level Coordination

### Global Resource Manager

```python
# system/resource_manager.py
from typing import Dict, List, Tuple
from dataclasses import dataclass
import asyncio
import time


@dataclass
class ResourceAllocation:
    agent_id: str
    backend_id: str
    environment_id: str
    allocated_at: float
    estimated_duration: float


class ResourceManager:
    """
    System-level manager for coordinating backend and environment resources.
    """
    
    def __init__(self):
        self.allocations: Dict[str, ResourceAllocation] = {}
        self.backend_usage: Dict[str, List[float]] = {}  # Track usage over time
        self.env_usage: Dict[str, List[float]] = {}
        self.lock = asyncio.Lock()
    
    async def allocate_resources(self, agent_id: str, backend_req: str, env_req: str, 
                                estimated_duration: float) -> Tuple[str, str]:
        """
        Allocate backend and environment resources to an agent.
        """
        async with self.lock:
            # Find available backend
            optimal_backend = await self.find_available_backend(backend_req)
            
            # Find available environment
            optimal_env = await self.find_available_env(env_req)
            
            # Record allocation
            allocation = ResourceAllocation(
                agent_id=agent_id,
                backend_id=optimal_backend,
                environment_id=optimal_env,
                allocated_at=time.time(),
                estimated_duration=estimated_duration
            )
            
            self.allocations[agent_id] = allocation
            
            # Update usage tracking
            if optimal_backend not in self.backend_usage:
                self.backend_usage[optimal_backend] = []
            self.backend_usage[optimal_backend].append(time.time())
            
            if optimal_env not in self.env_usage:
                self.env_usage[optimal_env] = []
            self.env_usage[optimal_env].append(time.time())
            
            return optimal_backend, optimal_env
    
    async def find_available_backend(self, backend_preference: str) -> str:
        """
        Find an available backend that matches the preference.
        """
        # This is a simplified implementation
        # In reality, this would consider load balancing, availability, etc.
        return backend_preference
    
    async def find_available_env(self, env_preference: str) -> str:
        """
        Find an available environment that matches the preference.
        """
        # This is a simplified implementation
        return env_preference
    
    async def release_resources(self, agent_id: str):
        """
        Release resources allocated to an agent.
        """
        async with self.lock:
            if agent_id in self.allocations:
                del self.allocations[agent_id]
    
    async def get_resource_utilization(self) -> Dict[str, float]:
        """
        Get current resource utilization metrics.
        """
        async with self.lock:
            # Calculate utilization for each backend
            backend_util = {}
            current_time = time.time()
            
            for backend_id, usage_times in self.backend_usage.items():
                # Count usage in the last 5 minutes
                recent_usage = [t for t in usage_times if current_time - t < 300]
                backend_util[backend_id] = len(recent_usage) / 60.0  # Requests per minute
            
            return {
                'backend_utilization': backend_util,
                'total_active_allocations': len(self.allocations)
            }
```

## Integration with Existing Systems

### Extending the Swarm RLM

```python
# rlm/core/swarm_rlm_extended.py
from rlm.core.swarm_rlm import SwarmRLM
from system.resource_manager import ResourceManager


class ExtendedSwarmRLM(SwarmRLM):
    """
    Extended Swarm RLM with backend and environment diversity support.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource_manager = ResourceManager()
        
        # Initialize backend and environment managers
        self.backend_manager = BackendManager()
        self.env_manager = EnvironmentManager()
    
    def spawn_agent_with_resources(self, task: str, backend_pref: str = None, 
                                  env_pref: str = None) -> str:
        """
        Spawn an agent with specific backend and environment preferences.
        """
        agent_id = str(uuid.uuid4())
        
        # If preferences are specified, try to honor them
        if backend_pref or env_pref:
            # Allocate specific resources
            backend_id, env_id = asyncio.run(
                self.resource_manager.allocate_resources(
                    agent_id, 
                    backend_pref or "default", 
                    env_pref or "default", 
                    estimated_duration=300  # 5 minutes default
                )
            )
        else:
            # Let the agent decide
            backend_id, env_id = "default", "default"
        
        # Create agent configuration with specified resources
        agent_config = AgentConfig(
            backend=backend_id,
            environment=env_id,
            # ... other config
        )
        
        # Create and register the agent
        agent = IntelligentAgent(agent_id, agent_config, parent_id=self.id if hasattr(self, 'id') else None)
        
        with self.agent_lock:
            self.agents[agent_id] = SwarmAgent(
                id=agent_id,
                parent_id=self.id if hasattr(self, 'id') else None,
                task=task,
                status=AgentStatus.IDLE,
                created_at=datetime.now(),
                last_update=datetime.now(),
                backend=backend_id,
                environment=env_id,
                rlm_instance=agent  # Use the intelligent agent
            )
        
        # Start the agent
        agent_thread = threading.Thread(target=self._run_intelligent_agent, args=(agent_id,))
        agent_thread.daemon = True
        agent_thread.start()
        
        return agent_id
    
    def _run_intelligent_agent(self, agent_id: str):
        """
        Run an intelligent agent that can select its own resources.
        """
        agent = self.agents[agent_id]
        agent.status = AgentStatus.EXECUTING
        agent.last_update = datetime.now()
        
        try:
            # The intelligent agent will select its own optimal resources
            result = agent.rlm.execute_task_with_optimal_resources(agent.task)
            agent.status = AgentStatus.COMPLETED
        except Exception as e:
            agent.status = AgentStatus.FAILED
            print(f"Agent {agent_id} failed: {str(e)}")
        finally:
            agent.last_update = datetime.now()
            
            # Release allocated resources
            asyncio.run(self.resource_manager.release_resources(agent_id))
```

This plan provides a comprehensive approach to implementing backend diversity and environment flexibility in the Self-Improving Swarm System, allowing agents to intelligently select the most appropriate resources for their specific tasks.