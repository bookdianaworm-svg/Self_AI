# Planning Conventions

This document establishes the rules for creating and managing plans in the Self_AI project.

---

## 1. Plan File Location Rule (CRITICAL)

**ALL plans MUST be saved to the `.kilo\plans\` directory.**

```
Correct:   .kilo\plans\<timestamp>-<descriptive-name>.md
INCORRECT: plans\<name>.md
```

### Why This Matters

- Plans in `.kilo\plans\` are tracked by the agent system
- Plans in `plans/` are NOT automatically recognized by the planning agent
- This has caused plans to be lost or misplaced in the past

### Plan Naming Convention

Plans should follow this naming format:
```
<timestamp>-<descriptive-name>.md
```

Example:
```
1774673361830-type-checking-system.md
20260328-swarm-implementation.md
```

---

## 2. Plan Creation Workflow

When creating a plan:

1. **Create the plan file** in `.kilo\plans\<timestamp>-<name>.md`
2. **Include metadata header** with:
   - Version
   - Date
   - Status
   - Dependencies
3. **Make it actionable** - include specific tasks, timelines, file manifests
4. **Link to related plans** when applicable

### Plan Metadata Template

```markdown
# <Plan Title>

**Version:** 1.0  
**Date:** YYYY-MM-DD  
**Status:** Draft | Ready for Integration | In Progress | Complete  
**Dependency:** <related plans or phases>

---

## Overview
...
```

---

## 3. Plan Categories

| Category | Location | Description |
|----------|----------|-------------|
| Agent Plans | `.kilo\plans\` | Plans created by planning agent |
| Implementation Plans | `plans/` | Project documentation, specs, roadmaps |

**Key distinction**: Plans created during agent planning sessions go to `.kilo\plans\`. Long-term project documentation goes to `plans/`.

---

## 4. Common Mistakes to Avoid

| Mistake | Problem | Solution |
|---------|---------|----------|
| Saving plan to `plans/` | Agent can't find it later | Always use `.kilo\plans\` |
| Generic filenames | Hard to identify | Use descriptive names with timestamps |
| Losing track of status | Unclear what's done | Update status field regularly |
| No file manifest | Unclear what to create | Always list new/modified files |

---

## 5. Plan Integration Checklist

Before considering a plan complete:

- [ ] File saved to `.kilo\plans\`
- [ ] Metadata header included (version, date, status)
- [ ] File manifest listed (new and modified files)
- [ ] Dependencies identified
- [ ] Success criteria defined
- [ ] Timeline/scope defined

---

## 6. Related Documents

- `AGENTS.md` - General agent guidelines
- `.kilo\agent-manager.json` - Session management
- `plans/` - Long-term project documentation
