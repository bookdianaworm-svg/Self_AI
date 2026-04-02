# Self_AI — Bootstrap Prompt

## First-Run Initialization

On first session start, before any other work:

1. **Index the codebase** using `codebase-memory-mcp`'s `index_project` tool:
   ```
   Tool: codebase-memory-mcp index_project
   ```

2. **Get architecture overview** using `get_architecture`:
   ```
   Tool: codebase-memory-mcp get_architecture
   Parameters: {recursive: true}
   ```

3. **Query memory-graph** for prior architectural context:
   ```
   Tool: memory-graph retrieve_memories
   ```

4. **Verify cocode MCP is reachable** by running a test semantic search for a central concept:
   ```
   Tool: cocode semantic_search
   Parameters: {query: "RLM engine execution flow", top_k: 3}
   ```

## Project Stack

- **Backend**: Python (FastAPI/RLM engine) + PostgreSQL
- **Frontend**: Next.js (UI) with TypeScript
- **Memory**: codebase-memory-mcp (knowledge graph) + memory-graph (persistent decisions) + cocode (semantic RAG)
- **CLI**: Claude Code with MCP servers (codebase-memory-mcp, memory-graph, repomix, cocode)

## Critical Rules

1. **Type safety**: All Python code must pass mypy; all TS/TSX must pass `tsc --noEmit`
2. **Hooks active**: Pre-edit checks warn on sensitive files; post-edit runs typecheck/lint
3. **Tool routing**: Code discovery → `codebase-memory-mcp` graph tools > cocode semantic search > grep > shell
4. **Memory**: Use memory-graph for cross-session architectural decisions; use cocode for natural-language code search
