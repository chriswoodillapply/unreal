"""
Simple test to verify upsert + color changing workflow

Run this script multiple times to see:
1. First run: Creates 3x3 grid of cubes
2. Second run: Changes colors to rainbow (upsert - updates existing)
3. Third run: Expand to 5x5 (upsert - keeps colored ones, adds new)
"""

from unreallib.workflow import WorkflowGraph, WorkflowExecutor, WorkflowConfig
from unreallib.tasks import ClearLevelTask, SpawnGridTask, SetActorColorTask
from unreallib.materials import COLORS

# Create workflow
graph = WorkflowGraph()

# Step 1: Clear the scene
graph.add_task(ClearLevelTask("clear"))

# Step 2: Spawn 3x3 grid
graph.add_task(
    SpawnGridTask(
        name="spawn_grid",
        rows=3,
        cols=3,
        spacing=200.0,
        shape='cube',
        scale=1.0
    ),
    depends_on=["clear"]
)

# Step 3: Color them rainbow
rainbow_colors = [
    ('red', COLORS['red']),
    ('orange', COLORS['orange']),
    ('yellow', COLORS['yellow']),
    ('green', COLORS['green']),
    ('cyan', COLORS['cyan']),
    ('blue', COLORS['blue']),
    ('purple', COLORS['purple']),
    ('magenta', COLORS['magenta']),
    ('pink', COLORS['pink']),
]

for i, (color_name, color) in enumerate(rainbow_colors):
    row = i // 3
    col = i % 3
    
    graph.add_task(
        SetActorColorTask(
            name=f"color_{color_name}",
            actor_labels=[f"workflow_grid_{row}_{col}"],
            color=color,
            opacity=1.0
        ),
        depends_on=["spawn_grid"]
    )

# Execute with clean slate config
config = WorkflowConfig.get_preset_config("clean_slate")
executor = WorkflowExecutor(graph, config)

print("\n" + "="*60)
print("UPSERT + COLOR TEST")
print("="*60)
print("Creating 3x3 rainbow grid...")

results = executor.execute()

# Summary
spawn_result = results.get("spawn_grid")
if spawn_result:
    print(f"\n✓ Spawned {spawn_result.output['actor_count']} actors")

colored_count = sum(
    r.output.get('modified_count', 0) 
    for k, r in results.items() 
    if k.startswith('color_')
)
print(f"✓ Colored {colored_count} actors with rainbow pattern")

print("\n" + "="*60)
print("Check your Unreal level - you should see a 3x3 rainbow grid!")
print("="*60)
