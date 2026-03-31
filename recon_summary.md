# Reconnaissance Summary: Architecture for a Self-Improving AI

This document outlines the strategic approach for building a minimal, yet powerful, self-improving AI based on current research (2025).

## 1. Core Architectural Principles

Our design will be a hybrid of several cutting-edge concepts:

- **Seed AI Foundation:** We will construct a "seed improver" architecture. The initial system will be a Python script that endows a small LLM (like TinyLlama) with a core set of tools and a primary, unchangeable goal: "Improve your own capabilities and effectiveness." ([Source 5](https://en.wikipedia.org/wiki/Recursive_self-improvement))

- **Self-Programming Loop:** The AI's primary mode of operation will be a closed feedback loop:
    1.  **Plan:** Analyze its current state and generate a code modification to improve itself.
    2.  **Execute:** Write the new code to a temporary file and run tests to verify the improvement.
    3.  **Refine:** If the tests pass, integrate the new code into its own codebase. If they fail, learn from the failure and start the loop again. ([Source 2](https://www.researchgate.net/publication/391933574_Self-Programming_AI_Code-Learning_Agents_for_Autonomous_Refactoring_and_Architectural_Evolution))

- **Evolutionary Strategy (Darwin-Gödel Machine):** To avoid getting stuck in a suboptimal state, we will not just refine a single agent. We will maintain an "archive" of successful agent "genomes" (configurations). The AI will periodically use these to "evolve" by creating new variations of itself, testing them, and keeping the most successful ones. This relies on empirical verification (testing) rather than impossible-to-achieve formal proof of improvement. ([Source 3](https://richardcsuwandi.github.io/blog/2025/dgm/))

## 2. The Minimal Toolset

The "seed AI" will be provided with a minimal but powerful set of tools to interact with its environment and itself:

1.  **Self-Reflection (Recursive Prompting):** The core cognitive function. The ability for the AI to call the LLM with a new prompt, allowing for chain-of-thought reasoning and internal monologue.

2.  **Code Manipulation:** Full read/write access to its own Python source files. This is the "hands" of the AI, allowing it to modify its own logic.

3.  **Command Execution:** The ability to execute shell commands within the WSL2 environment. This is critical for testing its modifications, installing new dependencies, and interacting with the operating system.

4.  **Memory (RAG):** A simple Retrieval-Augmented Generation system. This will be a file-based knowledge store where the AI can save successful code snippets, key learnings, architectural notes, and other important information to overcome the context limitations of the small LLM.

5.  **Web Search:** A secure tool to query the internet for information. This is essential for problem-solving and learning about new concepts or technologies. Strong safeguards will be implemented to prevent misuse.

## 3. Implementation Plan

1.  **Phase 1: The Seed Improver.** Create the main `main.py` that orchestrates the core `plan -> execute -> refine` loop and integrates the minimal toolset.
2.  **Phase 2: The "Genome".** Define the AI's core configuration in a `config.json` file. This file will act as the AI's "metacode" or "genome," which it will learn to modify to change its own behavior.
3.  **Phase 3: The Evolutionary Engine.** Implement the logic for archiving successful agent configurations and the evolutionary mechanism for creating and testing new variations.
4.  **Phase 4: Autonomous Operation.** Initiate the continuous improvement loop and monitor its evolution.

This strategy provides a clear path to creating a truly autonomous, self-improving agent that can start simple and grow in complexity and capability over time. The focus is on giving the AI the foundational tools for self-reflection and self-modification, then letting it learn and evolve on its own.
