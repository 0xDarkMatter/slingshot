# Contributing to CFWorker

Thank you for your interest in contributing to CFWorker! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect differing viewpoints and experiences

## How to Contribute

### Reporting Bugs

Before creating a bug report:
1. Check if the bug has already been reported in Issues
2. Verify you're using the latest version
3. Test with a clean environment

When reporting bugs, include:
- Python version (`python --version`)
- Operating system and version
- Steps to reproduce the issue
- Expected vs. actual behavior
- Error messages and stack traces
- Relevant configuration files (remove credentials!)

**Template:**
```markdown
**Environment:**
- Python version: 3.10.5
- OS: Ubuntu 22.04
- CFWorker version: 0.1.0

**Steps to Reproduce:**
1. Run `cfworker init test-worker`
2. Edit worker.js to...
3. Run `cfworker deploy`

**Expected:** Worker deploys successfully
**Actual:** Error: ...
**Error message:** ...
```

### Suggesting Features

Feature requests are welcome! Please:
1. Check if the feature has been suggested before
2. Explain the use case and benefit
3. Consider if it fits the project scope
4. Propose an API if applicable

### Contributing Code

#### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/CFWorker.git
   cd CFWorker
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv

   # Activate (Unix/Linux/macOS)
   source venv/bin/activate

   # Activate (Windows)
   venv\Scripts\activate
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

#### Making Changes

1. **Write Code**
   - Follow existing code style
   - Add type hints where applicable
   - Write docstrings for public functions/classes
   - Keep functions focused and testable

2. **Add Tests**
   - Write tests for new functionality
   - Update existing tests if behavior changes
   - Aim for good test coverage

   ```bash
   # Run tests
   pytest

   # With coverage
   pytest --cov=cfworker --cov-report=html
   ```

3. **Format Code**
   ```bash
   # Format with black
   black src/cfworker/ tests/

   # Check style with ruff
   ruff check src/cfworker/ tests/

   # Auto-fix style issues
   ruff check --fix src/cfworker/ tests/
   ```

4. **Update Documentation**
   - Update README.md if adding features
   - Update CHANGELOG.md following Keep a Changelog format
   - Add docstrings to new code
   - Update examples if needed

#### Commit Guidelines

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

**Examples:**
```bash
feat(cli): add worker logs command
fix(client): handle network timeouts properly
docs(readme): add security best practices section
test(config): add tests for validation logic
refactor(deployer): extract metadata preparation
```

#### Pull Request Process

1. **Before Submitting**
   - [ ] Tests pass: `pytest`
   - [ ] Code formatted: `black src/ tests/`
   - [ ] Linting passes: `ruff check src/ tests/`
   - [ ] Documentation updated
   - [ ] CHANGELOG.md updated

2. **Create Pull Request**
   - Use a clear, descriptive title
   - Reference related issues: `Fixes #123`
   - Describe changes and motivation
   - Include test coverage details
   - Add screenshots for UI changes (if applicable)

3. **PR Template:**
   ```markdown
   ## Description
   Brief description of changes

   ## Motivation
   Why is this change needed?

   ## Changes Made
   - Added feature X
   - Fixed bug Y
   - Updated documentation Z

   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Manual testing performed
   - [ ] Tests pass locally

   ## Checklist
   - [ ] Code follows project style
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] CHANGELOG.md updated
   ```

4. **After Submission**
   - Respond to feedback promptly
   - Make requested changes
   - Keep the PR up to date with main branch

## Development Guidelines

### Code Style

**Python Style:**
- Follow PEP 8
- Use Black formatter (100 char line length)
- Use Ruff for linting
- Add type hints for function signatures
- Use descriptive variable names

**Example:**
```python
from typing import Optional, Dict, Any

def deploy_worker(
    worker_name: str,
    script_content: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Deploy a worker script to Cloudflare.

    Args:
        worker_name: Name of the worker to deploy
        script_content: JavaScript/TypeScript worker code
        metadata: Optional metadata (bindings, vars, etc.)

    Returns:
        Deployment result dictionary

    Raises:
        DeploymentError: If deployment fails
    """
    # Implementation
    pass
```

### Testing

**Test Organization:**
- Place tests in `tests/` directory
- Mirror source structure: `src/cfworker/client.py` → `tests/test_client.py`
- Use pytest fixtures for common setup
- Mock external APIs (use `responses` library)

**Test Naming:**
```python
def test_config_load_success():
    """Test successful configuration loading."""
    pass

def test_config_load_missing_file():
    """Test loading nonexistent config file."""
    pass

def test_client_upload_worker_with_metadata():
    """Test worker upload with custom metadata."""
    pass
```

**Coverage Goals:**
- Aim for >80% code coverage
- Test happy paths and error conditions
- Test edge cases and boundary conditions

### Security

**When contributing:**
- Never commit real credentials
- Sanitize error messages (no credential leaks)
- Validate all user inputs
- Set restrictive file permissions for sensitive data
- Use secure defaults

**Security Review Checklist:**
- [ ] No hardcoded credentials
- [ ] Input validation present
- [ ] Error messages sanitized
- [ ] File permissions set correctly
- [ ] Dependencies up to date

### Documentation

**Docstrings:**
- Use Google style docstrings
- Document all parameters and return values
- Include examples for complex functions
- Document exceptions that can be raised

**README Updates:**
- Add new features to feature list
- Update examples if API changes
- Update installation if dependencies change
- Add troubleshooting entries for common issues

**CHANGELOG:**
- Add entry under `[Unreleased]`
- Use categories: Added, Changed, Deprecated, Removed, Fixed, Security
- Be specific about what changed
- Reference PR/issue numbers

## Project Structure

```
CFWorker/
├── src/cfworker/          # Source code
│   ├── __init__.py        # Package initialization
│   ├── cli.py             # CLI commands
│   ├── client.py          # Cloudflare API client
│   ├── config.py          # Configuration management
│   ├── deployer.py        # Deployment logic
│   └── py.typed           # Type hint marker
├── tests/                 # Test suite
│   ├── conftest.py        # Shared fixtures
│   ├── test_cli.py        # CLI tests
│   ├── test_client.py     # Client tests
│   ├── test_config.py     # Config tests
│   └── test_deployer.py   # Deployer tests
├── templates/             # Worker templates
├── examples/              # Example projects
├── .claude/agents/        # Claude Code agents
├── docs/                  # Additional documentation (future)
└── pyproject.toml         # Project configuration
```

### Module Responsibilities

- **cli.py**: User-facing CLI commands, Click interface, output formatting
- **client.py**: Cloudflare API wrapper, HTTP requests, error handling
- **config.py**: Configuration loading/saving, validation, environment variables
- **deployer.py**: Deployment orchestration, script bundling, metadata preparation

## Release Process

(For maintainers)

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md:
   - Move `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD`
   - Add comparison links
3. Create release commit: `chore: release vX.Y.Z`
4. Tag release: `git tag vX.Y.Z`
5. Push: `git push && git push --tags`
6. Create GitHub release from tag
7. Build and publish to PyPI (if applicable)

## Getting Help

- **Questions**: Open a Discussion on GitHub
- **Bugs**: Open an Issue with bug report template
- **Chat**: Join discussions in GitHub Discussions
- **Docs**: Check README.md and QUICKSTART.md

## Recognition

Contributors will be:
- Listed in GitHub's contributor graph
- Mentioned in release notes for significant contributions
- Appreciated and thanked! 🙏

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to CFWorker! Your help makes this project better for everyone. 🚀
