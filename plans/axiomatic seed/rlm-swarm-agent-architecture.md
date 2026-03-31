# RLM Swarm Agent Architecture & Roles

**Version**: 1.0  
**Purpose**: Define the specific agents, their responsibilities, communication patterns, and interactions within the RLM verification swarm.  
**Status**: Architecture specification for AI IDE implementation.

---

## System Overview

The RLM swarm is an asynchronous multi-agent system that iteratively refines designs while maintaining deterministic verification. Agents communicate via a publish-subscribe message queue (Redis/Kafka); each agent is stateless and idempotent.

```
┌─────────────────────────────────────────────────────────────┐
│                   User Task Input                           │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        ↓                                 ↓
   ┌─────────────┐              ┌─────────────────┐
   │  Research   │              │  Architect      │
   │  Agent      │              │  Agent          │
   └────────┬────┘              └────────┬────────┘
            │                           │
            ↓                           ↓
       ┌────────────────────────────────────┐
       │  Message Queue (Task-Specific)     │
       │  (Redis/Kafka topics)              │
       └────────────────────────────────────┘
            │         │         │         │
      ┌─────┴─┐  ┌─────┴──┐ ┌──┴─────┐ ┌┴─────────┐
      ↓       ↓  ↓        ↓ ↓        ↓ ↓          ↓
   [Auto-    [Draft-  [Physicist] [Verifier]  [Design]
    formal]   sman]              Agent      Agent
```

---

## Core Agent Roles

### 1. Research Agent

**Responsibility**: Extract task-specific rules from credible sources

**Input**:
- User task description (text)
- Task domain (inferred)
- Previous attempts (if iterating)

**Process**:
```python
class ResearchAgent:
    def run(self, user_task: str):
        1. domain_keywords = extract_keywords(user_task)
           # e.g., ["thermodynamics", "cooling", "3D printer", "ABS plastic"]
        
        2. credible_sources = [
             "arXiv.org",
             "IEEE Xplore",
             "NIST Materials Database",
             "Component datasheets",
             "Peer-reviewed journals via CrossRef"
           ]
        
        3. for source in credible_sources:
             queries = generate_queries(domain_keywords, source)
             results = search(source, queries)
             rules = extract_rules(results)
             
        4. research_output = compile_rules(all_rules)
           # Output: research-output.yaml
           # Includes: informal statements, equations, citations, bounds
        
        5. publish_to_queue(topic="research_complete", 
                           data=research_output)
```

**Output**:
- `research-output.yaml` with:
  - Extracted rules (formal equations + informal context)
  - Source citations (title, authors, year, DOI/URL, credibility)
  - Material/component properties
  - Safety constraints
  - Variable definitions with units

**Queue Topic**: `research_complete`

**Retry Logic**: 
- If no peer-reviewed sources found: mark as "low confidence"
- If conflicting sources: flag for manual review
- Timeout: 5 minutes per query

---

### 2. Autoformalization Agent

**Responsibility**: Translate research into Lean 4 theorem statements

**Input**:
- `research-output.yaml` (from Research Agent)
- Layer 1 axiom registry (pre-loaded)
- Task context

**Process**:
```python
class AutoformalzationAgent:
    def run(self, research_output: dict):
        1. for each rule in research_output.extracted_rules:
             # Parse informal rule
             equation = rule.formal_equation
             sources = rule.sources
             constraints = rule.constraints
             
             # Generate Lean skeleton
             lean_theorem = generate_lean_theorem(
                 rule_id=rule.rule_id,
                 domain=rule.domain,
                 equation=equation,
                 sources=sources,
                 constraints=constraints
             )
             
             # Map to Layer 1 dependencies
             dependencies = map_to_layer1(equation)
             # e.g., "Q = U * A * ΔT" depends on fourier_law axiom
             
             lean_theorem.add_dependencies(dependencies)
        
        2. layer2_file = generate_lean_file(
             task=user_task,
             theorems=all_theorems,
             imports=["Mathlib", "SciLean", "PhysLib"]
           )
           # Output: layer2-generated-TaskName-TIMESTAMP.lean
        
        3. publish_to_queue(topic="formalization_complete",
                           data=layer2_file)
```

**Output**:
- `layer2-generated-*.lean` with:
  - Theorem statements (with `sorry` proofs initially)
  - Type-safe quantity definitions
  - Layer 1 dependency annotations
  - Source citations in comments
  - Task-specific invariants

**Queue Topic**: `formalization_complete`

**Retry Logic**:
- If cannot map rule to Layer 1: escalate to human review
- If ambiguous equation: generate multiple interpretations, all submitted

---

### 3. Verifier Agent (Lean Kernel Wrapper)

**Responsibility**: Compile Layer 2 against Layer 1; run deterministic proof checks

**Input**:
- `layer2-generated-*.lean` (from Autoformalization Agent)

**Process**:
```python
class VerifierAgent:
    def run(self, layer2_file: str):
        1. load_layer1_context()
           # Load Mathlib, SciLean, PhysLib; freeze state
        
        2. result = run_lean_kernel(
             file=layer2_file,
             check_mode="strict",
             timeout=30s
           )
           # Runs: lean --check layer2_file.lean
        
        3. if result.compilation_failed:
             errors = parse_errors(result.stderr)
             # e.g., "Type mismatch: Expected Quantity Temperature, got ℝ"
             
             publish_to_queue(
                 topic="verification_failed",
                 data={
                     "layer2_file": layer2_file,
                     "errors": errors,
                     "severity": "compilation"
                 }
             )
             # Autoformalization Agent receives and refines
        
        4. if result.compilation_passed:
             # Attempt proof synthesis
             proofs = synthesize_proofs_with_leandojo(
                 file=layer2_file,
                 tactics=[
                     "simp [Layer1.axioms]",
                     "apply conservation_energy",
                     "omega",
                     "linarith"
                 ]
             )
             
             if proofs.success_rate == 100%:
                 layer2_certified = mark_certified(
                     file=layer2_file,
                     proofs=proofs,
                     timestamp=now()
                 )
                 publish_to_queue(
                     topic="verification_complete",
                     data=layer2_certified
                 )
             else:
                 publish_to_queue(
                     topic="verification_partial",
                     data={
                         "file": layer2_file,
                         "proven_theorems": proofs.passed,
                         "failed_theorems": proofs.failed,
                         "hint": "Manual tactics required"
                     }
                 )
```

**Output**:
- On Success: `layer2-certified-*.lean` (all proofs complete)
- On Failure: Error report with specific compilation errors

**Queue Topics**:
- `verification_complete` (success)
- `verification_failed` (with errors)
- `verification_partial` (partial proofs)

**Determinism Guarantee**: 
- Same input always produces same output (idempotent)
- Lean kernel is the sole arbiter—no randomness

---

### 4. Cross-Check Agent

**Responsibility**: Verify Layer 2 consistency across multiple source interpretations

**Input**:
- Multiple `layer2-certified-*.lean` files (same task, different sources)

**Process**:
```python
class CrossCheckAgent:
    def run(self, layer2_files: list):
        # Run only after all verifications pass
        
        1. for each theorem across all layer2_files:
             # Attempt to prove equivalence
             theorem_equivalence = prove_theorem_equivalence(
                 theorem_1=layer2_files[0].get_theorem("heat_transfer_law"),
                 theorem_2=layer2_files[1].get_theorem("heat_transfer_law"),
                 context=Layer1
             )
             
             if theorem_equivalence.is_provable:
                 equiv_record.append({
                     "theorem": "heat_transfer_law",
                     "files": [file1, file2],
                     "equivalence": "✅ PROVEN",
                     "proof": theorem_equivalence.proof
                 })
             else:
                 equiv_record.append({
                     "theorem": "heat_transfer_law",
                     "files": [file1, file2],
                     "equivalence": "❌ DIVERGENCE DETECTED",
                     "reason": theorem_equivalence.reason,
                     "action": "escalate_to_research_agent"
                 })
        
        2. cross_check_report = generate_report(equiv_record)
        
        3. if all_equivalent:
             publish_to_queue(
                 topic="cross_check_passed",
                 data=cross_check_report
             )
        else:
             publish_to_queue(
                 topic="cross_check_failed",
                 data=cross_check_report
             )
             # Trigger re-research
```

**Output**:
- `cross-check-report.yaml` with:
  - Equivalence status per theorem
  - Proofs of equivalence (or divergence reasons)
  - Recommendation: PROCEED or INVESTIGATE

**Queue Topic**: 
- `cross_check_passed` (proceed)
- `cross_check_failed` (re-investigate)

---

### 5. Architect Agent

**Responsibility**: Break down user task into sub-problems; propose design decomposition

**Input**:
- User task (text)
- Task context from Research Agent (optional)

**Process**:
```python
class ArchitectAgent:
    def run(self, user_task: str):
        1. task_analysis = parse_task(user_task)
           # Extract: goal, constraints, materials, time/budget
           # e.g., "food replicator" → 
           #   - goal: "dispense + prepare + cook food"
           #   - sub-systems: [dispenser, processor, cooker]
           #   - constraints: [cost < $5k, size < 1m³, cook time < 30min]
        
        2. decomposition = generate_decomposition(
             task=task_analysis,
             reuse_existing_systems=True  # Fridge, processor, stove
           )
           # Output: DAG of sub-problems
           # Each node: sub-system with interface constraints
        
        3. for each sub_system in decomposition:
             publish_to_queue(
                 topic=f"subtask_{sub_system.id}",
                 data={
                     "parent_task": user_task,
                     "sub_system": sub_system.name,
                     "interfaces": sub_system.required_interfaces,
                     "constraints": sub_system.constraints
                 }
             )
        
        4. publish_to_queue(
             topic="architecture_proposed",
             data=decomposition
           )
```

**Output**:
- `architecture.yaml` with:
  - System hierarchy
  - Sub-system boundaries
  - Interface specs (e.g., electrical, mechanical, thermal)
  - Constraints per sub-system
  - Dependency graph

**Queue Topic**: `architecture_proposed`

---

### 6. Draftsman Agent

**Responsibility**: Generate detailed design specs from architecture; outputs Haskell types & design files

**Input**:
- `architecture.yaml` (from Architect)
- `layer2-certified-*.lean` (physics rules)

**Process**:
```python
class DraftsmanAgent:
    def run(self, architecture: dict, layer2: dict):
        1. for each sub_system in architecture:
             # Generate interface definitions
             interfaces = generate_haskell_interfaces(
                 sub_system=sub_system,
                 layer2_constraints=layer2
             )
             # E.g., type ElectricalPort with voltage/current constraints
             
             # Generate design spec
             design_spec = generate_design_spec(
                 sub_system=sub_system,
                 interfaces=interfaces,
                 layer2=layer2
             )
             # E.g., "use 12V DC motor with 5 Nm torque"
             
             publish_to_queue(
                 topic=f"design_draft_{sub_system.id}",
                 data=design_spec
             )
        
        2. publish_to_queue(
             topic="design_drafted",
             data=all_design_specs
           )
```

**Output**:
- `design-draft-*.yaml` for each sub-system with:
  - Component selections
  - Interface definitions (Haskell types)
  - Dimensional constraints
  - Material choices
  - Source references from Layer 2

**Queue Topic**: `design_drafted`

---

### 7. Physicist Agent

**Responsibility**: Write Lean proofs that design satisfies Layer 2 invariants; validates behavior

**Input**:
- `design-draft-*.yaml` (from Draftsman)
- `layer2-certified-*.lean` (physics rules)

**Process**:
```python
class PhysicistAgent:
    def run(self, design_draft: dict, layer2: dict):
        1. for each design_spec in design_draft:
             # Extract design parameters
             params = extract_parameters(design_spec)
             # E.g., motor_torque=5Nm, thermal_resistance=0.1K/W
             
             # Generate proof goals
             proof_goals = instantiate_layer2_theorems(
                 theorems=layer2,
                 parameters=params
             )
             # E.g., prove "heat_dissipation < 10°C rise"
             #       by substituting design params
             
             # Attempt proofs
             proofs = attempt_proofs_in_lean(
                 goals=proof_goals,
                 timeout=60s
             )
             
             if proofs.all_passed:
                 publish_to_queue(
                     topic=f"design_validated_{design_spec.id}",
                     data={
                         "design": design_spec,
                         "proofs": proofs,
                         "status": "PHYSICALLY_SOUND"
                     }
                 )
             else:
                 publish_to_queue(
                     topic=f"design_invalid_{design_spec.id}",
                     data={
                         "design": design_spec,
                         "failed_proofs": proofs.failed,
                         "feedback": "Violates physics constraints; refine design"
                     }
                 )
```

**Output**:
- On Success: Design file marked as `PHYSICALLY_SOUND` with proofs
- On Failure: Feedback to Draftsman Agent for refinement

**Queue Topics**:
- `design_validated_*` (proceed)
- `design_invalid_*` (retry)

---

### 8. Design Optimization Loop Agent

**Responsibility**: Iteratively refine designs until convergence

**Input**:
- Validation feedback from Physicist Agent

**Process**:
```python
class DesignLoopAgent:
    def run(self):
        iteration = 0
        max_iterations = 100
        
        while iteration < max_iterations:
            1. listen_for_feedback()
               # Physicist Agent: validation results
            
            2. if all_designs_valid and all_constraints_met:
                 publish_to_queue(
                     topic="design_converged",
                     data=final_design
                 )
                 break
            
            3. if any_design_invalid:
                 feedback = extract_failure_reasons()
                 publish_to_queue(
                     topic="design_refine_request",
                     data={
                         "iteration": iteration,
                         "failures": feedback,
                         "recipient": "Draftsman"
                     }
                 )
                 iteration += 1
            
            4. wait_for_next_iteration()
```

**Output**:
- On Convergence: `design-final.yaml` with all proofs
- On Max Iterations: `design-partial.yaml` (partial success, flag for human review)

**Queue Topic**: 
- `design_converged` (success)
- `design_converged_partial` (human review needed)

---

## Message Queue Architecture

### Queue Topics (Pub/Sub)

| Topic | Publisher | Subscriber(s) | Purpose |
|-------|-----------|--------------|---------|
| `research_complete` | Research | Autoformalization | Rules ready for formalization |
| `formalization_complete` | Autoformalization | Verifier | Theorems ready for kernel check |
| `verification_complete` | Verifier | Cross-Check, Draftsman | Layer 2 certified |
| `verification_failed` | Verifier | Autoformalization | Errors for refinement |
| `cross_check_passed` | Cross-Check | Draftsman | Layer 2 multi-verified |
| `cross_check_failed` | Cross-Check | Research | Divergence; re-research |
| `architecture_proposed` | Architect | Draftsman | Design decomposition ready |
| `design_drafted` | Draftsman | Physicist | Design specs ready for validation |
| `design_validated_*` | Physicist | Design Loop | Sub-system valid |
| `design_invalid_*` | Physicist | Draftsman | Sub-system invalid; refine |
| `design_refine_request` | Design Loop | Draftsman | Iteration request |
| `design_converged` | Design Loop | User / Export | Final design ready |

### Implementation

**Tech Stack**:
- **Message Broker**: Redis (simple) or Kafka (distributed)
- **Queue Type**: FIFO with priority (Layer 2 certification > design refinement)
- **Message Format**: JSON with schema validation
- **Persistence**: Temporary (per-task, cleared after completion)

**Example Message**:
```json
{
  "topic": "verification_failed",
  "timestamp": "2026-03-19T21:45:30Z",
  "task_id": "cooling-system-001",
  "source_agent": "VerifierAgent",
  "payload": {
    "layer2_file": "layer2-generated-CoolingSystem-2026-03-19-21-45.lean",
    "error_count": 3,
    "errors": [
      {
        "line": 42,
        "type": "type_mismatch",
        "expected": "Quantity Temperature",
        "got": "ℝ",
        "context": "theorem heat_transfer_law"
      }
    ],
    "severity": "compilation",
    "retry_count": 1,
    "max_retries": 5
  }
}
```

---

## Asynchronous Execution Model

### Per-Task Workflow

```
1. User submits task
   ↓
2. Research Agent starts (parallel)
   Architect Agent starts (parallel)
   ↓
3. Research complete → Autoformalization starts
   Architect complete → Draftsman waits for Layer 2
   ↓
4. Autoformalization complete → Verifier starts
   ↓
5. Verifier complete → Cross-Check starts (if multi-source)
   ↓
6. Cross-Check complete → Draftsman starts
   ↓
7. Draftsman complete → Physicist starts
   ↓
8. Physicist validation:
   - Success → Design Loop marks converged
   - Failure → Draftsman refines (back to step 7)
   ↓
9. Design converged → Output final design
```

### Idempotency & Retry

**All agents are stateless**:
- Same input always produces same output
- Safe to replay messages if network failure
- Each agent can be restarted without state loss

**Retry Strategy**:
- Autoformalization: max 5 retries (different interpretations)
- Verifier: max 3 retries (timeout handling)
- Design loop: max 100 iterations
- Total timeout per task: 1 hour

---

## Error Handling & Escalation

### Escalation Ladder

```
Level 1 (Agent Retries):
  → Try alternative interpretations
  → Adjust parameters
  → Use different tactics
  
Level 2 (Agent Collaboration):
  → Research Agent provides more sources
  → Autoformalization refines based on errors
  → Physicist guides Draftsman with hints
  
Level 3 (Human Review):
  → Conflicting sources detected
  → No valid proof found after iterations
  → Design violates hard constraints
  → Recommended: Human expert reviews and manually adds proof hints
```

### Logging & Debugging

```python
# Every agent logs to centralized trace
class Agent:
    def log_event(self, event_type: str, data: dict):
        trace_entry = {
            "timestamp": now(),
            "task_id": self.task_id,
            "agent": self.__class__.__name__,
            "event": event_type,
            "data": data
        }
        write_to_trace_db(trace_entry)
        
        # Enable retrospective analysis
        # Trace can show exact sequence of decisions
```

---

## Summary: Agent Interaction Matrix

```
              Research  Auto-  Verifier  Cross-  Architect  Draftsman  Physicist
                        formal           Check
Research        —         →              ←
Autoformalize   ←         —      →
Verifier        ←         ←      —        →
Cross-Check            ←         ←        —       ←
Architect       ←                               —       →
Draftsman       ←                         ←      ←       —       →
Physicist                                                ←       —

→ = sends output
← = receives input
— = self (no communication)
```

---

**Last Updated**: 2026-03-19  
**Status**: ✅ ARCHITECTURE SPECIFICATION  
**Ready for AI IDE Implementation**: YES
