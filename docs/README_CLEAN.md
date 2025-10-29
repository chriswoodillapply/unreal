# Unreal Python Remote Control

A professional Python toolkit for remote code execution in Unreal Engine 5.6+, featuring a DAG-based workflow system for procedural scene generation and actor manipulation.

## 🚀 Quick Start

1. **Setup Environment**:
   ```powershell
   cd scripts
   .\setup.bat
   ```

2. **Configure Unreal Project**:
   ```powershell
   python -m remotecontrol.setup --project "C:\Path\To\YourProject.uproject"
   ```

3. **Run Your First Example**:
   ```powershell
   python -m remotecontrol examples/spawn_shapes.py --method=file
   ```

## 📁 Project Structure

```
scripts/
├── remotecontrol/          # Remote execution module
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── client.py           # Remote execution client
│   ├── execute.py          # Execution utilities
│   └── setup.py            # Unreal project setup
│
├── unreallib/              # Unreal utility library
│   ├── actors.py           # Actor spawning utilities
│   ├── level.py            # Level operations
│   ├── materials.py        # Material manipulation
│   ├── utils.py            # Shared utilities (ActorRegistry)
│   ├── workflow/           # Workflow orchestration
│   │   ├── task.py         # Base task class
│   │   ├── graph.py        # DAG workflow graph
│   │   ├── executor.py     # Workflow executor
│   │   └── config.py       # Workflow configuration
│   └── tasks/              # Task implementations
│       ├── clear_level.py
│       ├── spawn_actors.py
│       └── material_tasks.py
│
├── tests/                  # Unit & integration tests
│   ├── test_workflow_*.py  # Workflow unit tests (51 tests)
│   ├── test_client.py      # Client tests
│   └── test_integration_*.py  # Integration tests (NEW)
│
├── examples/               # Usage examples
│   ├── spawn_shapes.py     # Basic shape spawning
│   ├── spawn_grid.py       # Grid spawning
│   ├── run_upsert_mode.py  # Upsert mode demo
│   └── run_create_mode.py  # Create mode demo
│
├── utils/                  # Utility scripts
│   ├── count_actors.py     # Count actors in level
│   ├── check_current_level.py  # Check current level
│   └── monitor_ue_log.py   # Monitor Unreal logs
│
├── config.py               # Main configuration
├── requirements.txt        # Python dependencies
├── pytest.ini              # Pytest configuration
└── setup.bat               # Environment setup
```

## 🎯 Features

### Remote Execution
- **File-based execution**: Reliable command passing via file watcher
- **Environment configuration**: `.env` based setup
- **Auto-setup**: Automatic Unreal project configuration

### Workflow System
- **DAG orchestration**: Dependency-based task execution with topological sorting
- **Strategy pattern**: Extensible task system
- **Configuration presets**: clean_slate, incremental, production modes
- **Upsert support**: Update existing actors or create new ones

### Actor Manipulation
- **Spawning**: Cubes, spheres, cylinders with customizable properties
- **Patterns**: Grids, circles, spirals
- **Materials**: Dynamic color manipulation
- **Registry**: ID-based actor tracking for upsert operations

## 📖 Usage Examples

### Basic Actor Spawning

```python
from unreallib import actors

# Spawn individual shapes
cube = actors.spawn_cube(location=(0, 0, 50))
sphere = actors.spawn_sphere(location=(200, 0, 50))

# Spawn a grid
grid = actors.spawn_grid(rows=3, cols=3, spacing=200.0, shape='sphere')
```

### Workflow System

```python
from unreallib.workflow import WorkflowGraph, WorkflowExecutor
from unreallib.tasks import ClearLevelTask, SpawnGridTask

# Build workflow
workflow = WorkflowGraph()

clear = ClearLevelTask(task_id="clear")
spawn = SpawnGridTask(task_id="spawn", rows=3, cols=3)

workflow.add_task(clear)
workflow.add_task(spawn, dependencies=["clear"])

# Execute
executor = WorkflowExecutor()
results = executor.execute(workflow)
```

### Upsert Pattern

```python
from unreallib.utils import ActorRegistry
from unreallib import actors

registry = ActorRegistry()

# First call creates, second call updates same actor
actor = registry.update_or_create(
    actor_id="my_cube_1",
    create_func=lambda: actors.spawn_cube(location=(0, 0, 50)),
    update_func=lambda a: a.set_actor_location(unreal.Vector(0, 0, 150))
)
```

## 🧪 Testing

```powershell
# Run all unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=unreallib --cov=remotecontrol --cov-report=html

# Run specific test file
pytest tests/test_workflow_graph.py -v

# Run integration tests (requires Unreal running)
python -m remotecontrol tests/test_integration_actors.py --method=file
```

**Current Status**: 51/51 unit tests passing, 95%+ coverage on workflow core

## 🛠️ Configuration

### Environment Variables (.env)

```env
# Remote Control
UNREAL_REMOTE_PORT=6766
UNREAL_MULTICAST_GROUP=230.0.0.1
UNREAL_MULTICAST_TTL=1

# Project Paths
UNREAL_PROJECT_PATH=C:\Path\To\Your\Project.uproject
UNREAL_ENGINE_PATH=C:\Program Files\Epic Games\UE_5.6
```

### Workflow Configuration

```python
from unreallib.workflow import WorkflowConfig

# Preset configurations
config = WorkflowConfig.clean_slate()      # Clear level before execution
config = WorkflowConfig.incremental()      # Don't clear, add to existing
config = WorkflowConfig.production()       # Safe mode with saves

# Custom configuration
config = WorkflowConfig(
    clear_before_execute=True,
    upsert_mode=True,
    save_level_after=False
)
```

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)**: Get started in 5 minutes
- **[upyrc Setup](QUICKSTART_UPYRC.md)**: Remote control setup details
- **[Testing Checklist](TESTING_CHECKLIST.md)**: Testing workflow
- **[Migration Guide](MIGRATION.md)**: Upgrading from old structure

## 🔧 Requirements

- **Python**: 3.10+ (local), 3.9/3.10 (Unreal Engine)
- **Unreal Engine**: 5.6+
- **Plugins**: PythonScriptPlugin, RemoteControl
- **Python Packages**: upyrc 0.12.0, pytest 8.4.2, python-dotenv

## 🤝 Contributing

1. Create feature branch
2. Add tests for new functionality
3. Ensure all tests pass: `pytest tests/ -v`
4. Update documentation
5. Submit pull request

## 📝 License

See LICENSE file for details.

## 🎓 Advanced Topics

### Custom Tasks

```python
from unreallib.workflow.task import Task, TaskResult

class CustomTask(Task):
    def execute(self, context: dict) -> TaskResult:
        # Import unreal here (lazy import)
        import unreal
        from unreallib import actors
        
        # Your custom logic
        actor = actors.spawn_cube(location=(0, 0, 50))
        
        return TaskResult.success(
            message="Custom task complete",
            data={"actor": actor}
        )
```

### Integration Testing

Integration tests run actual code in Unreal Engine:

```python
# tests/test_integration_custom.py
def test_my_feature():
    code = '''
from unreallib import actors
actor = actors.spawn_cube(location=(0, 0, 50))
assert actor is not None
print("✓ Feature working")
'''
    # Execute via remotecontrol
```

Run with:
```powershell
python -m remotecontrol tests/test_integration_custom.py --method=file
```

## 🐛 Troubleshooting

### Common Issues

1. **"Module 'unreal' not found"**
   - Ensure code runs inside Unreal Engine
   - Check init_unreal.py adds scripts folder to sys.path

2. **"Connection refused"**
   - Verify RemoteControl plugin enabled
   - Check port 6766 is open
   - Use `--method=file` for file-based execution

3. **Import errors in tests**
   - Run tests from scripts directory
   - Check virtual environment activated

### Debug Utilities

```powershell
# Count actors in level
python -m remotecontrol utils/count_actors.py --method=file

# Check current level
python -m remotecontrol utils/check_current_level.py --method=file

# Monitor Unreal logs
python utils/monitor_ue_log.py
```

## 📊 Project Stats

- **51** unit tests (100% passing)
- **95%+** coverage on workflow core
- **35+** legacy files archived
- **5** integration test suites
- **4** example scripts
- **3** utility scripts

---

**Made with ❤️ for Unreal Engine procedural workflows**
