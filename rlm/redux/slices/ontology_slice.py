"""
Redux slice for universal ontology bootstrapping state management.

This module provides state management for the Universal Ontology Bootstrapping (Domain Zero),
handling novel domain formalization without hardcoded libraries.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
from enum import Enum
import time


class OntologyStatus(Enum):
    """Status of an ontology task."""

    PENDING = "pending"
    GENERATING = "generating"
    PROVING_GENESIS = "proving_genesis"
    CERTIFIED = "certified"
    FAILED = "failed"
    REQUIRES_ADJUSTMENT = "requires_adjustment"


class InhabitationProofStatus(Enum):
    """Status of an inhabitation proof."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"


@dataclass
class StructureInvariant:
    """An invariant rule deduced for a structure."""

    name: str
    description: str
    lean_expression: str
    is_verified: bool = False
    verification_error: Optional[str] = None


@dataclass
class StateTransitionFunction:
    """A state transition function for complex domains."""

    name: str
    input_type: str
    output_type: str
    lean_definition: str
    is_verified: bool = False


@dataclass
class OntologyStructure:
    """A formal structure representing a novel domain."""

    id: str
    name: str
    description: str
    lean_structure: str
    invariants: List[StructureInvariant] = field(default_factory=list)
    state_transitions: List[StateTransitionFunction] = field(default_factory=list)
    inhabitation_proof_status: InhabitationProofStatus = InhabitationProofStatus.PENDING
    created_at: float = field(default_factory=time.time)


@dataclass
class GenesisState:
    """A genesis state proof for an ontology structure."""

    id: str
    structure_id: str
    lean_genesis: str
    proof_script: str
    is_verified: bool = False
    verifier_output: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    verified_at: Optional[float] = None


@dataclass
class InvariantProof:
    """Proof that invariants are preserved across state transitions."""

    id: str
    structure_id: str
    invariant_name: str
    theorem_name: str
    proof_script: str
    is_verified: bool = False
    verification_error: Optional[str] = None
    created_at: float = field(default_factory=time.time)


@dataclass
class OntologyTask:
    """A task to formalize a novel domain as ontology."""

    id: str
    domain_description: str
    status: OntologyStatus = OntologyStatus.PENDING
    structure_id: Optional[str] = None
    genesis_state_id: Optional[str] = None
    error_message: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None


@dataclass
class OntologyState:
    """Redux slice for ontology bootstrapping state."""

    active_tasks: Dict[str, OntologyTask] = field(default_factory=dict)
    structures: Dict[str, OntologyStructure] = field(default_factory=dict)
    genesis_states: Dict[str, GenesisState] = field(default_factory=dict)
    invariant_proofs: Dict[str, InvariantProof] = field(default_factory=dict)
    failed_attempts: List[Dict] = field(default_factory=list)


class OntologyActions:
    """Action creators for ontology state updates."""

    @staticmethod
    def create_task(task: OntologyTask) -> dict:
        """Create action to create an ontology task."""
        return {
            "type": "ontology/create_task",
            "payload": {
                "id": task.id,
                "domain_description": task.domain_description,
            },
        }

    @staticmethod
    def update_task_status(task_id: str, status: OntologyStatus) -> dict:
        """Create action to update task status."""
        return {
            "type": "ontology/update_task_status",
            "payload": {
                "task_id": task_id,
                "status": status.value,
            },
        }

    @staticmethod
    def create_structure(structure: OntologyStructure) -> dict:
        """Create action to create an ontology structure."""
        return {
            "type": "ontology/create_structure",
            "payload": {
                "id": structure.id,
                "name": structure.name,
                "description": structure.description,
                "lean_structure": structure.lean_structure,
            },
        }

    @staticmethod
    def add_invariant(structure_id: str, invariant: StructureInvariant) -> dict:
        """Create action to add an invariant to a structure."""
        return {
            "type": "ontology/add_invariant",
            "payload": {
                "structure_id": structure_id,
                "name": invariant.name,
                "description": invariant.description,
                "lean_expression": invariant.lean_expression,
            },
        }

    @staticmethod
    def verify_invariant(
        structure_id: str,
        invariant_name: str,
        verified: bool,
        error: Optional[str] = None,
    ) -> dict:
        """Create action to verify an invariant."""
        return {
            "type": "ontology/verify_invariant",
            "payload": {
                "structure_id": structure_id,
                "invariant_name": invariant_name,
                "verified": verified,
                "error": error,
            },
        }

    @staticmethod
    def add_state_transition(
        structure_id: str, transition: StateTransitionFunction
    ) -> dict:
        """Create action to add a state transition function."""
        return {
            "type": "ontology/add_state_transition",
            "payload": {
                "structure_id": structure_id,
                "name": transition.name,
                "input_type": transition.input_type,
                "output_type": transition.output_type,
                "lean_definition": transition.lean_definition,
            },
        }

    @staticmethod
    def create_genesis_state(genesis: GenesisState) -> dict:
        """Create action to create a genesis state."""
        return {
            "type": "ontology/create_genesis_state",
            "payload": {
                "id": genesis.id,
                "structure_id": genesis.structure_id,
                "lean_genesis": genesis.lean_genesis,
                "proof_script": genesis.proof_script,
            },
        }

    @staticmethod
    def verify_genesis_state(
        genesis_id: str, is_verified: bool, verifier_output: Optional[str] = None
    ) -> dict:
        """Create action to verify a genesis state."""
        return {
            "type": "ontology/verify_genesis_state",
            "payload": {
                "genesis_id": genesis_id,
                "is_verified": is_verified,
                "verifier_output": verifier_output,
            },
        }

    @staticmethod
    def create_invariant_proof(proof: InvariantProof) -> dict:
        """Create action to create an invariant preservation proof."""
        return {
            "type": "ontology/create_invariant_proof",
            "payload": {
                "id": proof.id,
                "structure_id": proof.structure_id,
                "invariant_name": proof.invariant_name,
                "theorem_name": proof.theorem_name,
                "proof_script": proof.proof_script,
            },
        }

    @staticmethod
    def verify_invariant_proof(
        proof_id: str, is_verified: bool, error: Optional[str] = None
    ) -> dict:
        """Create action to verify an invariant proof."""
        return {
            "type": "ontology/verify_invariant_proof",
            "payload": {
                "proof_id": proof_id,
                "is_verified": is_verified,
                "error": error,
            },
        }

    @staticmethod
    def complete_task(task_id: str, structure_id: str, genesis_id: str) -> dict:
        """Create action to complete an ontology task."""
        return {
            "type": "ontology/complete_task",
            "payload": {
                "task_id": task_id,
                "structure_id": structure_id,
                "genesis_id": genesis_id,
            },
        }

    @staticmethod
    def fail_task(task_id: str, error_message: str) -> dict:
        """Create action to mark a task as failed."""
        return {
            "type": "ontology/fail_task",
            "payload": {
                "task_id": task_id,
                "error_message": error_message,
            },
        }

    @staticmethod
    def request_adjustment(task_id: str, reason: str) -> dict:
        """Create action to request ontology adjustment."""
        return {
            "type": "ontology/request_adjustment",
            "payload": {
                "task_id": task_id,
                "reason": reason,
            },
        }


def ontology_reducer(state: OntologyState, action: dict) -> OntologyState:
    """
    Reducer function for ontology state.

    Args:
        state: Current ontology state.
        action: Action to apply to the state.

    Returns:
        New ontology state.
    """
    action_type = action.get("type")

    if action_type == "ontology/create_task":
        payload = action.get("payload", {})
        task = OntologyTask(
            id=payload.get("id"),
            domain_description=payload.get("domain_description"),
            status=OntologyStatus.PENDING,
        )
        new_tasks = state.active_tasks.copy()
        new_tasks[task.id] = task
        return OntologyState(
            active_tasks=new_tasks,
            structures=state.structures,
            genesis_states=state.genesis_states,
            invariant_proofs=state.invariant_proofs,
            failed_attempts=state.failed_attempts,
        )

    elif action_type == "ontology/update_task_status":
        payload = action.get("payload", {})
        task_id = payload.get("task_id")
        task = state.active_tasks.get(task_id)
        if task:
            task.status = OntologyStatus(payload.get("status"))
            new_tasks = state.active_tasks.copy()
            new_tasks[task_id] = task
            return OntologyState(
                active_tasks=new_tasks,
                structures=state.structures,
                genesis_states=state.genesis_states,
                invariant_proofs=state.invariant_proofs,
                failed_attempts=state.failed_attempts,
            )
        return state

    elif action_type == "ontology/create_structure":
        payload = action.get("payload", {})
        structure = OntologyStructure(
            id=payload.get("id"),
            name=payload.get("name"),
            description=payload.get("description"),
            lean_structure=payload.get("lean_structure"),
        )
        new_structures = state.structures.copy()
        new_structures[structure.id] = structure
        return OntologyState(
            active_tasks=state.active_tasks,
            structures=new_structures,
            genesis_states=state.genesis_states,
            invariant_proofs=state.invariant_proofs,
            failed_attempts=state.failed_attempts,
        )

    elif action_type == "ontology/add_invariant":
        payload = action.get("payload", {})
        structure_id = payload.get("structure_id")
        structure = state.structures.get(structure_id)
        if structure:
            invariant = StructureInvariant(
                name=payload.get("name"),
                description=payload.get("description"),
                lean_expression=payload.get("lean_expression"),
            )
            structure.invariants.append(invariant)
            new_structures = state.structures.copy()
            new_structures[structure_id] = structure
            return OntologyState(
                active_tasks=state.active_tasks,
                structures=new_structures,
                genesis_states=state.genesis_states,
                invariant_proofs=state.invariant_proofs,
                failed_attempts=state.failed_attempts,
            )
        return state

    elif action_type == "ontology/verify_invariant":
        payload = action.get("payload", {})
        structure_id = payload.get("structure_id")
        invariant_name = payload.get("invariant_name")
        verified = payload.get("verified", False)
        structure = state.structures.get(structure_id)
        if structure:
            for inv in structure.invariants:
                if inv.name == invariant_name:
                    inv.is_verified = verified
                    inv.verification_error = payload.get("error")
                    break
            new_structures = state.structures.copy()
            new_structures[structure_id] = structure
            return OntologyState(
                active_tasks=state.active_tasks,
                structures=new_structures,
                genesis_states=state.genesis_states,
                invariant_proofs=state.invariant_proofs,
                failed_attempts=state.failed_attempts,
            )
        return state

    elif action_type == "ontology/add_state_transition":
        payload = action.get("payload", {})
        structure_id = payload.get("structure_id")
        structure = state.structures.get(structure_id)
        if structure:
            transition = StateTransitionFunction(
                name=payload.get("name"),
                input_type=payload.get("input_type"),
                output_type=payload.get("output_type"),
                lean_definition=payload.get("lean_definition"),
            )
            structure.state_transitions.append(transition)
            new_structures = state.structures.copy()
            new_structures[structure_id] = structure
            return OntologyState(
                active_tasks=state.active_tasks,
                structures=new_structures,
                genesis_states=state.genesis_states,
                invariant_proofs=state.invariant_proofs,
                failed_attempts=state.failed_attempts,
            )
        return state

    elif action_type == "ontology/create_genesis_state":
        payload = action.get("payload", {})
        genesis = GenesisState(
            id=payload.get("id"),
            structure_id=payload.get("structure_id"),
            lean_genesis=payload.get("lean_genesis"),
            proof_script=payload.get("proof_script"),
        )
        new_genesis = state.genesis_states.copy()
        new_genesis[genesis.id] = genesis
        structure = state.structures.get(genesis.structure_id)
        if structure:
            structure.inhabitation_proof_status = InhabitationProofStatus.IN_PROGRESS
            new_structures = state.structures.copy()
            new_structures[structure.id] = structure
        else:
            new_structures = state.structures
        return OntologyState(
            active_tasks=state.active_tasks,
            structures=new_structures,
            genesis_states=new_genesis,
            invariant_proofs=state.invariant_proofs,
            failed_attempts=state.failed_attempts,
        )

    elif action_type == "ontology/verify_genesis_state":
        payload = action.get("payload", {})
        genesis_id = payload.get("genesis_id")
        genesis = state.genesis_states.get(genesis_id)
        if genesis:
            genesis.is_verified = payload.get("is_verified", False)
            genesis.verifier_output = payload.get("verifier_output")
            if genesis.is_verified:
                genesis.verified_at = time.time()
                structure = state.structures.get(genesis.structure_id)
                if structure:
                    structure.inhabitation_proof_status = InhabitationProofStatus.PASSED
            new_genesis = state.genesis_states.copy()
            new_genesis[genesis_id] = genesis
            return OntologyState(
                active_tasks=state.active_tasks,
                structures=state.structures,
                genesis_states=new_genesis,
                invariant_proofs=state.invariant_proofs,
                failed_attempts=state.failed_attempts,
            )
        return state

    elif action_type == "ontology/create_invariant_proof":
        payload = action.get("payload", {})
        proof = InvariantProof(
            id=payload.get("id"),
            structure_id=payload.get("structure_id"),
            invariant_name=payload.get("invariant_name"),
            theorem_name=payload.get("theorem_name"),
            proof_script=payload.get("proof_script"),
        )
        new_proofs = state.invariant_proofs.copy()
        new_proofs[proof.id] = proof
        return OntologyState(
            active_tasks=state.active_tasks,
            structures=state.structures,
            genesis_states=state.genesis_states,
            invariant_proofs=new_proofs,
            failed_attempts=state.failed_attempts,
        )

    elif action_type == "ontology/verify_invariant_proof":
        payload = action.get("payload", {})
        proof_id = payload.get("proof_id")
        proof = state.invariant_proofs.get(proof_id)
        if proof:
            proof.is_verified = payload.get("is_verified", False)
            proof.verification_error = payload.get("error")
            new_proofs = state.invariant_proofs.copy()
            new_proofs[proof_id] = proof
            return OntologyState(
                active_tasks=state.active_tasks,
                structures=state.structures,
                genesis_states=state.genesis_states,
                invariant_proofs=new_proofs,
                failed_attempts=state.failed_attempts,
            )
        return state

    elif action_type == "ontology/complete_task":
        payload = action.get("payload", {})
        task_id = payload.get("task_id")
        task = state.active_tasks.get(task_id)
        if task:
            task.status = OntologyStatus.CERTIFIED
            task.structure_id = payload.get("structure_id")
            task.genesis_state_id = payload.get("genesis_id")
            task.completed_at = time.time()
            new_tasks = state.active_tasks.copy()
            new_tasks[task_id] = task
            return OntologyState(
                active_tasks=new_tasks,
                structures=state.structures,
                genesis_states=state.genesis_states,
                invariant_proofs=state.invariant_proofs,
                failed_attempts=state.failed_attempts,
            )
        return state

    elif action_type == "ontology/fail_task":
        payload = action.get("payload", {})
        task_id = payload.get("task_id")
        task = state.active_tasks.get(task_id)
        if task:
            task.status = OntologyStatus.FAILED
            task.error_message = payload.get("error_message")
            task.completed_at = time.time()
            new_tasks = state.active_tasks.copy()
            new_tasks[task_id] = task
            new_failed = state.failed_attempts + [
                {
                    "task_id": task_id,
                    "error": payload.get("error_message"),
                    "failed_at": time.time(),
                }
            ]
            return OntologyState(
                active_tasks=new_tasks,
                structures=state.structures,
                genesis_states=state.genesis_states,
                invariant_proofs=state.invariant_proofs,
                failed_attempts=new_failed,
            )
        return state

    elif action_type == "ontology/request_adjustment":
        payload = action.get("payload", {})
        task_id = payload.get("task_id")
        task = state.active_tasks.get(task_id)
        if task:
            task.status = OntologyStatus.REQUIRES_ADJUSTMENT
            task.error_message = payload.get("reason")
            new_tasks = state.active_tasks.copy()
            new_tasks[task_id] = task
            return OntologyState(
                active_tasks=new_tasks,
                structures=state.structures,
                genesis_states=state.genesis_states,
                invariant_proofs=state.invariant_proofs,
                failed_attempts=state.failed_attempts,
            )
        return state

    return state
