# AgentLoopStorage — Specification

## Overview

`AgentLoopStorage` is the **cloud persistence layer** for all RLM agent loop data. It replaces the original SQLite backend (`.agent_loop.db`) with a **PostgREST API** client that writes to **Supabase PostgreSQL**. This gives the agent memory that is accessible from any machine, session, or agent instance.

**Module**: `rlm.storage.agent_loop_storage`
**Class**: `AgentLoopStorage`
**Transport**: PostgREST REST API over HTTPS (port 443) — NOT raw PostgreSQL wire protocol

---

## Architecture

```
RLM Agent Process
    │
    │  AgentLoopStorage.save_*()
    │  AgentLoopStorage.get_*()
    │
    ▼
PostgREST API (Supabase edge)
    https://fwyhjaetoxequqfuktje.supabase.co/rest/v1/{table}
    │
    ▼
Supabase PostgreSQL 17
    Project: PC-System / ref: fwyhjaetoxequqfuktje
    Region: us-east-1
```

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `SUPABASE_URL` | Supabase project URL | Yes |
| `SUPABASE_ANON_KEY` | Supabase anon (client) key | Yes |
| `SUPABASE_KEY` | Alias for `SUPABASE_ANON_KEY` | No |
| `DATABASE_URL` | Alias fallback for `SUPABASE_URL` | No |

If any required variable is missing, the storage becomes a **no-op** (`enabled=False`).

---

## Supabase Project

- **URL**: `https://fwyhjaetoxequqfuktje.supabase.co`
- **Project ref**: `fwyhjaetoxequqfuktje`
- **Project ID**: `PC-System`
- **Region**: `us-east-1`
- **PostgreSQL**: v17
- **Auth**: Anon key used for all API calls (no server-side auth in storage layer)

---

## Database Schema

All tables use **PostgREST naming conventions** (`snake_case`, no schema prefix — `public` schema).

### Table: `llm_calls`
Every LLM API invocation made by the agent engine.

| Column | Type | Description |
|---|---|---|
| `call_id` | `text` PK | Unique call identifier |
| `agent_id` | `text` | Agent instance ID |
| `parent_call_id` | `text` | Parent LLM call if nested |
| `depth` | `integer` | Nesting depth |
| `model` | `text` | Model used (e.g. `gpt-4o`, `claude-3-5-sonnet`) |
| `prompt` | `text` | Full prompt sent |
| `response` | `text` | Full response received |
| `input_tokens` | `integer` | Input token count |
| `output_tokens` | `integer` | Output token count |
| `cost` | `real` | Estimated cost in USD |
| `execution_time` | `real` | Wall-clock time in seconds |
| `call_type` | `text` | Type label (e.g. `completion`, `embedding`) |
| `success` | `integer` | `1` = success, `0` = failure |
| `error` | `text` | Error message if failed |
| `timestamp` | `real` | Unix timestamp (from `time.time()`) |

### Table: `repl_executions`
Every Python REPL code execution.

| Column | Type | Description |
|---|---|---|
| `execution_id` | `text` PK | Unique execution identifier |
| `agent_id` | `text` | Agent instance ID |
| `parent_call_id` | `text` | Parent LLM call that triggered this |
| `code` | `text` | Python code executed |
| `stdout` | `text` | Standard output |
| `stderr` | `text` | Standard error |
| `execution_time` | `real` | Wall-clock time in seconds |
| `success` | `integer` | `1` = success, `0` = failure |
| `error` | `text` | Exception message if failed |
| `return_value_preview` | `text` | String preview of return value |
| `llm_calls_made` | `text` | JSON array of nested LLM call IDs |
| `timestamp` | `real` | Unix timestamp |

### Table: `iterations`
Each complete agent loop iteration.

| Column | Type | Description |
|---|---|---|
| `iteration_id` | `text` PK | Unique iteration identifier |
| `agent_id` | `text` | Agent instance ID |
| `iteration_number` | `integer` | Sequential iteration number |
| `depth` | `integer` | Recursion depth |
| `prompt` | `text` | User/system prompt for this iteration |
| `response` | `text` | Agent's response |
| `code_blocks` | `text` | JSON array of extracted code blocks |
| `final_answer` | `text` | Final answer if iteration concluded |
| `execution_time` | `real` | Wall-clock time in seconds |
| `timestamp` | `real` | Unix timestamp |

### Table: `spawning_events`
Every time an agent spawns a child agent.

| Column | Type | Description |
|---|---|---|
| `event_id` | `text` PK | Unique event identifier |
| `parent_agent_id` | `text` | Spawning agent's ID |
| `child_agent_id` | `text` | Newly spawned agent's ID |
| `child_task` | `text` | Task assigned to child |
| `reason` | `text` | Why this spawning occurred |
| `timestamp` | `real` | Unix timestamp |

### Table: `chain_thoughts`
Individual reasoning steps within an iteration.

| Column | Type | Description |
|---|---|---|
| `step_id` | `text` PK | Unique step identifier |
| `agent_id` | `text` | Agent instance ID |
| `iteration` | `integer` | Iteration number |
| `thought` | `text` | The reasoning content |
| `action` | `text` | Action taken or planned |
| `context` | `text` | JSON object of additional context |
| `timestamp` | `real` | Unix timestamp |

---

## API Methods

### Write Operations

| Method | Description |
|---|---|
| `save_llm_call(call_data)` | Persist an LLM call |
| `save_repl_execution(exec_data)` | Persist a REPL execution |
| `save_iteration(iter_data)` | Persist an iteration |
| `save_spawning_event(spawn_data)` | Persist a spawning event |
| `save_chain_thought(cot_data)` | Persist a chain-of-thought step |

### Read Operations

| Method | Description |
|---|---|
| `get_agent_history(agent_id, limit, ...)` | Fetch full history for an agent (all event types) |
| `get_llm_call(call_id)` | Fetch a specific LLM call |
| `get_repl_execution(execution_id)` | Fetch a specific REPL execution |
| `search_llm_calls(agent_id, contains_prompt, contains_response, limit)` | Full-text search on prompts/responses |
| `get_agent_stats(agent_id)` | Aggregate stats (total calls, tokens, cost, etc.) |
| `get_all_agents()` | List all agent IDs with recorded history |

### Management Operations

| Method | Description |
|---|---|
| `clear_agent_history(agent_id)` | Delete all records for an agent |
| `vacuum()` | No-op (server-side maintenance in Supabase) |

### Write Semantics

All writes use **PostgREST upsert** via the `Prefer: resolution=merge-duplicates` header. This matches SQLite's `INSERT OR REPLACE` behavior — if a record with the same primary key already exists, it is merged/updated.

### Read Semantics

- All reads go through the PostgREST REST API
- Filtering uses PostgREST query parameters (e.g., `agent_id=eq.{value}`)
- Ordering uses `order=column.asc|desc`
- Aggregation (`get_agent_stats`) is done **client-side** in Python — PostgREST does not support complex SQL aggregation without stored procedures

### Thread Safety

All public methods acquire `self._lock` (a `threading.Lock`) before making API calls, ensuring thread-safe access.

### Graceful Degradation

If `enabled=False` (no credentials), all write/read operations become **no-ops** returning empty results. No exceptions are raised.

---

## Authentication

PostgREST uses the Supabase **anon key** as both `apikey` and `Authorization: Bearer` header. This is the public/client-side key — appropriate for a client-side storage library. The anon key has full read/write access to the `public` schema tables.

**Row Level Security (RLS)** is disabled on all tables (confirmed via Supabase advisor). This is acceptable for the current trust model where the anon key is used app-internally.

---

## Important Constraints

1. **No historical data migration**: The SQLite `.agent_loop.db` was not migrated. Tables were created fresh and are currently empty.
2. **Client-side aggregation**: `get_agent_stats()` fetches all rows and sums in Python rather than using SQL — performance considerations apply at scale.
3. **No real-time subscriptions**: This is a synchronous request/response store. For real-time updates, Supabase Realtime would need to be added separately.
4. **JSON serialization**: `llm_calls_made`, `code_blocks`, and `context` fields store JSON strings — serialized before POST, deserialized by client on GET.

---

## For Agents

When working on the RLM engine, import and instantiate the storage like so:

```python
from rlm.storage.agent_loop_storage import AgentLoopStorage

storage = AgentLoopStorage()  # reads SUPABASE_URL + SUPABASE_ANON_KEY from env
if storage.enabled:
    storage.save_llm_call({"call_id": "call-001", "agent_id": "agent-123", ...})
    history = storage.get_agent_history("agent-123")
```

The storage is typically instantiated once per agent session and reused for all read/write operations.

---

## Task Knowledge Layer

The **Task Knowledge Layer** stores task fingerprints and extracted knowledge for cross-task similarity search, enabling the RLM engine to learn from prior task executions.

**Module**: `rlm.storage.task_knowledge_storage`
**Class**: `TaskKnowledgeStorage`

### Table: `task_knowledge`

| Column | Type | Description |
|---|---|---|
| `id` | `text` PK | Unique record identifier |
| `task_id` | `text` | Task identifier |
| `task_type` | `text` | Task type label |
| `fingerprint` | `text` | MinHash fingerprint (64-char hex string) |
| `code_artifacts` | `text` | JSON array of code snippets or artifact references |
| `error_patterns` | `text` | JSON array of error patterns encountered |
| `summary` | `text` | Short summary of task outcome |
| `lessons` | `text` | Key lessons learned |
| `similar_tasks` | `text` | JSON array of similar task IDs |
| `timestamp` | `real` | Unix timestamp |

### TaskFingerprint Algorithm

Generates a MinHash-based similarity fingerprint for a task's code artifacts.

- **Algorithm**: MinHash (datasketch library)
- **Permutations**: 128
- **Shingling**: k-shingles with `k=3` (3-character substrings)
- **Output**: 64-character hexadecimal string
- **Steps**:
  1. Convert input text to character n-grams (k=3 shingles)
  2. Hash each shingle into a 64-bit integer
  3. Compute MinHash signature with 128 permutations
  4. Convert signature to 64-char hex string

### KnowledgeExtractor Process

Extracts structured knowledge from an agent loop iteration for storage in the task knowledge layer.

**8-Step Process**:
1. **code_artifacts** — Extract and serialize code blocks, file paths, and command outputs
2. **error_patterns** — Identify and categorize error types, messages, and stack traces
3. **summary** — Generate a brief natural-language summary of task outcome
4. **lessons** — Extract key lessons, patterns to avoid, and best practices learned
5. **task_type** — Classify the task type (e.g., `code_generation`, `debugging`, `refactoring`)
6. **fingerprint** — Compute MinHash fingerprint via TaskFingerprint algorithm
7. **similar_tasks** — Query existing fingerprints to find similar prior tasks
8. **save** — Persist the complete knowledge record to `task_knowledge` table
