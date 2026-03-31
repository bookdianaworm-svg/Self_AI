# The Skunkworks Protocol (Decoupling Discovery from Verification)
**Version:** 1.0
**Purpose:** Ensures the RLM Swarm retains its open-ended, creative, heuristic problem-solving capabilities (the "magic" of LLMs) without sacrificing the deterministic safety of the Lean/Haskell verification layer.

## 1. The Dual-Hemisphere Architecture
To handle open-ended tasks where the starting point is unknown (e.g., reverse engineering proprietary hardware), the system workflow is split into two distinct phases:
1. **The Skunkworks (Context of Discovery):** Unbounded, heuristic, messy exploration.
2. **The Crucible (Context of Justification):** Formal, deterministic, axiomatic verification.

## 2. Phase 1: The Skunkworks Loop
When a task lacks formal documentation or a clear starting point, the `ArchitectAgent` routes the task to a `SkunkworksEnvironment` (an isolated, internet-enabled Docker/Modal container).
- **No Axiomatic Constraints Here:** In this phase, the swarm is allowed to write unverified Python, run heuristic fuzzers, scrape obscure forums, guess-and-check, and recursively iterate thousands of times.
- **User Collaboration:** The swarm is encouraged to ask the user clarifying questions or request manual intervention (e.g., "Can you plug in the USB and tell me if the green light blinks?").
- **Goal:** The objective of the Skunkworks is strictly to arrive at a "High-Confidence Hypothesis" (e.g., "We believe the device uses this specific API protocol").

## 3. Phase 2: The Crucible (The Axiomatic Bottleneck)
The swarm is strictly prohibited from presenting Skunkworks output as the *final* deliverable. The chaotic discovery must pass through the formal verification bottleneck.
- **Translation:** The `AutoformalizationAgent` takes the Skunkworks hypothesis and translates it into Formal Structures (e.g., Haskell Algebraic Data Types, Lean theorems).
- **Verification:** The `VerifierAgent` (Lean Kernel) attempts to prove that the hypothesis is logically consistent and mathematically safe (The Genesis Proof).
- **The Rejection Loop:** If the proof fails, the specific mathematical contradiction is passed back into the Skunkworks. The swarm uses this hard constraint to guide its next round of chaotic exploration.

## 4. Why We Decouple
The Lean/Haskell verification layer does not care *how* a hypothesis was generated—whether through a rigorous algorithm, an intuitive LLM hallucination, or a lucky guess. It only cares that the resulting hypothesis can be proven true. By decoupling the two, we allow infinite AI creativity bounded by absolute mathematical safety.