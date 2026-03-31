# RLM Routing Upgrade Overview (Backends + Environments)

**Version**: 0.1  
**Goal**: Upgrade the existing RLM+Lean system to support dynamic **backend client selection** and **execution environment selection** for *sub-calls*, without hardcoding specific agents.  
**Assumption**: The main orchestrator remains an RLM instance running on `LocalREPL`.

---

## 1. Current Baseline

### 1.1 Orchestrator

- The **main system** is a Recursive Language Model (RLM) instance (as in Alex Zhang's design) using `LocalREPL` as its environment.
- It:
  - Parses open-ended user tasks
  - Decomposes them recursively into subtasks / sub-calls
  - Executes code via `LocalREPL` to manage context, tools, and Lean/Haskell verification

### 1.2 Verification Stack (Unchanged)

- **Lean 4 + Haskell** provide deterministic verification of:
  - Structural constraints (Haskell dimensional types)
  - Physical/engineering correctness (Lean axioms and theorems)
- Verification always runs **locally** inside `LocalREPL` (Lean & Haskell installed in the host venv).

### 1.3 No Hardcoded Agents

- There are no baked-in "ResearchAgent", "PhysicistAgent", etc.
- Instead, the orchestrator spawns **subtasks / sub-calls** that *behave like* roles:
  - e.g., one sub-call may do web research, another may auto-formalize into Lean, another may validate proofs.
- This gives the system maximum freedom to evolve new roles and workflows over time.

---

## 2. What This Upgrade Adds

We add two orthogonal routing layers that operate **per sub-call**:

1. **Backend Routing** — *Which model / harness* should answer this sub-call?
   - Examples: `rlm_internal`, `claude_agent`, `openai`, `local_model`.

2. **Environment Routing** — *Where should the code for this sub-call execute*?
   - Examples: `local` (LocalREPL), `docker` (DockerREPL), `modal` (Modal Sandboxes).

The orchestrator remains on `LocalREPL`, but when it needs to create a sub-call, it will:

```text
1. Analyze the subtask (capabilities, complexity, safety).
2. Ask BackendRouter → choose backend client.
3. Ask EnvironmentRouter → choose execution environment.
4. Instantiate a new RLM sub-instance with those choices.
5. Run the sub-call, collect results, continue recursion.
```

No fixed agent classes are required; roles emerge from how subtasks are labeled and routed.

---

## 3. Conceptual Model

### 3.1 Sub-Call Metadata

Every sub-call is described by a **Task Descriptor** that includes:

```yaml
# Example sub-call descriptor
subtask_id: "task-001:sub-003"
parent_task_id: "task-001"

intent: "web_research"           # what it is trying to do
capabilities:
  needs_internet: true
  needs_filesystem: true
  needs_lean_access: false
  needs_haskell_access: false
  needs_docker_isolation: true

priority: "high"                  # affects backend choice
complexity_score: 0.7             # 0.0-1.0 heuristic
latency_budget_ms: 5000
cost_sensitivity: "medium"

input_summary:
  token_estimate: 3000
  description: "Gather thermodynamics rules for food-safe cooling system"
```

The orchestrator generates this descriptor **programmatically** from the recursive reasoning process (e.g., by adding small helper functions that classify subtasks).

### 3.2 Routers

Two small pure functions (or objects) operate on the descriptor:

- `BackendRouter.choose_backend(task_descriptor) -> backend_id`
- `EnvironmentRouter.choose_env(task_descriptor) -> env_id`

Where:

- `backend_id` might be one of: `"rlm_internal"`, `"claude_agent"`, `"openai_gpt"`, `"local_llama"`, etc.
- `env_id` might be one of: `"local"`, `"docker"`, `"modal"`.

The orchestrator then does something conceptually like:

```python
backend_id = BackendRouter.choose_backend(desc)
env_id = EnvironmentRouter.choose_env(desc)

sub_rlm = RLM(
    backend=backend_id,
    environment=env_id,
    **env_specific_kwargs
)

result = sub_rlm.completion(prompt=subtask_prompt)
```

The rest of the RLM recursion mechanism is unchanged.

---

## 4. Backend Routing (High-Level)

### 4.1 Goals

- Use **stronger / more expensive** models only when necessary.
- Route low-stakes, low-complexity subtasks to **cheaper / faster** backends.
- Capture feedback from **Lean/Haskell verification** about which backend works best for which type of subtasks.

### 4.2 Signals

Backend decisions can consider:

- `intent`: e.g. `"web_research"`, `"code_generation"`, `"proof_synthesis"`, `"refactoring"`, `"summarization"`.
- `complexity_score`: estimated difficulty or size of the problem.
- `latency_budget_ms`: how urgent is this subtask?
- `cost_sensitivity`: whether we care more about cheapness or quality.
- Historical performance metrics (per backend and intent):
  - Lean pass rate
  - Average iterations to pass
  - Average latency/cost

The detailed configuration schema and examples live in `backend-routing-config.md` (separate document).

---

## 5. Environment Routing (High-Level)

### 5.1 Goals

- Keep **Lean/Haskell verification** and local file operations on `LocalREPL`.
- Move **internet-facing and potentially unsafe** operations into **isolated environments**:
  - `docker`: local container with external network access
  - `modal`: remote sandbox with internet and managed infra
- Maintain a "plug-and-play" experience for users:
  - Default to `local` and `docker` where possible
  - Treat cloud environments (Modal) as optional enhancements

### 5.2 Signals

Environment decisions can consider:

- `needs_internet` (true/false)
- `needs_docker_isolation` (e.g. may install packages or run untrusted code)
- `needs_lean_access` / `needs_haskell_access`
- `data_sensitivity` (e.g., local-only vs safe-to-send-to-cloud)
- Deployment mode ("dev", "local_demo", "hosted")

The detailed configuration schema and examples live in `environment-routing-config.md` (separate document).

---

## 6. How This Respects "No Hardcoded Agents"

Instead of writing code like:

```python
if agent_role == "ResearchAgent":
    backend = "claude_agent"
    env = "docker"
```

We keep everything expressed in terms of **subtask properties**, not named classes. For example:

```python
if desc.intent == "web_research" and desc.capabilities["needs_internet"]:
    env = "docker"
    backend = "claude_agent"
```

- The **orchestrator** is free to invent new intents (e.g. `"thermal_simulation"`) over time.
- The routers operate purely on descriptors; they don’t know or care about specific "agents".
- If you later decide to materialize persistent agent classes (for observability or logging), they can simply wrap the same routing logic.

---

## 7. RLM-Orchestrator Perspective

From the main RLM’s point of view:

- It continues to run on **`LocalREPL`** and manage:
  - The global context / memory
  - The Lean/Haskell verification stack
  - The message queue / task graph (if you use one)
- When it needs a subtask solved, it:
  1. Creates a **Task Descriptor**.
  2. Calls **BackendRouter** and **EnvironmentRouter**.
  3. Constructs a **sub-RLM instance** configured with the selected backend & environment.
  4. Issues the sub-call and merges results back into the main reasoning trace.

No part of this requires hardcoding agents; it’s all driven by descriptors and small routing policies.

---

## 8. Planned Companion Documents

This overview describes *what* we’re adding and *why*. Implementation-level details are split into two additional documents:

1. **`backend-routing-config.md`**
   - Schema for backend routing policies
   - Examples for different backends (RLM, Claude, OpenAI, local)
   - How to log, monitor, and tune backend selection

2. **`environment-routing-config.md`**
   - Schema for environment routing policies
   - How to integrate `DockerREPL` and `Modal` without changing the main orchestrator
   - Security and plug-and-play considerations

These documents are designed to be ingested by your AI IDE and used to generate the actual routing modules.

---

## 9. Non-Goals

This upgrade **does not**:

- Change your Lean/Haskell axiomatic stack.
- Change how RLM recursion or LocalREPL itself works.
- Force you to use a specific model provider (Claude, OpenAI, etc.).
- Hardcode any fixed agent roles.

It only adds a **thin, configurable routing layer** to choose:

- Which backend to call per subtask
- Which environment to execute the subtask in

while keeping everything else as flexible and emergent as it is today.
