# Project Rules - READ THIS FIRST! ⚠️

## 🚨 IMPORTANT: Development Rules

Before creating any files, read these rules:

### Rule 1: Documentation Files → `docs/` folder ONLY

❌ **NEVER** create `.md` files in the project root (except README.md)  
✅ **ALWAYS** create documentation in `docs/` folder

```bash
# Wrong
scripts/MY_GUIDE.md

# Correct  
scripts/docs/MY_GUIDE.md
```

### Rule 2: Test Files → `tests/` folder as pytest unit tests ONLY

❌ **NEVER** create ad-hoc test scripts like `test_*.py` in root  
✅ **ALWAYS** create proper pytest unit tests in `tests/` folder

```bash
# Wrong
scripts/test_my_feature.py
scripts/quick_test.py

# Correct
scripts/tests/test_my_feature.py
```

## 📚 Full Guidelines

Read the complete guidelines here:
- **[DEVELOPMENT_GUIDELINES.md](docs/DEVELOPMENT_GUIDELINES.md)** ← **REQUIRED READING**
- **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** ← Before contributing

## 🔍 Quick Check

Before committing, verify:

```bash
# No docs in root (except README.md)
find . -maxdepth 1 -name "*.md" ! -name "README.md" ! -name "PROJECT_RULES.md"

# No ad-hoc tests in root  
find . -maxdepth 1 -name "test_*.py"

# Both should return nothing
```

## 📁 Correct File Locations

| File Type | Location |
|-----------|----------|
| Documentation (*.md) | `docs/` |
| Tests (test_*.py) | `tests/` |
| Examples | `examples/` |
| Utils | `utils/` |
| Setup scripts | `env_setup/` |

---

**Last Updated**: October 29, 2025
