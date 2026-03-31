# Test Fix Plan for Axiomatic RLM Routing Integration

## Executive Summary

**Current Status**: 116 failed, 234 passed, 21 warnings

**Overall Strategy**: Fix tests in priority order, starting with critical issues that affect multiple test suites, then addressing implementation gaps.

---

## Phase 1: Critical Infrastructure Fixes (High Priority)

### 1.1 Missing Route Methods on Routers

**Issue**: BackendRouter and EnvironmentRouter missing `route()` method

**Affected Tests**:
- All integration tests (41 failures)
- Most routing tests (39 failures)

**Root Cause**: Test files expect `router.route(task_descriptor)` but routers don't implement this method

**Fix Specification**:

1. **BackendRouter.route()** (`rlm/routing/backend_router.py`)
   ```python
   def route(self, task_descriptor: TaskDescriptor) -> BackendRoute:
       """
       Route task to appropriate backend based on task descriptor.

       Args:
           task_descriptor: Task metadata including intent, complexity, capabilities

       Returns:
           BackendRoute with selected backend_id and configuration

       Raises:
           ValueError: If no matching backend found
       """
       # Implementation:
       # 1. Match against config rules based on intent, complexity, capabilities
       # 2. Apply adaptive overrides based on metrics
       # 3. Return route with backend_id and merged config
   ```

2. **EnvironmentRouter.route()** (`rlm/routing/environment_router.py`)
   ```python
   def route(self, task_descriptor: TaskDescriptor) -> EnvironmentRoute:
       """
       Route task to appropriate environment based on security and capabilities.

       Args:
           task_descriptor: Task metadata including security constraints, capabilities

       Returns:
           EnvironmentRoute with environment_id and configuration

       Raises:
           ValueError: If security constraints violated or no matching environment
       """
       # Implementation:
       # 1. Check security constraints first (confidential data always local)
       # 2. Match against capability requirements
       # 3. Return route with environment_id and config
   ```

**Implementation Steps**:
1. Add route methods to both router classes
2. Implement rule matching logic from YAML configs
3. Add adaptive override logic for BackendRouter
4. Add security constraint checking for EnvironmentRouter
5. Update tests to handle edge cases properly

**Acceptance Criteria**:
- All routing tests pass (39 currently failing)
- All integration tests pass (41 currently failing)
- Route matching respects config rules
- Security constraints properly enforced

---

### 1.2 Agent Factory Method Signatures

**Issue**: `create_physicist_agent()` and `create_cross_check_agent()` have wrong signatures in tests

**Affected Tests** (5 failures):
- `test_create_physicist_agent`
- `test_physicist_agent_tools`
- `test_create_cross_check_agent`
- `test_cross_check_agent_tools`
- `test_create_multiple_agents`

**Root Cause**: Tests call these methods without required arguments

**Fix Specification**:

Update tests to provide required parameters:

1. **`create_physicist_agent()`**
   ```python
   # Current test (failing):
   agent = factory.create_physicist_agent()

   # Fixed test:
   agent = factory.create_physicist_agent(
       design_draft="Sample design draft for testing",
       layer2="layer2/theorem1.lean"
   )
   ```

2. **`create_cross_check_agent()`**
   ```python
   # Current test (failing):
   agent = factory.create_cross_check_agent()

   # Fixed test:
   agent = factory.create_cross_check_agent(
       layer2_files=["layer2/theorem1.lean", "layer2/theorem2.lean"]
   )
   ```

**Files to Modify**:
- `tests/agents/test_verification_agent_factory.py` (lines 244, 279, 321, 355, 541)

**Implementation Steps**:
1. Add fixture parameters for design_draft and layer2_files
2. Update all 5 failing tests to use these fixtures
3. Ensure tool validation tests work with actual agent creation

**Acceptance Criteria**:
- All 5 agent factory tests pass
- Tests use realistic sample data
- Tool validation works correctly

---

## Phase 2: Redux State Management Fixes (High Priority)

### 2.1 Initial State Issues

**Issue**: Routing state initialization fails due to missing metrics store

**Affected Tests** (5 failures):
- `test_routing_state_initialization`
- `test_backend_metrics_calculations`
- `test_reducer_initial_state`
- `test_reducer_routing_completed`
- `test_reducer_backend_metrics_updated`

**Root Cause**: RoutingState expects metrics_store but not provided in initialization

**Fix Specification**:

Update `RoutingState` initialization (`rlm/redux/slices/routing_slice.py`):

```python
@dataclass
class RoutingState:
    current_route: Optional[RoutingDecision] = None
    routing_in_progress: bool = False
    last_routing_time: Optional[float] = None
    backend_metrics: Dict[str, BackendMetrics] = field(default_factory=dict)

    def __post_init__(self):
        # Initialize empty dict if not provided
        if not isinstance(self.backend_metrics, dict):
            self.backend_metrics = {}
```

**Files to Modify**:
- `rlm/redux/slices/routing_slice.py`
- `tests/redux/test_routing_slice.py` (update expectations)

**Acceptance Criteria**:
- State initialization works without metrics_store
- BackendMetrics calculations work correctly
- All 5 tests pass

---

### 2.2 Reducer Implementation Gaps

**Issue**: Some reducers not implemented or have incorrect logic

**Affected Tests** (3 failures):
- `test_reducer_unknown_action`
- `test_reducer_routing_completed`
- `test_reducer_backend_metrics_updated`

**Fix Specification**:

1. **Unknown Action Handler**
   ```python
   def routing_reducer(state: RoutingState, action: Any) -> RoutingState:
       if isinstance(action, RoutingAction):
           # Handle known actions
           ...
       else:
           # Return unchanged state for unknown actions
           return state
   ```

2. **Routing Completed Action**
   ```python
   case RoutingAction.ROUTING_COMPLETED:
       return RoutingState(
           current_route=action.decision,
           routing_in_progress=False,
           last_routing_time=time.time(),
           backend_metrics=state.backend_metrics
       )
   ```

3. **Backend Metrics Updated Action**
   ```python
   case RoutingAction.BACKEND_METRICS_UPDATED:
       updated_metrics = state.backend_metrics.copy()
       updated_metrics[action.backend_id] = action.metrics
       return RoutingState(
           current_route=state.current_route,
           routing_in_progress=state.routing_in_progress,
           last_routing_time=state.last_routing_time,
           backend_metrics=updated_metrics
       )
   ```

**Acceptance Criteria**:
- All 3 reducer tests pass
- Reducer is immutable (returns new state)
- Unknown actions don't mutate state

---

### 2.3 Middleware Implementation Gaps

**Issue**: Middleware not handling actions correctly

**Affected Tests** (8 failures):
- `test_handle_load_layer1_success`
- `test_handle_load_layer1_failure`
- `test_handle_load_layer1_with_custom_path`
- `test_handle_load_layer1_exception`
- `test_handle_verify_theorem_success`
- `test_handle_verify_theorem_with_payload`
- `test_intercepts_load_layer1_request`
- `test_load_layer1_with_bootstrap_error`
- `test_middleware_with_none_action`
- `test_multiple_load_layer1_requests`

**Root Cause**: Middleware not properly intercepting and handling actions

**Fix Specification**:

Update middleware (`rlm/redux/middleware/verification_middleware.py`):

```python
def verification_middleware(store):
    def middleware(next_dispatcher):
        def dispatcher(action):
            # Handle Load Layer1 actions
            if action.type == VerificationAction.LOAD_LAYER1_REQUEST:
                # Load Layer1 and dispatch success/failure
                try:
                    bootstrap = Layer1Bootstrap()
                    bootstrap.load_layer1()
                    store.dispatch(VerificationAction.LOAD_LAYER1_SUCCESS(...))
                except Exception as e:
                    store.dispatch(VerificationAction.LOAD_LAYER1_FAILURE(...))

            # Handle Verify Theorem actions
            elif action.type == VerificationAction.VERIFY_THEOREM_REQUEST:
                # Verify theorem and dispatch result
                try:
                    result = verify_theorem(...)
                    store.dispatch(VerificationAction.VERIFY_THEOREM_SUCCESS(...))
                except Exception as e:
                    store.dispatch(VerificationAction.VERIFY_THEOREM_FAILURE(...))

            # Pass action to next middleware/reducer
            return next_dispatcher(action)

        return dispatcher
    return middleware
```

**Acceptance Criteria**:
- All 8 middleware tests pass
- Actions properly intercepted and handled
- Errors properly caught and dispatched as failures

---

## Phase 3: Environment Layer 1 Fixes (Medium Priority)

### 3.1 Mock Layer 1 Dependencies

**Issue**: Tests fail because Layer 1 components (Lean, PhysLib, Haskell) not installed

**Affected Tests** (9 failures):
- `test_load_lean_kernel_success`
- `test_load_physlib_success`
- `test_compile_haskell_types_success`
- `test_get_mathlib_version`
- `test_get_physlib_version`
- `test_get_memory_usage`
- `test_get_memory_usage_with_exception`
- `test_multiple_layer1_tool_calls`
- `test_verification_without_layer1_loaded`

**Root Cause**: Tests try to load real Layer 1 components instead of mocking

**Fix Specification**:

Update tests to use proper mocks:

1. **Mock Lean Kernel**
   ```python
   @patch('rlm.environments.layer1_bootstrap.os.path.exists', return_value=True)
   @patch('rlm.environments.layer1_bootstrap.subprocess.run')
   def test_load_lean_kernel_success(self, mock_run, mock_exists):
       mock_run.return_value = MagicMock(returncode=0, stdout="Lean 4.0.0")
       bootstrap = Layer1Bootstrap()
       kernel = bootstrap._load_lean_kernel()
       assert kernel is not None
   ```

2. **Mock PhysLib**
   ```python
   @patch('rlm.environments.layer1_bootstrap.os.path.exists', return_value=True)
   def test_load_physlib_success(self, mock_exists):
       bootstrap = Layer1Bootstrap()
       result = bootstrap._load_physlib()
       assert result is not None
   ```

3. **Fix psutil Mocking**
   ```python
   @patch('psutil.Process')  # Import psutil directly, not from module
   def test_get_memory_usage(self, mock_process):
       mock_proc = MagicMock()
       mock_proc.memory_info.return_value = MagicMock(rss=1024*1024*100)  # 100MB
       mock_process.return_value = mock_proc

       bootstrap = Layer1Bootstrap()
       memory = bootstrap.get_memory_usage()
       assert memory > 0
   ```

4. **Mock Version Files**
   ```python
   @patch('builtins.open', new_callable=mock_open, read_data="v4.0.0\n")
   def test_get_mathlib_version(self, mock_file):
       bootstrap = Layer1Bootstrap()
       version = bootstrap._get_mathlib_version()
       assert version == "v4.0.0"
   ```

**Files to Modify**:
- `tests/environments/test_layer1_bootstrap.py`
- `tests/environments/test_local_repl_layer1.py`
- `tests/integration/test_layer1_verification_flow.py`

**Acceptance Criteria**:
- All Layer 1 tests pass without requiring actual installations
- Proper mocking of filesystem operations
- Mocks return realistic test data

---

### 3.2 Prompt Consistency Test

**Issue**: Test expects "Layer 1" in all prompts but some don't mention it

**Affected Test** (1 failure):
- `test_all_prompts_use_layer1`

**Root Cause**: Not all prompts explicitly mention "Layer 1"

**Fix Specification**:

Two options:

**Option 1**: Update prompts to mention Layer 1 (preferred for consistency)
```python
# Add to physicist, cross-check prompts:
PHYSICIST_PROMPT = """
You are a physicist agent working with Layer 1 formal verification...
"""

CROSS_CHECK_PROMPT = """
You are a cross-check agent verifying Layer 1 theorems...
"""
```

**Option 2**: Update test to be more lenient
```python
def test_all_prompts_use_layer1():
    """Test that all prompts mention formal verification."""
    for prompt_name, prompt in get_all_prompts().items():
        # Check for either "Layer 1" or "formal verification"
        has_formal = "Layer 1" in prompt or "formal verification" in prompt
        assert has_formal, f"{prompt_name} should mention Layer 1 or formal verification"
```

**Recommendation**: Option 1 - update prompts for consistency

**Files to Modify**:
- `rlm/agents/prompts/verification_prompts.py`
- `tests/agents/test_verification_prompts.py`

**Acceptance Criteria**:
- All prompts mention Layer 1 or formal verification
- Prompt consistency test passes

---

## Phase 4: Routing Edge Cases (Medium Priority)

### 4.1 Task Descriptor Edge Cases

**Issue**: Edge case tests fail due to incorrect expectations or missing logic

**Affected Tests** (8 failures):
- `test_route_with_empty_task_descriptor`
- `test_route_with_extreme_complexity`
- `test_route_with_zero_latency_budget`
- `test_classify_code_generation`
- `test_classify_refactor`
- `test_needs_docker_isolation_detection`
- `test_capability_detection_case_insensitive`
- `test_estimate_complexity_with_negative_depth`

**Fix Specification**:

1. **Empty Task Descriptor**
   ```python
   def route(self, task_descriptor: TaskDescriptor) -> BackendRoute:
       if not task_descriptor or not task_descriptor.prompt:
           raise ValueError("Task descriptor cannot be empty")
       # ... rest of implementation
   ```

2. **Extreme Complexity**
   ```python
   # Test expects fallback to default backend
   def test_route_with_extreme_complexity(self, router):
       task = TaskDescriptor(
           prompt="test",
           complexity=1000.0,  # Extreme value
           intent="code_generation"
       )
       route = router.route(task)
       assert route.backend_id == router.config["default_backend"]
   ```

3. **Negative Depth**
   ```python
   # Test expects clamping to valid range
   def test_estimate_complexity_with_negative_depth(self):
       descriptor = TaskDescriptor(prompt="test", depth=-1)
       complexity = descriptor.estimate_complexity()
       assert complexity >= 0, "Complexity should be non-negative"
   ```

4. **Capability Detection Updates**
   ```python
   def needs_docker_isolation(self) -> bool:
       """Check if task needs docker isolation."""
       keywords = ["docker", "container", "isolation", "sandbox"]
       return any(keyword in self.prompt.lower() for keyword in keywords)
   ```

**Files to Modify**:
- `rlm/routing/task_descriptor.py`
- `tests/routing/test_task_descriptor.py`
- `tests/routing/test_backend_router.py`

**Acceptance Criteria**:
- All edge case tests pass
- Proper validation of inputs
- Sensible defaults for edge cases

---

### 4.2 Environment Router Edge Cases

**Issue**: Security constraint tests failing

**Affected Tests** (10 failures):
- `test_route_lean_task_to_local`
- `test_route_internet_task_to_modal`
- `test_route_sensitive_data_to_local`
- `test_route_with_no_matching_rule`
- `test_route_high_cpu_task_to_modal`
- `test_confidential_data_always_local`
- `test_public_data_can_use_remote`
- `test_internal_data_restricted_in_dev`
- `test_lean_access_requires_local`
- `test_haskell_access_requires_local`
- `test_filesystem_access_allows_docker`
- `test_multiple_capabilities_priority`
- `test_route_with_empty_task_descriptor`
- `test_route_with_extreme_cpu_requirements`
- `test_route_with_unknown_capability`
- `test_route_with_none_metrics`

**Fix Specification**:

Implement comprehensive security and capability routing:

```python
def route(self, task_descriptor: TaskDescriptor) -> EnvironmentRoute:
    # 1. Security constraints take precedence
    if task_descriptor.security_level == SecurityLevel.CONFIDENTIAL:
        return EnvironmentRoute(
            environment_id="local",
            config=self._get_config("local")
        )

    # 2. Check capability requirements
    if task_descriptor.needs_lean_access():
        return EnvironmentRoute(
            environment_id="local",
            config=self._get_config("local")
        )

    if task_descriptor.needs_haskell_access():
        return EnvironmentRoute(
            environment_id="local",
            config=self._get_config("local")
        )

    # 3. Check for resource-intensive tasks
    if task_descriptor.estimated_cpu_time > 3600:  # > 1 hour
        return EnvironmentRoute(
            environment_id="modal",
            config=self._get_config("modal")
        )

    # 4. Match against config rules
    for rule in self.config["rules"]:
        if self._matches_rule(task_descriptor, rule):
            return EnvironmentRoute(
                environment_id=rule["environment"],
                config=self._get_config(rule["environment"])
            )

    # 5. Default fallback
    return EnvironmentRoute(
        environment_id=self.config["default_environment"],
        config=self._get_config(self.config["default_environment"])
    )
```

**Acceptance Criteria**:
- All environment routing tests pass
- Security constraints properly enforced
- Capability routing works correctly
- Proper fallback handling

---

## Phase 5: Metrics Tracking (Low Priority)

### 5.1 Backend Metrics Implementation

**Issue**: Metrics tracking methods not implemented

**Affected Tests** (6 failures):
- `test_record_backend_call`
- `test_record_failed_backend_call`
- `test_get_backend_metrics`
- `test_metrics_aggregation`
- `test_adaptive_override_based_on_metrics`
- `test_adaptive_override_with_high_latency`

**Fix Specification**:

Implement metrics tracking in BackendRouter:

```python
class BackendRouter:
    def __init__(self):
        self.metrics_store: Dict[str, BackendMetrics] = {}

    def record_backend_call(self, backend_id: str, latency: float, success: bool):
        """Record a backend call for metrics."""
        if backend_id not in self.metrics_store:
            self.metrics_store[backend_id] = BackendMetrics(
                backend_id=backend_id,
                total_calls=0,
                successful_calls=0,
                failed_calls=0,
                total_latency=0.0,
                avg_latency=0.0
            )

        metrics = self.metrics_store[backend_id]
        metrics.total_calls += 1
        metrics.total_latency += latency
        metrics.avg_latency = metrics.total_latency / metrics.total_calls

        if success:
            metrics.successful_calls += 1
        else:
            metrics.failed_calls += 1

    def record_failed_backend_call(self, backend_id: str, error: Exception):
        """Record a failed backend call."""
        self.record_backend_call(backend_id, 0.0, False)

    def get_backend_metrics(self, backend_id: str) -> Optional[BackendMetrics]:
        """Get metrics for a specific backend."""
        return self.metrics_store.get(backend_id)

    def get_all_metrics(self) -> Dict[str, BackendMetrics]:
        """Get all backend metrics."""
        return self.metrics_store.copy()
```

**Acceptance Criteria**:
- All metrics tracking tests pass
- Metrics properly updated after each call
- Aggregation calculations correct

---

## Phase 6: Integration Tests Cleanup

### 6.1 Test Implementation Updates

**Issue**: Integration tests have implementation gaps after route methods added

**Affected Tests**: All remaining integration test failures after route methods implemented

**Fix Specification**:

Update integration tests to work with route methods:

1. **Backend Routing Flow**
   ```python
   def test_complete_backend_routing_flow(self, mock_rlm):
       # Create router
       router = BackendRouter()

       # Create task descriptor
       task = TaskDescriptor(
           prompt="Write a proof for theorem X",
           intent="proof_synthesis",
           complexity=0.7
       )

       # Route task
       route = router.route(task)

       # Verify route
       assert route.backend_id == "claude_agent"
       assert route.config["model"] == "claude-3-opus"

       # Record metrics
       router.record_backend_call(route.backend_id, 1.5, True)
       metrics = router.get_backend_metrics(route.backend_id)
       assert metrics.total_calls == 1
       assert metrics.successful_calls == 1
   ```

2. **Environment Routing Flow**
   ```python
   def test_complete_environment_routing_flow(self, mock_rlm):
       # Create router
       router = EnvironmentRouter()

       # Create task descriptor with security constraints
       task = TaskDescriptor(
           prompt="Verify theorem X",
           security_level=SecurityLevel.CONFIDENTIAL,
           capabilities=["lean_access"]
       )

       # Route task
       route = router.route(task)

       # Verify route respects security
       assert route.environment_id == "local"
       assert "lean" in route.config.get("enabled_tools", [])
   ```

3. **Combined Routing**
   ```python
   def test_combined_routing_flow(self, mock_rlm):
       # Create both routers
       backend_router = BackendRouter()
       env_router = EnvironmentRouter()

       # Route task
       task = TaskDescriptor(
           prompt="Prove theorem X with Lean",
           intent="proof_synthesis",
           capabilities=["lean_access"]
       )

       backend_route = backend_router.route(task)
       env_route = env_router.route(task)

       # Verify routes are consistent
       assert backend_route.backend_id == "claude_agent"
       assert env_route.environment_id == "local"
   ```

**Acceptance Criteria**:
- All integration tests pass
- Tests properly mock RLM and dependencies
- Tests validate end-to-end workflows

---

## Implementation Timeline

### Week 1: Critical Infrastructure
- Day 1-2: Implement route() methods on BackendRouter and EnvironmentRouter
- Day 3: Fix agent factory method signatures
- Day 4-5: Fix Redux state initialization issues

### Week 2: Redux & Environment Layer
- Day 1-2: Fix reducer implementation gaps
- Day 3-4: Fix middleware implementation gaps
- Day 5: Mock Layer 1 dependencies

### Week 3: Routing Edge Cases & Metrics
- Day 1-2: Fix task descriptor edge cases
- Day 3-4: Fix environment router edge cases
- Day 5: Implement metrics tracking

### Week 4: Integration Tests & Cleanup
- Day 1-3: Update and fix integration tests
- Day 4: Run full test suite and fix remaining issues
- Day 5: Final validation and documentation

---

## Success Criteria

1. **All tests pass**: 0 failures, 350 passes
2. **Test coverage maintained**: ≥ 80% coverage for modified code
3. **No regressions**: Previously passing tests continue to pass
4. **Documentation updated**: All modified methods documented
5. **Code quality**: Passes linting and type checking

---

## Risk Assessment

### High Risk
- Route method implementation may break existing code
- Redux state changes may affect production usage

**Mitigation**: Extensive testing, careful review of changes

### Medium Risk
- Mock implementations may not match real behavior
- Edge case handling may be incomplete

**Mitigation**: Add integration tests with real components when possible

### Low Risk
- Prompt consistency changes
- Test fixture updates

**Mitigation**: Minimal impact, easily reversible

---

## Testing Strategy

1. **Unit Tests**: Fix individual test failures one by one
2. **Integration Tests**: Ensure components work together
3. **Regression Tests**: Run full suite after each major change
4. **Manual Testing**: Verify routing decisions make sense
5. **Performance Testing**: Ensure metrics tracking doesn't slow system

---

## Rollback Plan

If any changes cause issues:

1. Git revert problematic commits
2. Document what broke and why
3. Create alternative approach
4. Test thoroughly before reapplying

---

## Post-Implementation Tasks

1. Update documentation with new methods
2. Add examples for route usage
3. Create integration guides
4. Update CI/CD pipelines
5. Add performance benchmarks
6. Document test coverage reports
