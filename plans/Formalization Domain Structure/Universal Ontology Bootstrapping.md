# Universal Ontology Bootstrapping (Domain Zero)
**Version:** 1.0
**Purpose:** Defines the protocol for the swarm to handle entirely novel, open-ended tasks (APIs, games, unknown systems) without hardcoded libraries, while mathematically guaranteeing the AI's foundational reasoning is free of contradictions.

## 1. The "Naked Axiom" Ban
When operating outside of verified domains (Physics, Math, etc.), the AI is strictly prohibited from using the `axiom` keyword in Lean to invent rules. 
- **Why:** If the AI hallucinates `axiom A: True` and `axiom B: False`, the system becomes inconsistent, bypassing all safety checks (Principle of Explosion).
- **Exception:** Only the human user can inject naked axioms via the Layer 1.5 `<axioms>` override.

## 2. The Solution: Structures and The Genesis Proof
Instead of asserting rules as absolute truths, the `AutoformalizationAgent` must formalize the unknown domain as a Lean `structure` (an abstract universe) and provide an **Inhabitation Proof** (proving that a valid state can exist without contradiction).

### Phase 1: Ontology Generation
The AI reads the arbitrary task (e.g., "Figure out the Google Calendar API") and defines the "Types" and "Invariants" of that universe.

```lean
-- Example: AI formalizes a novel domain (Google Calendar)
structure CalEvent where
  startTime : Nat
  endTime : Nat
  -- The Invariant / Rule the AI deduced
  valid_time : startTime < endTime 
```

### Phase 2: The Genesis State Proof (The Hard Check)
Before the AI is allowed to plan architecture, write code, or execute API calls, the `VerifierAgent` forces the AI to construct a `GenesisState` (a valid starting point). 
If the AI's rules contain a logical fallacy or contradiction, the Lean Kernel will reject the Genesis State.

```lean
-- The AI must prove its rules are mathematically consistent by creating an instance
def GenesisEvent : CalEvent := {
  startTime := 0,
  endTime := 1,
  -- Lean kernel verifies 0 < 1. If the AI's rules were contradictory, 
  -- this proof would fail and the system would reject the AI's reasoning.
  valid_time := by norm_num 
}
```

## 3. Handling Arbitrary State Machines (e.g., Games, Simulators)
For tasks requiring complex state evolution (e.g., "Create a SimCity clone"), the AI must formalize a **State Transition Function** and prove that invariants are preserved across time.

**The Universal State Machine Protocol:**
1. **Define `State`:** What variables exist? (Population, Grid, Funds).
2. **Define `Invariants`:** What must always be true? (Funds ≥ 0).
3. **Define `NextState`:** How does the system change?
4. **Prove `InvariantPreservation`:** `theorem safe_step (s : State) : valid s → valid (NextState s)`

If the AI proposes a game mechanic that could result in negative funds, the Lean Kernel will reject the `safe_step` proof, forcing the AI to fix its game design logic before writing the application code.

## 4. Execution Workflow for the Swarm
When the `ArchitectAgent` encounters a task that does not match `PHYSICS`, `MATH`, `SOFTWARE`, etc., it routes to `DOMAIN_ZERO` (Universal Ontology):
1. `ResearchAgent` queries standard web/API docs or generic literature.
2. `AutoformalizationAgent` writes the Lean `structure` and invariants.
3. `AutoformalizationAgent` attempts to write the `GenesisState` proof.
4. `VerifierAgent` checks for consistency.
   - **If Failed:** The AI's understanding of the domain is logically flawed. Route back to `Autoformalization` to adjust the invariants.
   - **If Passed:** The ontology is certified. The AI may now proceed to execute the task (generate code, call APIs, etc.) using this structure as its rigid blueprint.