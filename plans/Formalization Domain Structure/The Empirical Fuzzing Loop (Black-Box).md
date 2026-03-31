# The Empirical Fuzzing Loop (Black-Box Discovery)
**Version:** 1.0
**Purpose:** Defines the strict algorithmic constraints for the swarm when interacting with undocumented APIs, hardware, or unknown binaries in the `CYBER_SEC` or `DOMAIN_ZERO` edge cases.

## 1. The Ban on Random Fuzzing
Agents are strictly prohibited from writing unstructured "while-true" fuzzing scripts. All black-box protocol discovery must be executed using Automata Learning (Angluin's L* algorithm) to prevent infinite loops and state explosion.

## 2. Sandbox Architecture (The "Teacher")
The target system (binary or hardware API) must be isolated within a `Modal` or `DockerREPL` environment.
- **Network:** Air-gapped (No external internet access).
- **Timeouts:** Hard cap of 300 seconds per fuzzing iteration.
- **Observability:** The Sandbox must return strictly typed responses: `VALID_TRANSITION`, `REJECTED`, `TIMEOUT`, or `CRASH`.

## 3. The Discovery Workflow (The "Learner")
The `AutoformalizationAgent` and a dedicated `ProbingAgent` work in a loop to extract the Finite State Machine (FSM):

1. **Input Space Definition:** The AI defines the bounds of the test (e.g., "I will test hex bytes 0x00 through 0xFF").
2. **Membership Queries:** The `ProbingAgent` sends sequences of inputs to the Sandbox. It records which sequences result in a new valid state vs. a crash.
3. **Hypothesis Generation:** The `AutoformalizationAgent` constructs a proposed FSM in Haskell.
4. **Equivalence Fuzzing:** The `ProbingAgent` generates 1,000 random sequences based on the *proposed FSM* to try and break it. 
5. **Refinement:** If a sequence breaks the hypothesis, the FSM is updated. If it holds, the FSM is considered "Discovered."

## 4. Haskell FSM Synthesis
Once the protocol is discovered empirically, it must be translated into purely functional Haskell Algebraic Data Types (ADTs). This ensures that the generated driver cannot physically represent an invalid state.

```haskell
-- Example: Discovered Undocumented IoT Protocol
data IoTState = Disconnected | Handshake | Authenticated | ErrorState

data IoTCommand = SendSYN | SendAuthKey | RequestData | Terminate

-- The Discovered State Transition Function
-- The AI empirically learned that asking for data before authentication causes a crash,
-- so the Haskell type system enforces that transition to an ErrorState.
transition :: IoTState -> IoTCommand -> IoTState
transition Disconnected SendSYN = Handshake
transition Handshake SendAuthKey = Authenticated
transition Handshake RequestData = ErrorState -- Discovered constraint
transition Authenticated RequestData = Authenticated
transition _ Terminate = Disconnected
```

## 5. Bounded Verification in Lean
Because empirical data is never 100% mathematically certain (we only tested a bounded number of states), the `VerifierAgent` requires a **Bounded Proof**. 
The AI must prove in Lean that *within the discovered state machine*, an unsafe state (like a buffer overflow or unauthorized access) is categorically unreachable from the Genesis State.