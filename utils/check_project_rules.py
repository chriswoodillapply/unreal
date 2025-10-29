"""
Pre-commit validation script

Checks that project rules are being followed:
1. No .md files in root (except README.md and PROJECT_RULES.md)
2. No test_*.py files in root
3. All tests are in tests/ directory
4. All docs are in docs/ directory

Usage:
    python check_project_rules.py
    
Returns:
    0 if all rules pass
    1 if any rule violations found
"""

import sys
from pathlib import Path
from typing import List, Tuple

# Color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'


def check_documentation_files() -> Tuple[bool, List[str]]:
    """Check for .md files in wrong locations"""
    violations = []
    
    # Allowed files in root
    allowed_root_files = {'README.md', 'PROJECT_RULES.md'}
    
    # Check root directory for .md files
    root_md_files = [f for f in Path('.').glob('*.md') if f.is_file()]
    
    for md_file in root_md_files:
        if md_file.name not in allowed_root_files:
            violations.append(
                f"Documentation file in root: {md_file.name}\n"
                f"  → Should be in docs/{md_file.name}"
            )
    
    # Check non-docs directories for .md files
    exclude_dirs = {'docs', 'venv', '.git', '__pycache__', '.pytest_cache', 'htmlcov', 'archive', 'node_modules'}
    
    for md_file in Path('.').rglob('*.md'):
        if not md_file.is_file():
            continue
            
        # Skip if in docs/ or excluded directories
        parts = md_file.parts
        if any(excluded_dir in parts for excluded_dir in exclude_dirs):
            continue
        
        # Root files already checked above
        if len(parts) == 1:
            continue
        
        # env_setup/README.md is allowed (setup-specific docs)
        if md_file.parts == ('env_setup', 'README.md'):
            continue
        
        # Check if it's not in docs/
        if 'docs' not in parts:
            violations.append(
                f"Documentation file outside docs/: {md_file}\n"
                f"  → Should be in docs/{md_file.name}"
            )
    
    return len(violations) == 0, violations
    
    return len(violations) == 0, violations


def check_test_files() -> Tuple[bool, List[str]]:
    """Check for test files in wrong locations"""
    violations = []
    
    # Check root directory for test_*.py files
    root_test_files = [f for f in Path('.').glob('test_*.py') if f.is_file()]
    
    for test_file in root_test_files:
        violations.append(
            f"Ad-hoc test script in root: {test_file.name}\n"
            f"  → Should be in tests/{test_file.name} as proper pytest unit test"
        )
    
    # Check non-test directories for test_*.py files
    exclude_dirs = {'tests', 'venv', '.git', '__pycache__', '.pytest_cache', 'archive', 'examples', 'node_modules'}
    
    for test_file in Path('.').rglob('test_*.py'):
        if not test_file.is_file():
            continue
            
        # Skip if in tests/ or excluded directories
        parts = test_file.parts
        if any(excluded_dir in parts for excluded_dir in exclude_dirs):
            continue
        
        # Not in tests/ directory
        if 'tests' not in parts:
            violations.append(
                f"Test file outside tests/: {test_file}\n"
                f"  → Should be in tests/{test_file.name}"
            )
    
    return len(violations) == 0, violations


def main():
    """Run all rule checks"""
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}Project Rules Validation{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")
    
    all_passed = True
    
    # Check documentation files
    print(f"{BOLD}📚 Checking documentation files...{RESET}")
    docs_passed, docs_violations = check_documentation_files()
    
    if docs_passed:
        print(f"{GREEN}✓ All documentation files in correct location{RESET}\n")
    else:
        print(f"{RED}✗ Documentation rule violations:{RESET}\n")
        for violation in docs_violations:
            print(f"  {RED}{violation}{RESET}\n")
        all_passed = False
    
    # Check test files
    print(f"{BOLD}🧪 Checking test files...{RESET}")
    tests_passed, test_violations = check_test_files()
    
    if tests_passed:
        print(f"{GREEN}✓ All test files in correct location{RESET}\n")
    else:
        print(f"{RED}✗ Test file rule violations:{RESET}\n")
        for violation in test_violations:
            print(f"  {RED}{violation}{RESET}\n")
        all_passed = False
    
    # Summary
    print(f"{BOLD}{'='*60}{RESET}")
    if all_passed:
        print(f"{GREEN}{BOLD}✓ All project rules passed!{RESET}\n")
        return 0
    else:
        print(f"{RED}{BOLD}✗ Project rule violations found{RESET}")
        print(f"\n{YELLOW}Fix violations by:{RESET}")
        print(f"  1. Moving .md files to docs/ folder")
        print(f"  2. Moving test_*.py files to tests/ as proper unit tests")
        print(f"\n{YELLOW}See PROJECT_RULES.md for details{RESET}\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
