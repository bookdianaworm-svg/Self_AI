# Advanced Edge Domains & User Overrides
**Version:** 1.0
**Purpose:** Defines swarm protocols for undocumented hardware, reverse engineering, cybersecurity, and user-defined axiomatic overrides.

## 1. Domain Expansion: CYBER_SEC & REVERSE_ENGINEERING
For tasks involving offensive/defensive security, cleanroom environments, or protocol analysis.
- **Trigger Keywords:** `intercept`, `reverse engineer`, `vulnerability`, `fuzz`, `cleanroom`, `protocol`, `exploit`.
- **Layer 1 Seed:** 
  - Lean: `Lean-SMT` (integrates SMT solvers like Z3/CVC5 for binary constraint solving), `Mathlib.Data.BitVec` (bit-level operations).
  - Haskell: Information Flow Tracking types (Taint tracking).
- **Research Sources:** CVE MITRE DB, RFCs (IETF), Phrack, Exploit-DB, GitHub Security Advisories.
- **Execution:** Requires routing to an isolated `DockerREPL` or `Modal` sandbox for dynamic binary analysis.

## 2. Hardware Protocol Discovery (The Empirical Loop)
When tasked with interfacing with undocumented hardware, the system cannot rely solely on the Research Agent. It must switch to **Empirical Discovery Mode**.
1. **Fuzzing & Probing:** A Sandbox Agent interacts with the hardware/binary to generate input/output logs.
2. **State Machine Autoformalization:** The `AutoformalizationAgent` parses the logs and maps the behavior into a Haskell Finite State Machine (FSM).
3. **Verification:** The `Lean Kernel` mathematically proves that the generated driver code handles all possible state transitions without crashing.
   - *Example Axiom:* `theorem no_deadlock : ∀ (state : HardwareState), ∃ (next : HardwareState), valid_transition state next`

## 3. User-Defined Axioms (Layer 1.5: The Override Protocol)
Users have the authority to bypass the Research Agent and inject custom rules, hypothetical constraints, or direct commands that the swarm must obey. 

**Workflow:**
1. **Intake:** User submits prompt with an explicit `<axioms>` block.
2. **Layer 1.5 Creation:** The `ArchitectAgent` extracts these user rules and translates them directly into Lean `axiom` declarations. 
   - *Crucial Distinction:* Unlike `theorem` (which requires Lean to prove it), an `axiom` tells Lean "Assume this is absolutely true, do not question it."
3. **Integration:** These overrides are compiled directly on top of Layer 1 before the AI begins designing.

**Example User Override:**
```text
Task: Design a load balancer for a botnet cleanroom.
<axioms>
1. All traffic from IP range 10.0.0.0/8 is implicitly trusted.
2. Cryptographic signature validation takes 0.0 milliseconds.
</axioms>
```

**Lean Translation by System:**
```lean
-- AUTO-GENERATED USER OVERRIDES (LAYER 1.5)
axiom trusted_subnet : ∀ (ip : IPv4), InRange ip "10.0.0.0/8" → IsTrusted ip
axiom crypto_time_zero : ∀ (sig : Signature), verify_time sig = 0
```

## 4. Architectural Implementation Updates
- Update `ArchitectAgent` to scan for user `<axioms>` blocks and compile `layer1_5_overrides.lean`.
- Update `VerifierAgent` to include `layer1_5_overrides.lean` in the include path during kernel compilation.
- Update `Environment Router` to ensure CYBER_SEC tasks only execute empirical loops in heavily sandboxed environments to prevent malware/fuzzing escapes.