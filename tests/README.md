# Test Suite for Axiomatic RLM Routing Integration

This test suite provides comprehensive coverage for the axiomatic RLM routing integration upgrade, covering 14 components across 5 layers.

## Test Structure

```
tests/
├── __init__.py
├── mock_lm.py                 # Mock Language Model for testing
├── conftest.py                 # Pytest fixtures and shared setup
├── routing/                    # Routing layer tests
│   ├── __init__.py
│   ├── test_backend_router.py      # Backend routing, config loading, metrics
│   ├── test_backend_factory.py     # Backend client creation, ID mapping
│   ├── test_environment_router.py   # Environment routing, security constraints
│   ├── test_environment_factory.py # Environment instance creation
│   └── test_task_descriptor.py    # Intent classification, complexity estimation
├── environments/                # Layer1 environment tests
│   ├── __init__.py
│   ├── test_layer1_bootstrap.py   # Layer1 loading, Lean kernel, Haskell compiler
│   └── test_local_repl_layer1.py # LocalREPL Layer1 tools
├── redux/                      # Redux state management tests
│   ├── __init__.py
│   ├── test_routing_slice.py       # Routing state updates, backend metrics
│   ├── test_verification_slice.py  # Layer1 state, theorem verification
│   └── test_verification_middleware.py # Layer1 loading coordination
├── agents/                      # Verification agents tests
│   ├── __init__.py
│   ├── test_verification_agent_factory.py # Agent creation (Autoformalization, Verifier, etc.)
│   └── test_verification_prompts.py       # Prompt content validation
├── integration/                 # Integration tests
│   ├── __init__.py
│   ├── test_backend_routing_flow.py       # Backend routing through RLM._subcall()
│   ├── test_environment_routing_flow.py    # Environment routing through RLM._subcall()
│   ├── test_combined_routing.py            # Combined backend + environment routing
│   └── test_layer1_verification_flow.py   # Layer1 verification flow
└── fixtures/                    # Test fixtures
    ├── __init__.py
    ├── backend_routing_config.yaml    # Sample backend routing config
    ├── environment_routing_config.yaml # Sample environment routing config
    └── sample_tasks.py              # Sample task descriptors and prompts
```

## Running Tests

### Prerequisites

Ensure you have the required dependencies installed:

```bash
pip install pytest pytest-cov pytest-mock
```

### Basic Usage

Run all tests from the project root:

```bash
pytest tests/
```

Run tests for a specific module:

```bash
pytest tests/routing/
pytest tests/environments/
pytest tests/redux/
pytest tests/agents/
pytest tests/integration/
```                                                                                                             

Run a specific test file:

```bash
pytest tests/routing/test_backend_router.py
```

Run a specific test class:

```bash
pytest tests/routing/test_backend_router.py::TestBackendRouterInitialization
```

Run a specific test:

```bash
pytest tests/routing/test_backend_router.py::TestBackendRouterInitialization::test_init_with_default_config
```

### Running with Coverage

Generate a coverage report:

```bash
pytest --cov=rlm --cov-report=html tests/
```

View the coverage report:

```bash
open htmlcov/index.html
```

### Running Specific Test Categories

Run only unit tests:

```bash
pytest -m unit tests/
```

Run only integration tests:

```bash
pytest -m integration tests/
```

Run only slow tests:

```bash
pytest -m slow tests/
```

Run only Layer1 tests:

```bash
pytest -m layer1 tests/
```

### Running with Verbose Output

See detailed test output:

```bash
pytest -v tests/
```

See even more detailed output with print statements:

```bash
pytest -v -s tests/
```

### Running with Logging

Enable logging output:

```bash
pytest --log-cli-level=INFO tests/
```

## Test Organization

### Routing Layer Tests

Tests for routing components:

- **test_backend_router.py**: Tests YAML config loading, route matching, metrics tracking, adaptive overrides
- **test_backend_factory.py**: Tests backend client creation, ID mapping to ClientBackend, config merging
- **test_environment_router.py**: Tests environment rule matching, security constraint checking, capability-based routing
- **test_environment_factory.py**: Tests environment instance creation, ID mapping to EnvironmentType
- **test_task_descriptor.py**: Tests intent classification, complexity estimation, capability detection

### Layer1 Environment Tests

Tests for Layer1 components:

- **test_layer1_bootstrap.py**: Tests Layer1 loading, Lean kernel initialization, Haskell compiler setup, error handling
- **test_local_repl_layer1.py**: Tests LocalREPL Layer1 tools (verify_lean, check_haskell_types, get_layer1_axioms, prove_theorem)

### Redux State Management Tests

Tests for Redux components:

- **test_routing_slice.py**: Tests routing state updates, backend metrics tracking, routing decisions
- **test_verification_slice.py**: Tests Layer1 state, theorem verification tracking, verification queue
- **test_verification_middleware.py**: Tests Layer1 loading coordination, theorem verification orchestration

### Verification Agents Tests

Tests for verification agents:

- **test_verification_agent_factory.py**: Tests Autoformalization, Verifier, Physicist, Cross-check agent creation
- **test_verification_prompts.py**: Tests prompt content validation, tool integration verification

### Integration Tests

End-to-end integration tests:

- **test_backend_routing_flow.py**: Tests complete backend routing flow through RLM._subcall()
- **test_environment_routing_flow.py**: Tests complete environment routing flow through RLM._subcall()
- **test_combined_routing.py**: Tests combined backend + environment routing
- **test_layer1_verification_flow.py**: Tests Layer1 verification flow (loading → verification → theorem proving)

## Test Patterns

### Test Class Organization

Tests are organized into classes by functionality:

```python
class TestComponentName:
    """Tests for ComponentName functionality."""

    def test_specific_behavior(self):
        """
        Test specific behavior description.

        Expected behavior:
        - Should do X
        - Should return Y
        """
        # Setup
        # Execute
        # Assert
```

### Test Naming Convention

Test names follow the pattern: `test_<functionality>_<scenario>`

- `test_init_with_default_config` - Test initialization with default config
- `test_route_simple_task` - Test routing a simple task
- `test_verify_lean_success` - Test successful Lean verification
- `test_layer1_loading_failure` - Test Layer1 loading failure

### Mocking Pattern

Tests use the MockLM pattern for testing without real LLM calls:

```python
from tests.mock_lm import MockLM, MockLMWithResponse

def test_with_mock_lm():
    """Test using MockLM."""
    mock_lm = MockLM()
    response = mock_lm.completion("test prompt")
    assert "Mock response" in response
```

### Setup/Teardown Pattern

Tests follow the pattern: setup → execute → assert → cleanup

```python
def test_with_cleanup():
    """Test with proper cleanup."""
    # Setup
    router = BackendRouter()
    
    try:
        # Execute
        route = router.route(task)
        assert route is not None
    finally:
        # Cleanup
        router.cleanup()
```

### Assert Statements

Assert statements include descriptive failure messages:

```python
assert route.backend_id == "claude_agent", \
    "Should route to claude_agent for proof synthesis"

assert result["success"] is True, \
    "Layer1 loading should succeed"
```

## Debugging Guidelines

### Using Pytest Markers

Use markers to categorize tests:

```python
import pytest

@pytest.mark.unit
def test_unit_test():
    """Unit test."""
    pass

@pytest.mark.integration
def test_integration_test():
    """Integration test."""
    pass

@pytest.mark.slow
def test_slow_test():
    """Slow test."""
    pass

@pytest.mark.layer1
def test_layer1_test():
    """Layer1 test."""
    pass
```

### Using Caplog for Logging

Use the caplog fixture to capture log output:

```python
def test_with_logging(caplog):
    """Test with logging verification."""
    import logging
    
    # Execute code that logs
    with caplog.at_level(logging.INFO):
        # Code under test
    
    # Verify logs
    assert "Expected message" in caplog.text
```

### Using PDB for Debugging

Drop into PDB on test failure:

```bash
pytest --pdb tests/
```

### Using Breakpoints

Add breakpoints in tests for debugging:

```python
def test_with_breakpoint():
    """Test with breakpoint."""
    # Set breakpoint
    breakpoint()  # Python 3.7+
    
    # Test code
    result = function_under_test()
    assert result is not None
```

## Fixtures

### Available Fixtures

The `conftest.py` file provides shared fixtures:

- `test_data_dir`: Path to test fixtures directory
- `temp_dir`: Temporary directory for test files
- `mock_config_path`: Path to a mock configuration file
- `simple_task_descriptor`: Simple task descriptor for testing
- `complex_task_descriptor`: Complex task descriptor for testing
- `task_descriptor_dict`: Task descriptor as a dictionary
- `backend_router`: BackendRouter instance with test config
- `backend_factory`: BackendFactory instance with test configs
- `environment_router`: EnvironmentRouter instance with test config
- `environment_factory`: EnvironmentFactory instance with test configs
- `initial_routing_state`: Initial RoutingState
- `routing_state_with_metrics`: RoutingState with sample metrics
- `initial_verification_state`: Initial VerificationState
- `verification_state_loaded`: VerificationState with Layer1 loaded
- `verification_state_with_theorems`: VerificationState with sample theorems
- `mock_layer1_bootstrap`: Layer1Bootstrap instance with mocked dependencies
- `mock_parent_rlm`: Mock parent RLM instance
- `mock_lm`: MockLM instance
- `mock_lm_with_responses`: MockLMWithResponse instance
- `mock_lean_kernel`: Mock Lean kernel for testing
- `mock_haskell_compiler`: Mock Haskell compiler for testing
- `caplog_with_level`: Caplog fixture with INFO level

### Using Fixtures

Use fixtures in tests:

```python
def test_with_fixture(mock_parent_rlm: MagicMock):
    """Test using mock_parent_rlm fixture."""
    factory = VerificationAgentFactory(parent_rlm=mock_parent_rlm)
    agent = factory.create_verifier_agent("layer2/theorem1.lean")
    assert agent is not None
```

## Test Coverage

### Coverage Goals

The test suite aims to provide comprehensive coverage for:

1. **Happy Path**: Normal operation scenarios
2. **Edge Cases**: Boundary conditions and extreme values
3. **Error Handling**: Invalid inputs, failures, exceptions
4. **Configuration**: Loading/parsing of YAML configs
5. **State Transitions**: Redux state changes through actions
6. **Integration**: End-to-end workflows across components

### Running Coverage Report

Generate coverage report:

```bash
pytest --cov=rlm --cov-report=term-missing tests/
```

View missing coverage:

```bash
pytest --cov=rlm --cov-report=html tests/
open htmlcov/index.html
```

## Troubleshooting

### Common Issues

#### Import Errors

If you encounter import errors:

```bash
# Make sure you're running from the project root
cd /path/to/Self_AI
pytest tests/
```

#### Fixture Not Found

If a fixture is not found:

```bash
# Check that conftest.py is in the tests/ directory
ls tests/conftest.py

# Check that fixtures are properly defined
grep -n "^def " tests/conftest.py
```

#### Mock Not Working

If mocks aren't being applied:

```bash
# Check patch decorators are correct
# Use full import paths in patches
@patch('rlm.routing.backend_router.BackendRouter.route')
```

#### Test Isolation

If tests are interfering with each other:

```bash
# Run tests in isolation
pytest --forked tests/

# Or run tests one at a time
pytest -x tests/
```

### Getting Help

For more pytest options:

```bash
pytest --help
```

For pytest markers:

```bash
pytest --markers
```

## Best Practices

1. **Write Clear Test Names**: Test names should clearly describe what is being tested
2. **Use Docstrings**: Each test should have a docstring explaining its purpose
3. **Add Comments**: Complex logic should be explained with comments
4. **Use Descriptive Asserts**: Assert messages should explain expected vs actual
5. **Clean Up Resources**: Always clean up resources in teardown
6. **Use Appropriate Fixtures**: Reuse fixtures instead of duplicating setup code
7. **Mock External Dependencies**: Use mocks for LLM clients, file system, etc.
8. **Test Both Success and Failure**: Test both happy path and error scenarios
9. **Keep Tests Independent**: Each test should be able to run independently
10. **Avoid Test Order Dependencies**: Tests should not depend on execution order

## Contributing

When adding new tests:

1. Follow the existing test structure and patterns
2. Use descriptive test names and docstrings
3. Include both happy path and error cases
4. Add fixtures to conftest.py if they're reusable
5. Update this README with new test descriptions
6. Ensure tests pass before committing

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```bash
# Run all tests
pytest tests/ --junitxml=results.xml

# Run with coverage
pytest tests/ --cov=rlm --cov-report=xml --junitxml=results.xml
```

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Python unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [RLM Documentation](../../README.md)
