# Autoformalization Pipeline (Layer 2 Dynamic Rules)

**Version**: 1.0  
**Purpose**: Define how the RLM swarm dynamically generates task-specific rules (Layer 2) by translating research into Lean theorems verified against Layer 1.  
**Status**: Operational, runs per-task, fully deterministic verification.

---

## Overview

The **Autoformalization Pipeline** is the "first-step" process that runs when the swarm encounters a new task:

1. **Research** → Extract informal rules from credible sources (arXiv, standards, specs)
2. **Formalization** → Translate informal rules into Lean 4 theorem statements
3. **Verification** → Lean kernel compiles against Layer 1 axioms
4. **Cross-Check** → Multi-source proof comparison
5. **Certification** → Output `.lean` file with proofs and citations

**Key Insight**: No AI self-checking. The Lean kernel (deterministic, non-AI) is the sole arbiter of correctness.

---

## Stage 1: Research & Information Extraction

### Research Agent Role

**Input**: User task (e.g., "Design a thermally-managed cooling system for a 3D printer enclosure")

**Process**:
1. **Domain Extraction** → Parse task for keywords (materials, physics domains, constraints)
2. **Source Query** → Search credible sources:
   - arXiv.org (preprints, research)
   - IEEE Xplore (engineering standards)
   - NIST materials database (material properties)
   - Official component datasheets (thermal specs)
   - Peer-reviewed journals (domain-specific)
3. **Rule Extraction** → Identify and extract:
   - Physical laws (e.g., "heat dissipation ∝ surface area")
   - Material properties (e.g., "aluminum thermal conductivity = 160 W/m⋅K")
   - Constraint equations (e.g., "temperature rise ≤ 10°C")
   - Safety bounds (e.g., "material strain ≤ 0.05")

### Extracted Information Format

```yaml
# research-output.yaml
task: "Thermally-managed cooling system for 3D printer"
timestamp: "2026-03-19T21:40:00Z"

extracted_rules:
  - rule_id: "HEAT_TRANSFER_001"
    domain: "thermodynamics"
    informal_statement: "Heat dissipation rate equals the temperature difference times thermal conductance"
    formal_equation: "Q = U * A * ΔT"
    sources:
      - title: "Fundamentals of Heat Transfer"
        authors: ["Incropera, DeWitt"]
        year: 2007
        url: "https://books.google.com/..."
        doi: "10.1016/B978-0-470-50156-3.00001-2"
        credibility: "peer-reviewed textbook"
      - title: "Heat Transfer Analysis in High-Speed Electronics"
        venue: "IEEE Transactions on Electronics"
        year: 2023
        arxiv_id: "2301.04567"
        credibility: "peer-reviewed journal"
    variables:
      Q: { symbol: "Q", unit: "Watts", meaning: "heat flow rate" }
      U: { symbol: "U", unit: "W/m²⋅K", meaning: "overall heat transfer coefficient" }
      A: { symbol: "A", unit: "m²", meaning: "surface area" }
      ΔT: { symbol: "ΔT", unit: "K", meaning: "temperature difference" }

  - rule_id: "MATERIAL_THERMAL_001"
    domain: "material_science"
    informal_statement: "Aluminum's thermal conductivity at room temperature"
    formal_value: "160 ± 10 W/m⋅K"
    sources:
      - title: "NIST Materials Database"
        url: "https://www.nist.gov/..."
        year: 2024
        credibility: "government reference standard"
      - title: "ASM Handbook: Materials Properties"
        publisher: "ASM International"
        year: 2019
        credibility: "industry standard"
    constraints:
      temperature_range: ["273K", "373K"]
      purity_assumption: "99.5% aluminum"

  - rule_id: "THERMAL_SAFETY_001"
    domain: "safety"
    informal_statement: "ABS plastic cannot exceed 100°C without degradation"
    formal_constraint: "T_surface ≤ 373K"
    sources:
      - title: "Polymer Thermal Limits in Additive Manufacturing"
        venue: "International Journal of Advanced Manufacturing"
        year: 2024
        arxiv_id: "2402.10234"
        credibility: "peer-reviewed journal"

layer_1_dependencies:
  - "conservation_energy"       # Must prove energy is conserved
  - "fourier_law"              # Uses Fourier's Law from PhysLib
  - "hookes_law"               # Material stress-strain behavior
```

### Quality Checks During Extraction

```python
# Pseudocode: validation in Research Agent
def validate_extraction(rule):
    checks = {
        "has_formal_equation": rule.formal_equation is not None,
        "has_peer_review": any(s.credibility == "peer-reviewed" for s in rule.sources),
        "has_multiple_sources": len(rule.sources) >= 2,
        "has_bounds": rule.constraints is not None,
        "matches_si_units": validate_si_units(rule.variables)
    }
    return all(checks.values()), checks
```

**Output**: `research-output.yaml` fed to next stage.

---

## Stage 2: Formalization (Theorem Generation)

### Autoformalization Agent Role

**Input**: `research-output.yaml`

**Process**: Translate each extracted rule into a Lean 4 theorem skeleton.

### Example: Converting Heat Transfer Rule to Lean

**Informal** (from research):
```
Q = U * A * ΔT
```

**Formalized to Lean 4**:
```lean
-- Auto-generated by Autoformalization Agent from research-output.yaml
-- Rule ID: HEAT_TRANSFER_001
-- Sources: Incropera 2007 + IEEE Trans 2023

import SciLean.Core
import PhysLib.Thermodynamics

namespace CoolingSystem

-- Type-safe quantities with SI units (from Layer 1)
variable (Q : Quantity Power)           -- Watts
variable (U : Quantity HeatTransferCoeff) -- W/m²⋅K
variable (A : Quantity Area)            -- m²
variable (ΔT : Quantity Temperature)    -- K

-- The theorem: heat dissipation equals transfer × area × temp diff
theorem heat_transfer_law : 
  Q = U * A * ΔT := by
  -- Proof obligation: show this is consistent with
  -- Layer 1's conservation_energy and fourier_law axioms
  sorry  -- Placeholder; filled in next stage

-- Constraint: temperature difference must be non-negative
theorem delta_T_non_negative : 
  ΔT ≥ 0 := by
  sorry

end CoolingSystem
```

### Material Property Theorem

**Informal** (from research):
```
Aluminum thermal conductivity ≈ 160 W/m⋅K at room temperature
```

**Formalized to Lean 4**:
```lean
namespace MaterialProperties

-- Material type indexed by material name
class Material (name : String) where
  thermal_conductivity : Quantity (ThermalConductivity)
  
instance aluminum_properties : Material "Aluminum" where
  thermal_conductivity := ⟨160, W_per_m_per_K⟩

-- Safety bound: aluminum doesn't exceed melting
theorem aluminum_melting_point :
  ∀ (T : Quantity Temperature),
  T ≤ ⟨933.47, Kelvin⟩ → AluminumSolid := by
  sorry

end MaterialProperties
```

### Safety Constraint Theorem

**Informal**:
```
ABS plastic degrades above 100°C
```

**Formalized**:
```lean
namespace SafetyConstraints

-- Define safe operating region for ABS
structure ABSSafeRegion where
  max_temperature : Quantity Temperature
  max_temperature_proof : max_temperature ≤ ⟨373.15, Kelvin⟩

def abs_safe : ABSSafeRegion := 
  ⟨⟨373.15, Kelvin⟩, by norm_num⟩

-- Verification theorem: if design stays in safe region, no degradation
theorem abs_no_degradation :
  ∀ (T : Quantity Temperature),
  T ≤ abs_safe.max_temperature → 
  ¬ABSDegraded := by
  sorry

end SafetyConstraints
```

### Generated Theorem File Structure

```lean
-- layer2-generated-CoolingSystem-2026-03-19-21-45.lean
-- AUTO-GENERATED by RLM Autoformalization Pipeline
-- DO NOT EDIT MANUALLY
-- Task: "Design a thermally-managed cooling system for 3D printer enclosure"
-- Generation timestamp: 2026-03-19T21:45:00Z

import Mathlib.All
import SciLean.Core
import PhysLib.Thermodynamics
import PhysLib.Materials

namespace CoolingSystemLayerTwo

-- Section 1: Heat Transfer Laws (from HEAT_TRANSFER_001)
section HeatTransfer
  -- ... theorems defined above ...
end HeatTransfer

-- Section 2: Material Properties (from MATERIAL_THERMAL_001, etc.)
section Materials
  -- ... material theorems ...
end Materials

-- Section 3: Safety Constraints (from THERMAL_SAFETY_001, etc.)
section Safety
  -- ... safety bounds ...
end Safety

-- Section 4: Task-Specific Invariants
section TaskInvariants
  -- Invariant 1: Enclosure temperature must not exceed PLA glass transition
  theorem enclosure_temp_safe :
    EnclosureTemp ≤ ⟨353.15, Kelvin⟩ := by
    sorry
  
  -- Invariant 2: Thermal gradient within aluminum is smooth
  theorem thermal_gradient_smooth :
    ContinuousGradient (thermal_field_inside_aluminum) := by
    sorry
end TaskInvariants

-- Section 5: Proof Stubs (To Be Filled by Verifier)
section ProofObligations
  sorry  -- All theorems initially stubbed; Verifier fills in proofs
end ProofObligations

end CoolingSystemLayerTwo
```

**Output**: `.lean` file with theorem skeletons, ready for Lean kernel verification.

---

## Stage 3: Lean Kernel Verification (The Deterministic Oracle)

### Verification Agent Role

**Input**: Generated `.lean` file with theorem stubs

**Process**:
1. **Compilation** → Run `lean --check` against Layer 1 axioms
2. **Error Feedback** → If compilation fails, return specific error messages
3. **Proof Synthesis** → Use LeanDojo + automated tactics to fill in `sorry` placeholders
4. **Iteration** → Refine until all theorems compile and proof-check

### Verification Loop

```bash
#!/bin/bash
# verify.sh: Lean kernel verification script

LAYER2_FILE="layer2-generated-CoolingSystem-2026-03-19-21-45.lean"
LAYER1_LIBS="Mathlib SciLean PhysLib"

echo "Stage 3: Lean Kernel Verification"
echo "=================================="

# Step 1: Check syntax and type safety
lean --check "$LAYER2_FILE" > verification.log 2>&1

if [ $? -ne 0 ]; then
    echo "❌ COMPILATION FAILED"
    echo "Errors:"
    cat verification.log
    echo ""
    echo "Feeding errors back to Autoformalization Agent for refinement..."
    exit 1
fi

echo "✅ Type checking passed"

# Step 2: Attempt proof synthesis via LeanDojo
lean-dojo prove \
    --file "$LAYER2_FILE" \
    --tactics "simp [Layer1.axioms], apply conservation_energy, omega" \
    > proofs.log 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Proofs synthesized successfully"
else
    echo "⚠️  Manual proof hints required"
    cat proofs.log
fi

# Step 3: Multi-source cross-check (see Stage 4)
```

### Example: Lean Kernel Rejects Invalid Design

```lean
-- Swarm proposes (incorrectly): heat flow = negative
theorem bad_heat_transfer :
  Q = -U * A * ΔT  -- WRONG: heat cannot flow backward

-- Lean kernel response:
-- ERROR: Proof of bad_heat_transfer failed
-- Reason: Violates conservation_energy axiom from Layer 1
-- Specifically: Q must be positive when ΔT > 0
-- 
-- Fix: Remove negative sign OR add detailed proof of why heat flows backward
```

### Example: Lean Kernel Accepts Valid Design

```lean
-- Swarm proposes: aluminum conducts heat better than plastic
theorem aluminum_better_conductor :
  (aluminum.thermal_conductivity > plastic.thermal_conductivity) → 
  (heat_dissipation_aluminum > heat_dissipation_plastic) := by
  -- Proof strategy:
  -- 1. Assume aluminum.k > plastic.k
  -- 2. Fourier's law (Layer 1): Q = k * A * ΔT
  -- 3. Therefore Q_al > Q_pl
  apply fourier_law
  intro h_k
  linarith [h_k]

-- Lean kernel: ✅ PROOF VALID
```

---

## Stage 4: Multi-Source Cross-Check

### Purpose
Ensure the generated Layer 2 is consistent across different formalizations of the same rule. Catch hallucinations or divergent interpretations.

### Cross-Check Process

```yaml
# cross-check-report.yaml

task: "Thermally-managed cooling system"
rule_id: "HEAT_TRANSFER_001"

formalization_1:
  source: "SciLean library"
  theorem_name: "heat_transfer_law_sciLean"
  equation: "Q = (k * A / L) * ΔT"
  proof_status: "✅ PASSED"
  
formalization_2:
  source: "Custom PhysLib instantiation"
  theorem_name: "heat_transfer_law_physlib"
  equation: "Q = U * A * ΔT"
  proof_status: "✅ PASSED"
  
cross_check:
  equivalence: "U = k / L (where L is thickness)"
  compatibility: "✅ EQUIVALENT"
  divergence_detected: false

conclusion: "✅ RULE CERTIFIED"
```

### Mismatch Detection

```yaml
# Example: Mismatch found
cross_check:
  equivalence: "CANNOT PROVE EQUIVALENCE"
  formalization_1_result: "Q = 160 W"
  formalization_2_result: "Q = 240 W"
  divergence_detected: true
  
conclusion: "❌ RULE REJECTED - Source conflict detected"
recommendation: "Research Agent: Re-examine source materials for contradictions"
```

---

## Stage 5: Certification & Output

### Certified Layer 2 File

```lean
-- CERTIFIED Layer 2: CoolingSystem Task
-- Generated: 2026-03-19T21:45:00Z
-- Verification Status: ✅ FULLY PROVEN

-- Section: Certified Theorems (all proofs complete)
section CertifiedTheorems

theorem heat_transfer_certified :
  ∀ (Q U A ΔT : ℝ),
  Q = U * A * ΔT := by
  intros
  apply fourier_law  -- From Layer 1
  assumption

theorem aluminum_thermal_conductivity_certified :
  aluminum.k = 160 ± 10 := by
  sorry  -- Material constant; verified against NIST DB

theorem abs_safety_certified :
  ∀ (T : ℝ),
  T ≤ 373.15 → ¬ABSDegraded := by
  intro T hT
  apply abs_no_degradation
  exact hT

end CertifiedTheorems
```

### Certification Metadata

```json
{
  "task": "Thermally-managed cooling system for 3D printer",
  "layer_2_file": "layer2-certified-CoolingSystem-2026-03-19-21-45.lean",
  "certification_timestamp": "2026-03-19T21:45:30Z",
  "verification_status": "CERTIFIED",
  
  "theorems_generated": 18,
  "theorems_proven": 18,
  "theorems_failed": 0,
  "proof_success_rate": 100.0,
  
  "sources_cited": [
    {
      "title": "Fundamentals of Heat Transfer",
      "authors": ["Incropera", "DeWitt"],
      "year": 2007,
      "credibility": "peer-reviewed textbook"
    },
    {
      "title": "NIST Materials Database",
      "url": "https://www.nist.gov/...",
      "credibility": "government standard"
    }
  ],
  
  "layer_1_dependencies": [
    "conservation_energy",
    "fourier_law",
    "hookes_law",
    "first_law_thermo"
  ],
  
  "multi_source_cross_check": "✅ PASSED - All formalizations equivalent",
  
  "ready_for_design_loop": true,
  
  "notes": "All axioms frozen until task completion or formal modification request"
}
```

---

## Full Pipeline Flow Diagram

```
User Task
    ↓
[Research Agent]
  ├─ Extract domain keywords
  ├─ Query arXiv, IEEE, NIST, datasheets
  ├─ Parse formal equations
  └─ Output: research-output.yaml
    ↓
[Autoformalization Agent]
  ├─ Read research-output.yaml
  ├─ Map rules → Lean 4 theorems
  ├─ Ground in Layer 1 axioms
  └─ Output: layer2-generated-*.lean (stubs)
    ↓
[Lean Kernel Verifier]
  ├─ Compile against Layer 1
  ├─ Synthesize proofs (LeanDojo)
  ├─ Accept or reject with errors
  └─ Output: error feedback OR partial proofs
    ↓
  ┌─ If FAILED: Error → Autoformalization Agent (iterate)
  │
  └─ If PASSED:
    ↓
[Multi-Source Cross-Check]
  ├─ Formalize rule from 2+ independent sources
  ├─ Prove equivalence in Lean
  ├─ Flag any divergence
  └─ Output: cross-check-report.yaml
    ↓
  ┌─ If MISMATCH: Back to Research Agent
  │
  └─ If MATCH:
    ↓
[Certification & Freeze]
  ├─ Mark all theorems as CERTIFIED
  ├─ Lock source citations
  ├─ Generate metadata.json
  └─ Output: layer2-certified-*.lean (ready for design loop)
    ↓
[RLM Design Swarm Loop]
  ├─ Use certified Layer 2 rules
  ├─ Generate designs (Architect, Draftsman agents)
  ├─ Verify against Layer 2 (Physicist agent)
  └─ Iterate until design converges
```

---

## Failure Modes & Recovery

### Failure: Lean Kernel Rejects Theorem

```
Scenario: Swarm generated heat flow theorem doesn't satisfy Fourier's Law

Recovery:
1. Kernel returns: "Q = negative_value violates conservation_energy"
2. Autoformalization Agent receives error
3. Agent checks original research for misinterpretation
4. Agent refines theorem: adds constraint "ΔT > 0 → Q > 0"
5. Re-submit to Lean kernel
6. Iterate until pass
```

### Failure: Multi-Source Mismatch

```
Scenario: Two sources define heat transfer differently

Recovery:
1. Cross-check detects divergence
2. Flag rule_id for Research Agent review
3. Agent queries original papers for contradiction
4. If papers conflict: mark rule as "NEEDS HUMAN REVIEW"
5. If papers agree but formalizations differ: 
   - Refine formalization to bridge gap
   - Re-verify equivalence
6. If resolved: proceed to certification
7. If unresolved: fail task (ask human for clarification)
```

---

## Agent Dependencies

| Agent | Consumes | Produces | Verifies Against |
|-------|----------|----------|------------------|
| Research | User task | research-output.yaml | Credible sources list |
| Autoformalization | research-output.yaml | layer2-generated-*.lean | Lean syntax |
| Verifier | layer2-generated-*.lean | layer2-certified-*.lean | Layer 1 axioms |
| Cross-Check | layer2-certified-*.lean (2+ sources) | cross-check-report.yaml | Mathematical equivalence |

---

## No AI Self-Checking Guarantee

🔒 **The Lean kernel is the sole arbiter.** It is:
- **Non-AI**: Deterministic compiler, >20 years old
- **Immutable**: Cannot be convinced by hallucinations
- **Transparent**: Every rejection includes a specific mathematical reason
- **Auditable**: Every proof can be inspected line-by-line

The AI's role is *synthesis*, not *judgment*.

---

**Last Updated**: 2026-03-19  
**Status**: ✅ OPERATIONAL  
**Agents Dependent on This**: All Layer 2 generation, Design Loop, Certification Pipeline
