# Workflow Definitions

This folder contains JSON workflow definitions that can be loaded and executed in Unreal Engine.

## Workflow Format

```json
{
  "name": "Workflow Name",
  "description": "What this workflow does",
  "config": {
    "upsert_mode": true,
    "clear_before_execute": false,
    "save_after": true,
    "actor_id_prefix": "my_prefix_"
  },
  "tasks": [
    {
      "name": "task1",
      "type": "SpawnGridTask",
      "enabled": true,
      "params": {
        "rows": 5,
        "cols": 5,
        "spacing": 200
      }
    },
    {
      "name": "task2",
      "type": "ColorGridTask",
      "enabled": false,
      "params": {
        "prefix": "my_prefix_"
      },
      "depends_on": ["task1"]
    }
  ]
}
```

### Task Properties

Each task supports the following properties:
- **name** (required): Unique identifier for the task
- **type** (required): Task class name (see Available Task Types below)
- **enabled** (optional): Set to `false` to skip this task (defaults to `true`)
- **params** (optional): Task-specific parameters
- **depends_on** (optional): Array of task names this task depends on

## Available Task Types

- **ClearLevelTask** - Clears all actors from the level
- **SpawnGridTask** - Spawns actors in a grid pattern
- **SpawnCircleTask** - Spawns actors in a circle pattern
- **SpawnSpiralTask** - Spawns actors in a spiral pattern
- **SetActorColorTask** - Sets colors on specific actors
- **ColorGridTask** - Applies color map to grid actors

## Usage

### From Python (Local)

```python
from unreallib.workflow import WorkflowLoader, WorkflowExecutor

# Load workflow
loader = WorkflowLoader()
workflow = loader.load('simple_grid')

# Execute
executor = WorkflowExecutor()
result = executor.execute(workflow)
```

### From Command Line

```powershell
# Run a workflow
python -m remotecontrol examples/run_workflow.py --method file
```

## Example Workflows

### simple_grid.json
Creates a basic 5x5 grid of cubes. Good for testing.

### colored_grid.json
Creates a 3x3 grid with different colors using upsert mode.

### multiple_patterns.json
Creates grid, circle, and spiral patterns in parallel.

## Creating Your Own Workflows

1. Create a new `.json` file in this folder
2. Define your tasks and dependencies
3. Set appropriate config options
4. Load and execute using `WorkflowLoader`

## Config Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `upsert_mode` | boolean | false | Update existing actors instead of creating new ones |
| `clear_before_execute` | boolean | false | Clear level before running workflow |
| `save_after` | boolean | false | Save level after workflow completes |
| `actor_id_prefix` | string | "workflow_" | Prefix for actor labels |

## Task Parameters

Each task type has its own parameters. See individual task files in `unreallib/tasks/` for details.

### SpawnGridTask
```json
{
  "rows": 5,
  "cols": 5,
  "spacing": 200,
  "shape": "cube|sphere|cylinder",
  "scale": 1.0
}
```

### SpawnCircleTask
```json
{
  "count": 12,
  "radius": 500,
  "shape": "cube|sphere|cylinder"
}
```

### SpawnSpiralTask
```json
{
  "count": 15,
  "max_radius": 400,
  "height_increment": 50,
  "shape": "cube|sphere|cylinder"
}
```

### ColorGridTask
```json
{
  "prefix": "workflow_grid_",
  "color_map": {
    "0_0": {"color": [1.0, 0.0, 0.0], "opacity": 1.0},
    "0_1": {"color": [0.0, 1.0, 0.0], "opacity": 1.0}
  }
}
```
