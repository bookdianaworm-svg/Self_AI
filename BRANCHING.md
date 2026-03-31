# Branching Strategy for Self_AI Project

## Overview

This project uses a feature-based branching strategy with clear separation of concerns, enabling parallel development of multiple complex features while maintaining code quality and stability.

## Branch Structure

### Primary Branches

- **main** - Production-ready code. Only stable, tested code is merged here.
- **develop** - Integration branch for features. All completed features are merged here for testing and integration.

### Feature Branches

Feature branches are created from `develop` and named with the `feature/` prefix:

- **feature/redux-state-management** - Redux store implementation with slices for agents, tasks, messages, system state, tools, and improvements
- **feature/agent-framework** - Base agent classes and specialized agent implementations
- **feature/swarm-orchestration** - Main swarm instance with continuous spawning and coordination
- **feature/messaging-system** - Shared messaging infrastructure with request-response, broadcast, and pub-sub patterns
- **feature/dynamic-tools** - Tool creation, registry, and sharing system with approval workflow
- **feature/verification-system** - Lean 4 axiomatic seed integration for verification
- **feature/backend-diversity** - Multi-backend routing and environment selection
- **feature/visualization-interface** - Real-time monitoring UI with agent grid, communication log, and system metrics
- **feature/self-improvement** - Improvement contribution system with approval and application
- **feature/testing-infrastructure** - Test framework, CI/CD pipelines, and automated testing

### Legacy Branches

- **general-caravel** - Legacy branch (to be removed after migration)
- **test-feature** - Legacy branch (to be removed after migration)

## Branch Naming Conventions

- **feature/*** - New features and functionality
- **bugfix/*** - Bug fixes that don't affect existing features
- **hotfix/*** - Emergency fixes for production issues
- **release/*** - Release preparation and versioning

## Workflow

### Feature Development

1. Create a feature branch from `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. Make commits to your feature branch with clear, descriptive messages

3. Push the branch to remote:
   ```bash
   git push -u origin feature/your-feature-name
   ```

4. Create a Pull Request to `develop`

5. Code review and testing

6. Merge to `develop` after approval

### Integration to Main

1. When `develop` is stable and all features are tested:
   ```bash
   git checkout main
   git pull origin main
   git merge develop
   git push origin main
   ```

2. Create a release tag:
   ```bash
   git tag -a v0.1.0 -m "Release version 0.1.0"
   git push origin v0.1.0
   ```

### Hotfix Workflow

1. Create hotfix branch from `main`:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/your-hotfix
   ```

2. Implement the fix

3. Merge to both `main` AND `develop`:
   ```bash
   git checkout main
   git merge hotfix/your-hotfix
   git push origin main
   
   git checkout develop
   git merge hotfix/your-hotfix
   git push origin develop
   ```

## Branch Protection Rules

### Main Branch
- Require pull request reviews before merging
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Restrict who can push to this branch
- Require conversation resolution before merging

### Develop Branch
- Require pull request reviews before merging
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Do not restrict direct pushes (for flexibility)

## Feature Dependencies

Some features have dependencies on others:

1. **feature/swarm-orchestration** depends on:
   - feature/redux-state-management
   - feature/agent-framework
   - feature/messaging-system

2. **feature/visualization-interface** depends on:
   - feature/redux-state-management
   - feature/messaging-system

3. **feature/self-improvement** depends on:
   - feature/dynamic-tools
   - feature/messaging-system

4. **feature/verification-system** depends on:
   - feature/agent-framework

When working with dependent features:
- Wait for upstream features to be merged to `develop`
- Rebase your branch on `develop` periodically:
  ```bash
  git checkout feature/your-feature
  git rebase develop
  ```

## Commit Message Guidelines

Follow these guidelines for commit messages:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes (formatting, etc.)
- refactor: Code refactoring
- test: Adding or updating tests
- chore: Maintenance tasks

**Example:**
```
feat(agent-framework): add TaskProcessingAgent class

- Implemented base agent lifecycle management
- Added task execution with RLM integration
- Included agent-to-agent messaging support

Closes #123
```

## Code Review Process

1. **Self-Review**: Review your own PR before requesting reviews
2. **Automated Checks**: Ensure all CI/CD checks pass
3. **Review Assignment**: Assign at least one reviewer
4. **Review Criteria**:
   - Code quality and style
   - Test coverage
   - Documentation updates
   - Performance implications
   - Security considerations
5. **Approval**: At least one approval required to merge
6. **Resolution**: All review comments must be addressed

## Continuous Integration

All branches trigger CI/CD pipelines that:
- Run linters and formatters
- Execute test suites
- Check code coverage
- Build artifacts
- Run security scans

## Cleanup

Delete merged branches regularly:

```bash
# Delete local merged branches
git branch --merged | grep -E "feature/|bugfix/" | xargs git branch -d

# Delete remote merged branches
git remote prune origin
```

## Release Process

1. Finalize features in `develop`
2. Create release branch: `git checkout -b release/v0.1.0 develop`
3. Update version numbers and changelog
4. Merge to `main`: `git checkout main && git merge release/v0.1.0`
5. Tag release: `git tag -a v0.1.0 -m "Release v0.1.0"`
6. Back-merge to `develop`: `git checkout develop && git merge release/v0.1.0`
7. Push all: `git push origin main develop && git push origin v0.1.0`

## Questions?

For questions about this branching strategy, please refer to:
- GitFlow documentation
- Project team guidelines
- GitHub issues for specific questions
