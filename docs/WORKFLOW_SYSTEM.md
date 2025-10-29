# JSON Workflow System

## Overview

The JSON workflow system allows you to define complex Unreal Engine workflows using simple JSON files. This makes it easy to create, share, and version control your scene generation workflows.

## Quick Start

### 1. Create a Workflow JSON

```json
{
  "name": "My Workflow",
  "description": "What this workflow does",
  "config": {
    "upsert_mode": false,
    "clear_before_execute": true,
    "save_after": false,
    "actor_id_prefix": "my_prefix_"
  },
  "tasks": [
    {
      "name": "clear_scene",
      "type": "ClearLevelTask"
    },
    {
      "name": "spawn_grid",
      "type": "SpawnGridTask",
      "params": {
        "rows": 5,
        "cols": 5,
        "spacing": 200,
        "shape": "cube"
      },
      "depends_on": ["clear_scene"]
    }
  ]
}
```

### 2. Load and Execute

```python
from unreallib.workflow import WorkflowLoader, WorkflowExecutor

# Load workflow
loader = WorkflowLoader()
workflow = loader.load('my_workflow')  # .json extension optional
config = loader.last_config

# Execute
executor = WorkflowExecutor(config=config)
results = executor.execute(workflow)

# Check results
for task_name, result in results.items():
    print(f"{task_name}: {result.status}")
```

### 3. Run via Remote Control

```powershell
# Copy run_workflow.py to your project
# Edit to load your workflow name
python -m remotecontrol examples/run_workflow.py --method file
```

## Architecture

### Components

1. **WorkflowLoader** - Loads JSON files and creates WorkflowGraph instances
2. **TASK_REGISTRY** - Maps task type strings to Python classes
3. **JSON Workflows** - Declarative workflow definitions in `workflows/` folder
4. **WorkflowGraph** - DAG of tasks with dependencies
5. **WorkflowExecutor** - Executes workflows with configuration

### Flow

```
JSON File → WorkflowLoader → WorkflowGraph → WorkflowExecutor → Results
                ↓
            last_config (WorkflowConfig)
```

## Available Task Types

| Task Type | Description | Key Parameters |
|-----------|-------------|----------------|
| `ClearLevelTask` | Clears all actors from level | None |
| `SpawnGridTask` | Spawns actors in grid pattern | rows, cols, spacing, shape |
| `SpawnCircleTask` | Spawns actors in circle pattern | count, radius, shape |
| `SpawnSpiralTask` | Spawns actors in spiral pattern | count, max_radius, height_increment |
| `SetActorColorTask` | Colors specific actors | actor_labels, color, opacity |
| `ColorGridTask` | Applies color map to grid | prefix, color_map |

## Configuration Options

```json
{
  "config": {
    "upsert_mode": false,           // Update existing actors vs create new
    "clear_before_execute": false,  // Clear level before workflow
    "save_after": false,             // Save level after workflow
    "actor_id_prefix": "workflow_"   // Prefix for actor labels
  }
}
```

## Example Workflows

### Simple Grid (simple_grid.json)
- Clears scene
- Spawns 5x5 grid of cubes
- Good for testing

### Colored Grid (colored_grid.json)
- Creates 3x3 grid with upsert mode
- Applies different colors to each actor
- Demonstrates color mapping

### Multiple Patterns (multiple_patterns.json)
- Clears scene
- Spawns grid, circle, and spiral in parallel
- Demonstrates parallel task execution

## Adding New Task Types

1. Create task class in `unreallib/tasks/`:

```python
from unreallib.workflow import Task, TaskResult, TaskStatus

class MyCustomTask(Task):
    def __init__(self, name: str, param1: str, param2: int):
        super().__init__(name, param1=param1, param2=param2)
    
    def execute(self, context: dict) -> TaskResult:
        # Your implementation
        return TaskResult(
            status=TaskStatus.SUCCESS,
            output={'result': 'success'}
        )
```

2. Add to `unreallib/tasks/__init__.py`:

```python
from .my_custom_task import MyCustomTask

__all__ = [
    # ... existing tasks
    'MyCustomTask',
]
```

3. Register in `unreallib/workflow/loader.py`:

```python
TASK_REGISTRY = {
    # ... existing tasks
    'MyCustomTask': MyCustomTask,
}
```

4. Use in JSON:

```json
{
  "name": "my_task",
  "type": "MyCustomTask",
  "params": {
    "param1": "value1",
    "param2": 42
  }
}
```

## Testing

All workflow loader functionality is tested:

```powershell
# Run workflow loader tests
pytest tests/test_workflow_loader.py -v

# Run all tests
pytest tests/ -v
```

Current test coverage: **93/93 tests passing** (includes 16 workflow loader tests)

## Workflow Management

### List Available Workflows

```python
loader = WorkflowLoader()
workflows = loader.list_workflows()
for wf in workflows:
    print(wf)  # simple_grid.json, colored_grid.json, etc.
```

### Get Workflow Info

```python
loader = WorkflowLoader()
info = loader.get_workflow_info('simple_grid')
print(f"Name: {info['name']}")
print(f"Description: {info['description']}")
print(f"Tasks: {info['task_count']}")
```

### Custom Workflow Directory

```python
from pathlib import Path

# Use custom directory
loader = WorkflowLoader(Path('/path/to/my/workflows'))
workflow = loader.load('my_workflow')
```

## Best Practices

1. **Version Control** - Keep workflow JSON files in Git
2. **Descriptive Names** - Use clear task names and workflow descriptions
3. **Dependencies** - Explicitly define task dependencies
4. **Upsert Mode** - Use for iterative development to update existing scenes
5. **Testing** - Test workflows incrementally with small grids first
6. **Documentation** - Document custom workflows in README.md

## Error Handling

The system provides clear error messages:

```python
# Invalid task type
ValueError: Unknown task type 'BadTask'. Available types: ClearLevelTask, SpawnGridTask, ...

# Missing required field
ValueError: Task definition missing 'name': {...}

# File not found
FileNotFoundError: Workflow file not found: /path/to/workflows/missing.json
```

## Performance

- **Parallel Execution**: Independent tasks run in parallel
- **Upsert Mode**: Faster iterations by updating existing actors
- **Dependency Resolution**: Topological sort ensures correct execution order

## Future Enhancements

Potential additions:
- [ ] Workflow validation before execution
- [ ] Workflow templates/presets
- [ ] CLI tool for workflow management
- [ ] Workflow composition (include other workflows)
- [ ] Conditional task execution
- [ ] Loop/iteration support
- [ ] Variable substitution in parameters

## References

- Workflow definitions: `workflows/README.md`
- Task implementations: `unreallib/tasks/`
- Configuration: `unreallib/workflow/config.py`
- Examples: `examples/run_workflow.py`
- Tests: `tests/test_workflow_loader.py`

## Support

For issues or questions:
1. Check documentation in `docs/` folder
2. Review example workflows in `workflows/`
3. Run tests to verify system state
4. Check Git commit history for recent changes
