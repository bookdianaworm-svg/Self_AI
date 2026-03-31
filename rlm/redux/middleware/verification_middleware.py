"""
Redux middleware for handling verification-related actions.

This middleware intercepts verification actions and coordinates with the
verification agent factory to perform Layer 1 loading and theorem verification.
"""

from typing import Callable, Any
from rlm.agents.verification_agent_factory import VerificationAgentFactory
from rlm.redux.slices.verification_slice import VerificationActions
from rlm.environments.layer1_bootstrap import Layer1Bootstrap


class VerificationMiddleware:
    """
    Redux middleware for handling verification-related actions.
    
    This middleware intercepts verification actions and uses the
    VerificationAgentFactory to spawn specialized verification agents.
    """
    
    def __init__(self, store):
        """
        Initialize verification middleware.
        
        Args:
            store: Redux store instance
        """
        self.store = store
        self.agent_factory = None
    
    def __call__(self, store: Callable) -> Callable:
        """
        Middleware factory function.
        
        Args:
            store: Redux store
        
        Returns:
            Middleware function
        """
        def middleware(next: Callable) -> Callable:
            def dispatch(action: dict) -> Any:
                # Handle verification actions
                if action is None:
                    return next(action)
                if action.get("type") == "verification/load_layer1_request":
                    self._handle_load_layer1(action)
                elif action.get("type") == "verification/verify_theorem_request":
                    self._handle_verify_theorem(action)
                
                return next(action)
            return dispatch
        return middleware
    
    def _handle_load_layer1(self, action: dict):
        """
        Handle Layer 1 loading request.
        
        This method coordinates the loading of the Layer 1 Axiomatic Foundation
        and dispatches appropriate success/failure actions.
        
        Args:
            action: The load_layer1_request action
        """
        try:
            # Create Layer 1 bootstrap instance
            layer1_path = action.get("payload", {}).get("layer1_path")
            bootstrap = Layer1Bootstrap(layer1_path=layer1_path)
            
            # Load Layer 1
            result = bootstrap.load_layer1()
            
            if result.get("success"):
                # Dispatch success action
                self.store.dispatch(VerificationActions.load_layer1_success(result))
            else:
                # Dispatch failure action
                error = result.get("error", "Unknown error loading Layer 1")
                self.store.dispatch(VerificationActions.load_layer1_failure(error))
        
        except Exception as e:
            # Dispatch failure action on exception
            self.store.dispatch(VerificationActions.load_layer1_failure(str(e)))
    
    def _handle_verify_theorem(self, action: dict):
        """
        Handle theorem verification request.
        
        This method creates a Verifier Agent and uses it to verify the
        specified theorem against Layer 1 axioms.
        
        Args:
            action: The verify_theorem_request action
        """
        try:
            payload = action.get("payload", {})
            theorem_id = payload.get("theorem_id")
            layer2_file = payload.get("layer2_file")
            
            if not theorem_id or not layer2_file:
                raise ValueError("theorem_id and layer2_file are required")
            
            # Use the agent factory if set, otherwise try to get parent RLM from store
            factory = self.agent_factory
            if factory is None:
                parent_rlm = getattr(self.store, 'parent_rlm', None)
                if parent_rlm is not None:
                    factory = VerificationAgentFactory(parent_rlm)
            
            if factory is not None:
                agent = factory.create_verifier_agent(layer2_file)
                result = agent.completion(f"Verify theorem {theorem_id}")
                if result.get("success"):
                    self.store.dispatch(VerificationActions.verify_theorem_success(
                        theorem_id, result.get("proof", "")
                    ))
                else:
                    self.store.dispatch(VerificationActions.verify_theorem_failure(
                        theorem_id, result.get("error", "Verification failed")
                    ))
            else:
                error = "Verification agent factory not initialized"
                self.store.dispatch(VerificationActions.verify_theorem_failure(theorem_id, error))
        
        except Exception as e:
            # Dispatch failure action on exception
            theorem_id = action.get("payload", {}).get("theorem_id", "unknown")
            self.store.dispatch(VerificationActions.verify_theorem_failure(theorem_id, str(e)))
    
    def set_agent_factory(self, agent_factory: VerificationAgentFactory):
        """
        Set the verification agent factory.
        
        This method should be called after the middleware is initialized
        to provide the agent factory for creating verification agents.
        
        Args:
            agent_factory: VerificationAgentFactory instance
        """
        self.agent_factory = agent_factory


__all__ = [
    "VerificationMiddleware",
]
