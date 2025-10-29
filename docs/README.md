# Unreal Python Remote Control

A professional Python toolkit for remote code execution in Unreal Engine 5.6+, featuring a DAG-based workflow system for procedural scene generation and actor manipulation.

## 🚀 Quick Start

```powershell
# 1. Setup environment
cd scripts
.\setup.bat

# 2. Configure your Unreal project
python -m remotecontrol.setup --project "C:\Path\To\YourProject.uproject"

# 3. Run your first example (with Unreal Engine running)
python -m remotecontrol examples/spawn_shapes.py --method=file
```

## 📁 Project Structure

```
scripts/
├── remotecontrol/      # Remote execution module
├── unreallib/          # Unreal utility library
│   ├── actors.py       # Actor spawning
│   ├── level.py        # Level operations
│   ├── materials.py    # Material manipulation
│   ├── workflow/       # Workflow orchestration (DAG)
│   └── tasks/          # Task implementations
├── tests/              # Unit & integration tests (77 passing)
├── examples/           # Usage examples
├── utils/              # Utility scripts
├── docs/               # Documentation
└── config.py           # Configuration
```

## 🎯 Features

- **Remote Execution**: File-based command passing to Unreal Engine
- **Workflow System**: DAG-based task orchestration with topological sorting
- **Actor Manipulation**: Spawn, position, scale, and color actors
- **Upsert Pattern**: Update existing actors or create new ones
- **Configuration**: Environment-based setup with presets
- **Testing**: 77 unit tests with pytest

## 📖 Documentation

### Getting Started
- **[Complete Guide](docs/README_CLEAN.md)** - Full documentation with examples
- **[Quick Start](docs/QUICKSTART.md)** - Get started in 5 minutes
- **[upyrc Setup](docs/QUICKSTART_UPYRC.md)** - Remote control configuration

### Development
- **[Development Guidelines](docs/DEVELOPMENT_GUIDELINES.md)** - ⚠️ **REQUIRED READING** - Project standards and rules
- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute to this project
- **[Testing Guide](docs/TESTING_CHECKLIST.md)** - Testing workflow and procedures

### Reference
- **[Migration Guide](docs/MIGRATION.md)** - Upgrading from old structure
- **[Setup Cleanup](docs/SETUP_CLEANUP.md)** - Setup scripts organization
- **[Cleanup Summary](docs/CLEANUP_SUMMARY.md)** - Recent reorganization details

## 💡 Usage Examples

### Basic Actor Spawning

```python
from unreallib import actors

# Spawn individual shapes
cube = actors.spawn_cube(location=(0, 0, 50))
sphere = actors.spawn_sphere(location=(200, 0, 50))

# Spawn a grid
grid = actors.spawn_grid(rows=3, cols=3, spacing=200.0, shape='sphere')
```

### Workflow Execution

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

# Run specific test file
pytest tests/test_workflow_graph.py -v

# Current status: 77/77 tests passing ✅
```

## 🛠️ Requirements

- **Python**: 3.10+ (local), 3.9/3.10 (Unreal Engine)
- **Unreal Engine**: 5.6+
- **Plugins**: PythonScriptPlugin, RemoteControl
- **Packages**: upyrc 0.12.0, pytest 8.4.2, python-dotenv

## 📊 Project Stats

- **77** unit tests (100% passing)
- **95%+** coverage on workflow core
- **9** example scripts
- **3** utility scripts
- **Professional** module structure

## 🔗 Quick Links

- [Examples Directory](examples/) - Ready-to-run examples
- [Tests Directory](tests/) - Unit and integration tests
- [Utils Directory](utils/) - Helpful utilities
- [Documentation](docs/) - Complete documentation

---

**For detailed documentation, see [docs/README_CLEAN.md](docs/README_CLEAN.md)**
