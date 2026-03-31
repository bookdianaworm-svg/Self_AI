# Development Workflow Setup Guide

## Quick Start

This guide will help you set up the professional development workflow for the Self_AI project.

## Prerequisites

1. Git installed and configured
2. GitHub account
3. Project cloned locally

## Branch Structure Overview

Your repository now has the following professional branching structure:

### Primary Branches
- **main** - Production-ready code (renamed from master)
- **develop** - Integration branch for features

### Feature Branches (created from develop)
- `feature/redux-state-management` - Redux store implementation
- `feature/agent-framework` - Base agent classes
- `feature/swarm-orchestration` - Swarm orchestration
- `feature/messaging-system` - Messaging infrastructure
- `feature/dynamic-tools` - Tool creation system
- `feature/verification-system` - Lean 4 verification
- `feature/backend-diversity` - Multi-backend routing
- `feature/visualization-interface` - Monitoring UI
- `feature/self-improvement` - Improvement system
- `feature/testing-infrastructure` - Test framework

## Creating the GitHub Repository

### Option 1: Manual Setup (Recommended for learning)

1. Go to GitHub.com
2. Click "+" → "New repository"
3. Repository name: `Self_AI` (or your preferred name)
4. Description: "Self-Improving Swarm System with RLM Framework"
5. Visibility: Private (recommended for this project)
6. **Do NOT** initialize with README, .gitignore, or license (already exists)
7. Click "Create repository"
8. Follow the instructions to push your existing local repository

### Option 2: Automated Setup

Provide the following information to have Kilo create the repository:
- Your GitHub username
- Preferred repository name (default: `Self_AI`)
- Public or private (default: private)

## Pushing Branches to GitHub

After creating the repository on GitHub, push your branches:

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/Self_AI.git

# Push main branch
git push -u origin main

# Push develop branch
git push -u origin develop

# Push all feature branches
git push -u origin feature/redux-state-management
git push -u origin feature/agent-framework
git push -u origin feature/swarm-orchestration
git push -u origin feature/messaging-system
git push -u origin feature/dynamic-tools
git push -u origin feature/verification-system
git push -u origin feature/backend-diversity
git push -u origin feature/visualization-interface
git push -u origin feature/self-improvement
git push -u origin feature/testing-infrastructure

# Push all branches at once (after pushing main first)
git push -u origin --all
```

## Setting Up Branch Protection

### Main Branch Protection

1. Go to repository → Settings → Branches
2. Click "Add rule"
3. Branch name pattern: `main`
4. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (1)
   - ✅ Dismiss stale PR approvals when new commits are pushed
   - ✅ Require branches to be up to date before merging
   - ✅ Require status checks to pass before merging (set up checks first)
   - ✅ Require conversation resolution before merging
5. Restrict who can push:
   - ✅ Only allow maintainers to push

### Develop Branch Protection

1. Click "Add rule"
2. Branch name pattern: `develop`
3. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (1)
   - ✅ Dismiss stale PR approvals when new commits are pushed
   - ✅ Require branches to be up to date before merging
   - ✅ Require status checks to pass before merging
6. Do NOT restrict pushes (allow direct pushes)

## Setting Up CI/CD

### Recommended Actions

Create `.github/workflows/` directory and add these workflows:

1. **`.github/workflows/test.yml`** - Run tests on every push
2. **`.github/workflows/lint.yml`** - Run linters on every push
3. **`.github/workflows/schedule.yml`** - Scheduled maintenance tasks

Example test workflow:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop, feature/** ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/
```

## Development Workflow

### Starting a New Feature

```bash
# 1. Update develop
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Make changes and commit
git add .
git commit -m "feat(scope): description of changes"

# 4. Push to remote
git push -u origin feature/your-feature-name

# 5. Create Pull Request on GitHub
```

### Working on Existing Feature

```bash
# 1. Switch to feature branch
git checkout feature/your-feature-name

# 2. Update from develop periodically
git fetch origin develop
git rebase origin/develop

# 3. Continue development
git add .
git commit -m "feat(scope): more changes"

# 4. Push
git push origin feature/your-feature-name
```

## Review Process

### Pull Request Checklist

Before requesting review:
- [ ] Code compiles and runs without errors
- [ ] All tests pass locally
- [ ] Added tests for new functionality
- [ ] Updated documentation
- [ ] Followed commit message guidelines
- [ ] No sensitive data committed
- [ ] Code style matches project standards

### Reviewer Checklist

When reviewing a PR:
- [ ] Code quality is acceptable
- [ ] Tests are adequate and passing
- [ ] Documentation is updated
- [ ] No obvious bugs or security issues
- [ ] Performance considerations addressed
- [ ] Edge cases handled

## Code Quality Tools

### Recommended Tools

1. **Black** - Code formatting
   ```bash
   pip install black
   black rlm/
   ```

2. **Flake8** - Linting
   ```bash
   pip install flake8
   flake8 rlm/
   ```

3. **pylint** - Code analysis
   ```bash
   pip install pylint
   pylint rlm/
   ```

4. **mypy** - Type checking
   ```bash
   pip install mypy
   mypy rlm/
   ```

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Run black
black --check rlm/
# Run flake8
flake8 rlm/
# Run tests
pytest tests/ -q
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Documentation

Update these files as needed:
- `README.md` - Project overview and quick start
- `BRANCHING.md` - Branching strategy (already created)
- `DEVELOPMENT.md` - Development guidelines (create this)
- `API.md` - API documentation (create when API is stable)
- `CONTRIBUTING.md` - Contribution guidelines (create this)

## Issue Tracking

Use GitHub Issues to track:
- Bugs with steps to reproduce
- Feature requests with use cases
- Questions and discussions
- Tasks and milestones

Issue labels:
- `bug` - Bug reports
- `enhancement` - Feature requests
- `documentation` - Documentation issues
- `good first issue` - Beginner-friendly tasks
- `help wanted` - Community contributions welcome
- `wontfix` - Issues that won't be addressed

## Next Steps

1. ✓ Branches created locally
2. ⏳ Create GitHub repository
3. ⏳ Push branches to remote
4. ⏳ Set up branch protection rules
5. ⏳ Set up CI/CD workflows
6. ⏳ Create team and assign maintainers
7. ⏳ Start development on first feature

## Questions?

Refer to:
- `BRANCHING.md` - Detailed branching strategy
- Git documentation - Git commands and workflows
- GitHub documentation - GitHub features and best practices

Need help? Ask in GitHub Issues or contact the project maintainers.
