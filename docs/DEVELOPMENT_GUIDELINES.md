# Development Guidelines

## 📋 Project Standards

This document defines the standards and conventions for this project to maintain consistency and quality.

---

## 📚 Documentation Rules

### ✅ DO: Store all documentation in `docs/` folder

All markdown documentation files (*.md) must be placed in the `docs/` directory:

```
docs/
├── README_CLEAN.md          # Main documentation
├── QUICKSTART.md            # Quick start guide
├── QUICKSTART_UPYRC.md      # upyrc setup guide
├── TESTING_CHECKLIST.md     # Testing procedures
├── MIGRATION.md             # Migration guides
├── SETUP_CLEANUP.md         # Setup information
└── [your-new-doc].md        # Any new documentation
```

**Exception**: The root `README.md` is the only documentation file allowed in the project root.

### ❌ DON'T: Create documentation files in project root

```
❌ WRONG:
scripts/
├── MY_NEW_GUIDE.md          # Don't create here
├── SETUP_NOTES.md           # Don't create here
└── ARCHITECTURE.md          # Don't create here

✅ CORRECT:
scripts/
├── README.md                # Only this file allowed
└── docs/
    ├── MY_NEW_GUIDE.md      # Create here instead
    ├── SETUP_NOTES.md       # Create here instead
    └── ARCHITECTURE.md      # Create here instead
```

### Creating New Documentation

When creating new documentation:

1. **Create in `docs/` folder**:
   ```bash
   # Create new doc
   touch docs/MY_NEW_GUIDE.md
   ```

2. **Use descriptive names**:
   - Good: `API_REFERENCE.md`, `DEPLOYMENT_GUIDE.md`, `WORKFLOW_PATTERNS.md`
   - Bad: `notes.md`, `stuff.md`, `temp.md`

3. **Update root README.md** to link to new documentation:
   ```markdown
   ## 📖 Documentation
   
   - **[Complete Guide](docs/README_CLEAN.md)**
   - **[Your New Guide](docs/MY_NEW_GUIDE.md)** ← Add link
   ```

---

## 🧪 Testing Rules

### ✅ DO: Create all tests as unit tests in `tests/` folder

All test code must be created as proper pytest unit tests in the `tests/` directory:

```
tests/
├── test_client.py               # Client tests
├── test_config.py               # Configuration tests
├── test_workflow_graph.py       # Workflow graph tests
├── test_workflow_executor.py    # Workflow executor tests
├── test_integration_actors.py   # Integration tests
└── test_[your_feature].py       # Your new test file
```

### ❌ DON'T: Create ad-hoc test scripts

```
❌ WRONG:
scripts/
├── test_my_feature.py           # Don't create ad-hoc tests here
├── quick_test.py                # Don't create ad-hoc tests here
└── debug_test.py                # Don't create ad-hoc tests here

✅ CORRECT:
scripts/
├── tests/
│   └── test_my_feature.py       # Create proper unit test here
└── examples/
    └── demo_my_feature.py       # Or create example here
```

### Writing Proper Unit Tests

Follow pytest conventions:

```python
"""
tests/test_my_feature.py

Unit tests for my_feature module
"""

import pytest
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unreallib import my_feature


class TestMyFeature:
    """Tests for MyFeature functionality"""
    
    def test_basic_functionality(self):
        """Test basic feature works"""
        result = my_feature.do_something()
        assert result is not None
    
    def test_edge_case(self):
        """Test edge case handling"""
        with pytest.raises(ValueError):
            my_feature.do_invalid_thing()


def test_standalone_function():
    """Test standalone function"""
    assert my_feature.calculate(2, 2) == 4
```

### Test Categories

Organize tests by category:

1. **Unit Tests** (`test_*.py`):
   - Test individual functions/classes in isolation
   - No Unreal Engine required
   - Fast execution
   - Mock external dependencies

2. **Integration Tests** (`test_integration_*.py`):
   - Test components working together
   - May require Unreal Engine running
   - Slower execution
   - Test real workflows

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_my_feature.py -v

# Run specific test class
pytest tests/test_my_feature.py::TestMyFeature -v

# Run specific test function
pytest tests/test_my_feature.py::TestMyFeature::test_basic_functionality -v

# Run with coverage
pytest tests/ --cov=unreallib --cov=remotecontrol
```

### When to Use Examples vs Tests

| Use `examples/` | Use `tests/` |
|----------------|--------------|
| Demonstrating usage | Verifying functionality |
| User-facing demos | Developer validation |
| Tutorial code | Automated testing |
| Interactive scripts | CI/CD integration |

**Example Script** (for users):
```python
# examples/demo_my_feature.py
"""
Demonstration of MyFeature

Shows how to use the feature in a real scenario.
"""
from unreallib import my_feature

# Simple demo
result = my_feature.do_something()
print(f"Result: {result}")
```

**Unit Test** (for developers):
```python
# tests/test_my_feature.py
"""Unit tests for MyFeature"""
import pytest
from unreallib import my_feature

def test_do_something():
    """Verify do_something returns expected value"""
    result = my_feature.do_something()
    assert isinstance(result, str)
    assert len(result) > 0
```

---

## 🗂️ File Organization Rules

### Directory Structure

```
scripts/
├── README.md                    # Root readme only
├── setup.bat                    # Main setup script
├── config.py                    # Configuration
├── requirements.txt             # Dependencies
├── pytest.ini                   # Test configuration
│
├── docs/                        # ✅ All documentation here
│   ├── README_CLEAN.md
│   ├── QUICKSTART.md
│   └── ...
│
├── tests/                       # ✅ All tests here
│   ├── test_client.py
│   ├── test_workflow_*.py
│   └── test_integration_*.py
│
├── examples/                    # User-facing examples
│   ├── spawn_shapes.py
│   └── ...
│
├── utils/                       # Utility scripts
│   ├── count_actors.py
│   └── ...
│
├── env_setup/                   # Setup scripts
│   ├── README.md               # (Exception: setup-specific docs)
│   └── ...
│
├── remotecontrol/              # Remote control module
│   └── ...
│
└── unreallib/                  # Unreal library module
    └── ...
```

### What Goes Where

| File Type | Location | Purpose |
|-----------|----------|---------|
| `*.md` docs | `docs/` | All documentation |
| `test_*.py` | `tests/` | All unit/integration tests |
| `*.py` examples | `examples/` | User-facing demonstrations |
| `*.py` utils | `utils/` | Helper/utility scripts |
| `*.bat` setup | `env_setup/` | Setup/installation scripts |

---

## ⚠️ Enforcement

### Before Committing

Check your changes follow these rules:

```bash
# Check for misplaced documentation
find . -maxdepth 1 -name "*.md" ! -name "README.md"
# Should return nothing (or only README.md)

# Check for ad-hoc test scripts
find . -maxdepth 1 -name "test_*.py"
# Should return nothing

# Verify all tests are in tests/
ls tests/test_*.py
# Should show all test files
```

### Code Review Checklist

When reviewing pull requests, verify:

- [ ] All `*.md` files (except root README.md) are in `docs/`
- [ ] All `test_*.py` files are in `tests/` directory
- [ ] Tests follow pytest conventions (use `assert`, proper fixtures)
- [ ] No ad-hoc test scripts in root or other directories
- [ ] Examples are in `examples/` if intended for users
- [ ] New documentation is linked from root README.md

### Cleaning Up Violations

If you find files in wrong locations:

```bash
# Move misplaced documentation
mv MY_GUIDE.md docs/

# Move ad-hoc test to proper test file
# Either:
mv test_quick.py tests/test_feature.py  # If it's a real test
# Or:
mv test_quick.py examples/demo_feature.py  # If it's a demo
# Or:
mv test_quick.py archive/  # If it's obsolete
```

---

## 📝 Summary

### Golden Rules

1. **📚 Documentation → `docs/` folder**
   - Exception: Root `README.md` only
   - Link from root README.md

2. **🧪 Tests → `tests/` folder as pytest unit tests**
   - Never create ad-hoc test scripts
   - Use pytest conventions
   - Organize by test type (unit vs integration)

3. **📂 Everything has a place**
   - Examples → `examples/`
   - Utils → `utils/`
   - Setup → `env_setup/`
   - Tests → `tests/`
   - Docs → `docs/`

### Benefits

- **Consistency**: Everyone knows where to find things
- **Maintainability**: Clear organization makes updates easier
- **Discoverability**: New contributors can navigate easily
- **Professionalism**: Industry-standard structure
- **Automation**: CI/CD can reliably find tests and docs

---

## 🔗 Related Documentation

- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute
- [Testing Checklist](docs/TESTING_CHECKLIST.md) - Testing procedures
- [Project Structure](docs/README_CLEAN.md#-project-structure) - Full structure

---

**Last Updated**: October 29, 2025  
**Version**: 1.0
