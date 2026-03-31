# Universal Dual-Loop Architecture (System 1 / System 2)
**Version:** 2.0
**Purpose:** Upgrades the RLM Swarm from a rigid, linear pipeline into an asynchronous, dual-loop engine. This maximizes LLM creativity and real-time user UX (System 1) while enforcing absolute mathematical correctness in the background (System 2).

## 1. Global Decoupling Principle
For *all* tasks—whether designing a food replicator, writing a React app, or reverse-engineering an API—generation and verification are strictly decoupled. 
- **Generation (System 1)** is permitted to be messy, probabilistic, heuristic, and fast.
- **Verification (System 2)** remains deterministic, axiomatic, and absolute.

## 2. Track A: The Fast Loop (Skunkworks & UX)
The user interacts exclusively with the Fast Loop. 
- **Agents Involved:** `ArchitectAgent`, `DraftsmanAgent`, `ResearchAgent`.
- **Behavior:** Operates like a standard autonomous AI. It writes draft code, queries the web, runs local Python scripts, and iterates rapidly.
- **UX Requirement:** All logs, thoughts, and trial-and-error executions must stream to the user interface in real-time. The user must see the "work being done."
- **The Output:** Once the Fast Loop completes a stable iteration, it packages the state into a `ReleaseCandidate (RC)` and places it in the Async Message Queue.

## 3. Track B: The Slow Loop (The Crucible)
The Slow Loop monitors the Async Message Queue. The user does not wait for this loop; it runs concurrently.
- **Agents Involved:** `AutoformalizationAgent`, `VerifierAgent` (Lean/Haskell).
- **Behavior:** Picks up the `ReleaseCandidate`. Extracts the core logic/design. Translates it into a formal `structure`. Defines the `GenesisState`. Compiles against the task's Layer 1 Axioms.
- **Output:** Returns a binary `PASS` or `FAIL` with a specific mathematical proof or error trace.

## 4. The Handoff & Interrupt Protocol
The two loops communicate via a strict interrupt protocol:
1. **While Pending:** The Fast Loop can move on to the next phase of the project while the Slow Loop checks the previous phase.
2. **On Pass:** The Slow Loop tags the RC as `CERTIFIED`. The Fast Loop silently integrates this as a frozen foundation.
3. **On Fail (The Bounce-Back):** The Slow Loop issues a high-priority interrupt to the Fast Loop. 
   - It translates the Lean kernel error (e.g., `Type Mismatch: Voltage expected, got Null`) into plain text.
   - The Fast Loop pauses, acknowledges the constraint failure to the user, and re-factors the RC to satisfy the newly discovered mathematical boundary.

## 5. End-of-Task Constraint
A task can never be marked `100% COMPLETE` or presented to the user as a final, deployable artifact until all associated Release Candidates have passed the Slow Loop (Track B) and received a `CERTIFIED` tag. The user may play with unverified Skunkworks drafts, but the final RLM stamp of approval requires mathematical absolute truth.