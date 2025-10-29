# Contributing Guidelines

Thank you for considering contributing to the Unreal Python Remote Control project!

## 📋 Quick Rules

Before contributing, please follow these guidelines:

### 1. 📚 Documentation Rules

**✅ DO**: Store all documentation in the `docs/` folder

```bash
# Correct
docs/MY_NEW_GUIDE.md

# Wrong
scripts/MY_NEW_GUIDE.md
```

**Exception**: Only `README.md` is allowed in the project root.

### 2. 🧪 Testing Rules

**✅ DO**: Create all tests as pytest unit tests in the `tests/` folder

```bash
# Correct
tests/test_my_feature.py

# Wrong
scripts/test_my_feature.py
scripts/quick_test.py
```

**Never create ad-hoc test scripts.** Use proper pytest conventions.

For detailed guidelines, see [DEVELOPMENT_GUIDELINES.md](DEVELOPMENT_GUIDELINES.md)

---

## 🚀 Getting Started

### 1. Setup Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd scripts

# Setup Python environment
env_setup\setup_python_env.bat

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Unreal Project

```bash
# Setup Unreal project for remote execution
env_setup\setup_unreal_remote.bat "C:\Path\To\Project.uproject"
```

### 3. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Verify all tests pass before making changes
```

---

## 📝 Making Changes

### Adding New Features

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Write your code**:
   - Follow existing code structure
   - Add type hints where appropriate
   - Include docstrings for public APIs

3. **Write tests** in `tests/`:
   ```python
   # tests/test_my_feature.py
   import pytest
   from unreallib import my_feature
   
   def test_my_new_feature():
       """Test my new feature works correctly"""
       result = my_feature.do_something()
       assert result is not None
   ```

4. **Add documentation** in `docs/`:
   ```bash
   # Create documentation
   docs/MY_FEATURE_GUIDE.md
   
   # Update root README.md to link to it
   ```

5. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

6. **Update examples** if needed:
   ```python
   # examples/demo_my_feature.py
   """Demonstration of my new feature"""
   from unreallib import my_feature
   
   result = my_feature.do_something()
   print(f"Result: {result}")
   ```

### Code Style

- **Python**: Follow PEP 8
- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Add type hints for function signatures
- **Imports**: Group imports (standard library, third-party, local)

Example:
```python
"""
Module description

This module provides functionality for...
"""

import sys
from pathlib import Path
from typing import Optional, List

import unreal

from unreallib import actors


def my_function(name: str, count: int = 5) -> List[str]:
    """
    Brief description of function
    
    Args:
        name: Description of name parameter
        count: Description of count parameter (default: 5)
    
    Returns:
        List of result strings
    
    Raises:
        ValueError: If count is negative
    """
    if count < 0:
        raise ValueError("Count must be non-negative")
    
    return [f"{name}_{i}" for i in range(count)]
```

---

## 🧪 Testing Guidelines

### Test Structure

All tests must be in `tests/` directory and follow pytest conventions:

```python
# tests/test_feature.py
"""
Unit tests for feature module
"""

import pytest
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unreallib import feature


class TestFeature:
    """Tests for Feature class"""
    
    def test_basic_case(self):
        """Test basic functionality"""
        result = feature.do_something()
        assert result is not None
    
    def test_edge_case(self):
        """Test edge case"""
        with pytest.raises(ValueError):
            feature.do_invalid()


def test_helper_function():
    """Test standalone helper function"""
    assert feature.helper(1, 2) == 3
```

### Test Categories

- **Unit Tests**: `test_*.py` - Test individual components
- **Integration Tests**: `test_integration_*.py` - Test complete workflows

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_my_feature.py -v

# With coverage
pytest tests/ --cov=unreallib --cov=remotecontrol
```

### Test Requirements

- All new features must have tests
- Tests must pass before submitting PR
- Aim for >80% code coverage on new code
- Include both positive and negative test cases

---

## 📚 Documentation Guidelines

### Creating Documentation

1. **Create in `docs/` folder**:
   ```bash
   docs/MY_GUIDE.md
   ```

2. **Use clear headings and structure**:
   ```markdown
   # Feature Name
   
   Brief description
   
   ## Overview
   
   ## Usage
   
   ## Examples
   
   ## API Reference
   ```

3. **Link from root README.md**:
   ```markdown
   ## 📖 Documentation
   
   - **[Your New Guide](docs/MY_GUIDE.md)**
   ```

### Documentation Standards

- Use clear, concise language
- Include code examples
- Add usage scenarios
- Document all parameters and return values
- Include troubleshooting sections

---

## 🔄 Pull Request Process

### Before Submitting

1. **Run all tests**:
   ```bash
   pytest tests/ -v
   ```

2. **Check code style**:
   ```bash
   # Run linter if available
   pylint unreallib/ remotecontrol/
   ```

3. **Update documentation**:
   - Add/update docs in `docs/` folder
   - Update root README.md if needed
   - Add examples if appropriate

4. **Verify file locations**:
   ```bash
   # No docs in root (except README.md)
   find . -maxdepth 1 -name "*.md" ! -name "README.md"
   # Should return nothing
   
   # No ad-hoc tests in root
   find . -maxdepth 1 -name "test_*.py"
   # Should return nothing
   ```

### Submitting PR

1. **Create descriptive title**:
   - Good: "Add color manipulation tasks for workflow system"
   - Bad: "Fix stuff", "Updates"

2. **Write clear description**:
   ```markdown
   ## Changes
   - Added SetActorColorTask
   - Added ColorGridTask
   - Added materials.py utility module
   
   ## Testing
   - Added test_material_tasks.py with 15 tests
   - All tests passing (77/77)
   
   ## Documentation
   - Added docs/MATERIALS_GUIDE.md
   - Updated README.md with materials examples
   ```

3. **Reference related issues**:
   ```markdown
   Fixes #123
   Related to #456
   ```

4. **Wait for review**:
   - Respond to feedback
   - Make requested changes
   - Update tests and docs as needed

### PR Review Checklist

Reviewers will check:

- [ ] All tests in `tests/` directory
- [ ] All docs in `docs/` directory (except root README.md)
- [ ] Tests pass (`pytest tests/ -v`)
- [ ] Code follows style guidelines
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] No ad-hoc test scripts
- [ ] Examples updated if needed

---

## 🏗️ Project Structure

When adding files, follow this structure:

```
scripts/
├── README.md                   # Root readme only
├── DEVELOPMENT_GUIDELINES.md   # This file
├── CONTRIBUTING.md             # Contributing guide
│
├── docs/                       # ✅ All documentation
│   ├── README_CLEAN.md
│   └── [your-docs].md
│
├── tests/                      # ✅ All tests
│   ├── test_*.py              # Unit tests
│   └── test_integration_*.py  # Integration tests
│
├── examples/                   # User examples
│   └── [your-example].py
│
├── unreallib/                  # Main library
│   ├── actors.py
│   ├── level.py
│   ├── workflow/
│   └── tasks/
│
└── remotecontrol/             # Remote execution
    └── ...
```

---

## 🐛 Reporting Issues

### Bug Reports

Include:
- Python version
- Unreal Engine version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/logs

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative approaches considered
- Examples of usage

---

## 💬 Questions?

- Check [Documentation](docs/README_CLEAN.md)
- Check [Development Guidelines](DEVELOPMENT_GUIDELINES.md)
- Open an issue for questions

---

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on the code, not the person

---

Thank you for contributing! 🎉
