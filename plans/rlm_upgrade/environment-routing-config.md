# Environment Routing Configuration (RLM Sub-Calls)

**Version**: 0.1  
**Purpose**: Define how the system chooses **which execution environment** (LocalREPL, DockerREPL, Modal, etc.) to use for each RLM sub-call, without hardcoding fixed agents.  
**Companion Docs**: `rlm-routing-upgrade-overview.md`, `backend-routing-config.md`.

---

## 1. Concepts & Definitions

### 1.1 Execution Environment

An **execution environment** is where the sub-call’s code actually runs. In Alex Zhang's RLM library, environments are pluggable and currently include:[code_file:107]

- `local` — **LocalREPL** (Python `exec` in the host process / venv)
- `docker` — **DockerREPL** (code runs inside a Docker container)
- `modal` — **Modal Sandboxes** (remote, serverless sandbox with internet)
- `prime` — **Prime Sandboxes** (slower / beta, possibly for later)

Each environment defines:

- How to start the REPL
- What resources it has access to (filesystem, network, packages)
- How isolation and cleanup are handled

### 1.2 Task Descriptor (Environment-Relevant Fields)

From the full Task Descriptor (see overview doc), the environment router cares about:

```yaml
capabilities:
  needs_internet: bool
  needs_filesystem: bool
  needs_lean_access: bool
  needs_haskell_access: bool
  needs_docker_isolation: bool      # may run arbitrary or untrusted code

security:
  data_sensitivity: "local_only" | "internal" | "external_ok"

performance:
  latency_budget_ms: 500-10000
  expected_cpu_seconds: 1-600

mode: "dev" | "local_demo" | "hosted"
```

The orchestrator populates these based on its own reasoning about the subtask.

---

## 2. Configuration Schema

### 2.1 Top-Level YAML Schema

```yaml
# environment-routing.yaml

version: 0.1

# Define available environments and their properties
environments:
  local:
    kind: "localrepl"
    description: "Host Python REPL (Lean/Haskell installed here)"
    default: true

  docker:
    kind: "dockerrepl"
    description: "Docker container with optional internet access"
    image: "python:3.11-slim"          # default image
    network_mode: "bridge"             # allows outbound internet
    cpu_limit: 1.0
    memory_limit_gb: 2

  modal:
    kind: "modalrepl"
    description: "Modal Sandbox for internet-facing subtasks"
    profile: "default"
    cpu_limit: 2.0
    memory_limit_gb: 4


defaults:
  # Fallback environment if no rule matches
  fallback_environment: "local"

  # Global knobs
  allow_remote_compute_in_dev: false
  strict_local_for_sensitive_data: true


rules:
  - name: "lean_and_haskell_always_local"
    when:
      capabilities.needs_lean_access: true
    choose:
      environment: "local"

  - name: "pure_filesystem_local"
    when:
      capabilities.needs_filesystem: true
      capabilities.needs_internet: false
      security.data_sensitivity: "local_only"
    choose:
      environment: "local"

  - name: "untrusted_code_docker"
    when:
      capabilities.needs_docker_isolation: true
      capabilities.needs_internet: false
    choose:
      environment: "docker"

  - name: "internet_research_dev_mode_docker"
    when:
      mode: "dev"
      capabilities.needs_internet: true
    choose:
      environment: "docker"

  - name: "internet_research_hosted_mode_modal"
    when:
      mode: "hosted"
      capabilities.needs_internet: true
      security.data_sensitivity: "external_ok"
    choose:
      environment: "modal"

  - name: "sensitive_data_force_local"
    when:
      security.data_sensitivity: "local_only"
    choose:
      environment: "local"
```

---

## 3. Matching Semantics

### 3.1 Condition Syntax

Same as backend routing:

- Nested keys: `capabilities.needs_internet`
- Exact matches: `mode: "dev"`
- Booleans: `true` / `false`

Rules are evaluated in order; the first matching rule determines the environment. If none match, `defaults.fallback_environment` is used.

### 3.2 Examples

#### 3.2.1 Lean Proof Sub-Call

```yaml
intent: "proof_synthesis"
capabilities:
  needs_internet: false
  needs_filesystem: true
  needs_lean_access: true
  needs_haskell_access: false
  needs_docker_isolation: false
security:
  data_sensitivity: "local_only"
mode: "dev"
```

Matches rule `lean_and_haskell_always_local` → `environment = "local"`.

#### 3.2.2 Internet Research in Dev Mode

```yaml
intent: "web_research"
capabilities:
  needs_internet: true
  needs_filesystem: false
  needs_lean_access: false
  needs_haskell_access: false
  needs_docker_isolation: false
security:
  data_sensitivity: "internal"
mode: "dev"
```

Matches rule `internet_research_dev_mode_docker` → `environment = "docker"`.

#### 3.2.3 Internet Research in Hosted Mode

```yaml
intent: "web_research"
capabilities:
  needs_internet: true
  needs_filesystem: false
  needs_lean_access: false
  needs_haskell_access: false
  needs_docker_isolation: false
security:
  data_sensitivity: "external_ok"
mode: "hosted"
```

Matches rule `internet_research_hosted_mode_modal` → `environment = "modal"`.

---

## 4. EnvironmentRouter Pseudocode

```python
class EnvironmentRouter:
    def __init__(self, cfg: dict):
        self.cfg = cfg

    def choose_env(self, desc: dict) -> dict:
        env_id = self._match_rules(desc)
        return {
            "environment": env_id,
            "rule": desc.get("_matched_rule", "fallback"),
        }

    def _match_rules(self, features: dict) -> str:
        for rule in self.cfg["rules"]:
            if self._matches(rule["when"], features):
                features["_matched_rule"] = rule["name"]
                return rule["choose"]["environment"]
        return self.cfg["defaults"]["fallback_environment"]

    def _matches(self, cond: dict, features: dict) -> bool:
        for key, pattern in cond.items():
            value = self._get_nested(features, key)
            if value != pattern:
                return False
        return True

    def _get_nested(self, obj: dict, key: str):
        parts = key.split(".")
        cur = obj
        for p in parts:
            cur = cur.get(p)
            if cur is None:
                return None
        return cur
```

---

## 5. Integrating With RLM (LocalREPL as Orchestrator)

### 5.1 Root Orchestrator Stays Local

- The **main RLM instance** continues to run on `environment="local"`.
- It uses `LocalREPL` for:
  - Global orchestration logic
  - Lean/Haskell verification
  - Managing task descriptors and routing decisions

### 5.2 Sub-RLM Instances per Environment

For each sub-call, the orchestrator:

1. Builds the **Task Descriptor**.
2. Calls **EnvironmentRouter** to get `env_id`.
3. Uses an `environment_factory` to construct the correct environment object.
4. Constructs a **sub-RLM** with that environment.

Example sketch:

```python
def run_subcall(prompt: str, desc: dict):
    env_route = environment_router.choose_env(desc)
    env_id = env_route["environment"]
    env = environment_factory.get(env_id, config)

    backend_route = backend_router.choose_backend(desc)
    backend_client = backend_factory.get(backend_route["backend"], config)

    sub_rlm = RLM(backend=backend_client, environment=env)
    result = sub_rlm.completion(prompt=prompt)
    return result
```

- The **root RLM** never changes environment.
- It simply instantiates additional RLM objects with `environment="docker"` or `environment="modal"` as needed.

---

## 6. DockerREPL & Internet Access

### 6.1 Docker Image Design

For dev/local-demo mode, we expect users to have Docker installed. You provide a base image, for example:

```dockerfile
# Dockerfile.research
FROM python:3.11-slim

RUN pip install \
    requests \
    httpx \
    beautifulsoup4 \
    arxiv \
    crossrefapi

WORKDIR /app
COPY research_tools/ /app/research_tools/
```

- `DockerREPL` will run the sub-call code in a container from this image.
- With `network_mode: "bridge"`, containers have outbound internet by default (suitable for web research).

### 6.2 Security/Isolation

- Untrusted or internet-facing code can run in Docker without touching the host Python process.
- For highly sensitive setups, you can disable internet or tighten network rules at Docker level.

---

## 7. ModalREPL (Optional Hosted Mode)

### 7.1 Use Case

- In a **hosted / cloud** deployment, instead of requiring users to run Docker locally, you:
  - Keep orchestrator + verification on your servers.
  - Use `environment="modal"` for heavy, internet-facing subtasks.

### 7.2 Pricing & Ops Notes

- Modal is a serverless compute platform with:
  - Per-second CPU billing and generous free credits (sufficient for development and early testing).
  - Fast startup sandboxes designed for LLM agent workloads.

You can treat `modal` as a drop-in replacement for `docker` in the environment routing file for the `hosted` mode.

---

## 8. No Hardcoded Agents, Only Policies

- All environment choices are expressed in terms of **capabilities** and **modes**, not fixed agent names.
- The orchestrator is free to spawn new kinds of subtasks with new `intent` or capability combinations.
- Routing logic lives in this config file + a small router, which the AI IDE can maintain and evolve.

---

## 9. Summary

- **LocalREPL** remains the main orchestrator and verification environment.
- **DockerREPL** is used for local/demo internet-facing or untrusted subtasks.
- **ModalREPL** (optional) is used for hosted production scenarios.
- Environment routing is driven by **Task Descriptor flags**, not hardcoded agent classes.
- This design is compatible with the existing RLM stack and can be added incrementally.
