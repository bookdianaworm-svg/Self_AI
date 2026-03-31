# Domain Routing Protocol (System Expansion)
**Version:** 1.0
**Purpose:** Defines how the Architect Agent classifies user tasks to dynamically mount domain-specific Layer 1 axioms and Research Agent sources.

## 1. Task Intake & Classification
When a new task is received, the `ArchitectAgent` executes a pre-processing step before breaking down sub-systems:
- **Input:** Raw user prompt.
- **Process:** Extract domain keywords (verbs, entities, constraints).
- **Output:** Domain assignment (`MATH`, `SOFTWARE`, `PHYSICS`, `CHEMISTRY`, `FINANCE`, `GENERAL`).

## 2. Dynamic Layer 1 Mounting
Based on the Domain assignment, the system generates a task-specific `layer1-bootstrap.lean` file. 
*Do not load all libraries globally.*

**Configuration Map:**
- `MATH`: `import Mathlib.All`
- `SOFTWARE`: `import Batteries`, `import Std`, `import Lean.Meta`
- `PHYSICS`: `import SciLean`, `import PhysLib`, `import Mathlib.Analysis`
- `CHEMISTRY`: `import ChemLean`, `import PhysLib.Thermodynamics`
- `FINANCE`: `import Mathlib.Probability`, `import Mathlib.MeasureTheory`

## 3. Dynamic Source Routing (Research Agent)
The `ResearchAgent` must restrict its API queries to domain-specific credible databases to prevent context pollution and hallucination.

**Source Map:**
- `MATH`: [arXiv:math, zbMATH, IACR]
- `SOFTWARE`: [ACM Digital Library, IEEE CS, arXiv:cs]
- `PHYSICS`: [NIST, IEEE Xplore, ASM]
- `CHEMISTRY`: [PubChem, ChemRxiv, Materials Project]
- `FINANCE`: [SSRN, NBER, arXiv:q-fin]

## 4. Execution Pseudocode for Agents
```python
# In agents/architect_agent.py

def determine_domain(self, task_description: str) -> str:
    """Uses LLM to map task to predefined domains based on keywords."""
    domain_keywords = {
        "SOFTWARE": ["algorithm", "code", "api", "software", "network"],
        "PHYSICS": ["design", "hardware", "heat", "force", "machine"],
        "FINANCE": ["market", "ledger", "price", "economy", "trade"]
    }
    # Logic: Score task against keywords, return highest matching domain.
    # Default to PHYSICS if hardware design, SOFTWARE if code.

def generate_layer1_bootstrap(self, domain: str):
    """Writes the Lean import statements dynamically."""
    imports = {
        "SOFTWARE": "import Batteries\nimport Std",
        "PHYSICS": "import SciLean\nimport PhysLib"
    }
    with open("layer1_bootstrap.lean", "w") as f:
        f.write(imports[domain])
        f.write("\nnamespace VerificationOracle\n...")
```

## 5. Fallback & Correction
If the `VerifierAgent` (Lean Kernel) fails 100% of proof attempts in the first pass, it signals a **Domain Mismatch**. The `ArchitectAgent` will re-classify the prompt to the second-highest scoring domain, mount the new Layer 1 libraries, and trigger the `ResearchAgent` to start over.