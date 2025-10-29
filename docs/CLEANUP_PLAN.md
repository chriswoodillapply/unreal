# Scripts Cleanup Plan

## Summary
- **DELETE**: 35+ legacy debugging/testing files
- **MOVE**: 4 files to examples/
- **CONVERT**: 5 files to proper pytest integration tests
- **KEEP**: Core infrastructure (remotecontrol, unreallib, tests/, examples/)

## 1. DELETE - Legacy Debugging Files (35 files)

### Connection/Network Debugging (7 files)
```
test_connection.py
test_network.py
test_ports.py
test_direct_udp.py
test_handshake.py
test_plain.py
test_exact_format.py
```
**Reason**: These were temporary debugging scripts during upyrc setup. Connection is now stable.

### Import Debugging (8 files)
```
test_imports.py
test_config_import.py
test_init_imports.py
test_imports_to_file.py
test_reload.py
test_direct_config.py
test_config_syntax.py
test_python_version.py
```
**Reason**: Import issues are resolved. Module structure is stable.

### upyrc/Protocol Debugging (7 files)
```
test_upyrc.py
test_uprc_import.py
test_simple_upyre.py
test_upyre_working.py
test_command_types.py
test_types.py
test_file_command.py
```
**Reason**: upyrc integration is working via --method=file. These were exploratory tests.

### Deprecated WebRemoteControl (3 files)
```
test_webremote.py
test_remote_control.py
test_epic_client.py
```
**Reason**: UE 5.6 uses RemoteControl plugin, not WebRemoteControl. These don't apply.

### Duplicate/Obsolete Tests (10 files)
```
test_upsert_demo.py          # Duplicate of test_upsert_persistent.py
test_upsert_simple.py        # Duplicate of test_upsert_persistent.py
test_mode_config.py          # Superseded by test_upsert_config.py
test_multi_run_upsert.py     # Duplicate functionality
test_workflow_upsert.py      # Duplicate functionality
test_office_basic.py         # Has errors, superseded by test_unit_simple.py
test_basic_cubes.py          # Merge into examples
test_basic_spawn.py          # Merge into examples
test_workflow_direct.py      # Convert to proper test
test_simple_workflow.py      # Convert to proper test
```

## 2. MOVE TO examples/ (4 files)

Create comprehensive example files:

### examples/spawn_shapes.py (NEW - merge 3 files)
Merge: `test_spawn_three.py`, `test_basic_cubes.py`, `test_basic_spawn.py`
```python
"""
Examples of spawning basic shapes in Unreal
Demonstrates: spawn_cube, spawn_sphere, spawn_cylinder
"""
```

### examples/spawn_grid.py (RENAME)
From: `test_actors_module.py`
```python
"""
Example of spawning actor grids
Demonstrates: spawn_grid() with different shapes and configurations
"""
```

### Keep existing examples:
- `run_create_mode.py` - Runner for CREATE mode
- `run_upsert_mode.py` - Runner for UPSERT mode

## 3. CONVERT TO PROPER TESTS in tests/ (5 new integration tests)

### tests/test_integration_actors.py (NEW)
From: `test_unit_simple.py`
```python
"""
Integration tests for actor spawning and manipulation
Requires: Unreal Engine running, level open
"""
import pytest

def test_spawn_grid():
    """Test spawning a grid of actors"""
    # Use pytest fixtures, proper assertions
    
def test_clear_level():
    """Test clearing actors from level"""
    
def test_actor_labeling():
    """Test actor label assignment"""
```

### tests/test_integration_upsert.py (NEW)
From: `test_upsert_persistent.py`
```python
"""
Integration tests for upsert functionality
Tests actor creation vs update behavior
"""
import pytest

def test_upsert_creates_new_actors():
    """First run should create actors"""
    
def test_upsert_updates_existing_actors():
    """Subsequent runs should update, not duplicate"""
    
def test_upsert_position_persistence():
    """Actor positions should persist and update across runs"""
```

### tests/test_integration_upsert_config.py (NEW)
From: `test_upsert_config.py`
```python
"""
Integration tests for configurable upsert modes
Tests UPSERT_MODE=True vs False behavior
"""
import pytest

def test_upsert_mode_true():
    """With upsert_mode=True, should update existing actors"""
    
def test_upsert_mode_false():
    """With upsert_mode=False, should create unique actors"""
```

### tests/test_integration_workflow.py (NEW)
From: `test_workflow_direct.py`, `test_simple_workflow.py`
```python
"""
Integration tests for workflow execution in Unreal
Tests complete workflow DAGs with real actor spawning
"""
import pytest

def test_simple_sequence_workflow():
    """Test sequential task execution"""
    
def test_dag_workflow_with_dependencies():
    """Test DAG execution with task dependencies"""
```

### tests/test_integration_materials.py (NEW)
From: `test_materials.py`
```python
"""
Integration tests for material and color manipulation
"""
import pytest

def test_set_actor_color():
    """Test changing actor colors"""
    
def test_color_grid():
    """Test applying colors to grid of actors"""
```

## 4. Files to KEEP

### Core Infrastructure
- `remotecontrol/` - Remote control module
- `unreallib/` - Unreal library module
- `tests/` - Proper unit tests (6 files + 5 new integration tests)
- `examples/` - Usage examples (existing + 2 new)

### Configuration & Setup
- `.env`, `.env.example`
- `config.py`
- `requirements.txt`
- `pytest.ini`
- `setup.bat`, `setup_upyrc.bat`

### Documentation
- `README.md`, `README_NEW.md`
- `QUICKSTART.md`, `QUICKSTART_UPYRC.md`
- `TESTING_CHECKLIST.md`
- `MIGRATION.md`, `UPYRC_SETUP.md`

### Utilities (keep the valuable ones)
- `count_actors.py` - Useful utility
- `check_current_level.py` - Useful utility
- `file_watcher.py` - If still used
- `monitor_ue_log.py` - Useful for debugging
- `troubleshooting_guide.py` - Documentation/utility

### Legacy Utils (evaluate these)
- `level_utils.py` - Check if superseded by unreallib.level
- `populate_scene.py` - Check if superseded by workflow examples
- `populate_multi_level.py` - Check if still needed
- `remote_control_example.py` - Check if superseded by examples/
- `run_in_unreal.py`, `run_in_console.py` - Check if still used
- `send_command.py`, `send_to_unreal.py` - Check if superseded by remotecontrol module
- Batch files: `run_python_in_unreal.bat`, `send_to_unreal.bat`

## Execution Steps

1. **Backup**: Create `scripts/archive/` for deleted files (in case)
2. **Delete**: Remove all Category 1 files (35 files)
3. **Create Examples**: Build new example files in `examples/`
4. **Create Tests**: Build new integration tests in `tests/`
5. **Update Documentation**: Update README with new structure
6. **Run Tests**: Verify all pytest tests still pass
7. **Cleanup**: Remove `scripts/archive/` after verification

## Final Structure

```
scripts/
  remotecontrol/          # Remote control module
  unreallib/              # Unreal library module
  tests/                  # All pytest tests
    test_client.py
    test_config.py
    test_workflow_*.py (4 files)
    test_integration_*.py (5 NEW files)
  examples/               # Usage examples
    spawn_shapes.py (NEW)
    spawn_grid.py (renamed)
    run_create_mode.py
    run_upsert_mode.py
  utils/                  # Utility scripts (NEW folder?)
    count_actors.py
    check_current_level.py
    monitor_ue_log.py
  config.py
  requirements.txt
  pytest.ini
  setup.bat
  README.md
```

## Benefits

1. **Clarity**: Clear separation of tests, examples, and utilities
2. **Maintainability**: Proper pytest tests are easier to maintain
3. **Discoverability**: New users can easily find examples
4. **CI/CD Ready**: Proper test structure enables automation
5. **Less Clutter**: ~35 fewer files in root directory
