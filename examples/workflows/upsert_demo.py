"""
Upsert Workflow Example - Demonstrating Update-or-Insert Pattern

This example shows how to:
1. Create actors with registry tracking
2. Update existing actors (change colors)
3. Add new actors without duplicating existing ones
"""

from unreallib.workflow import WorkflowGraph, WorkflowExecutor, WorkflowConfig
from unreallib.tasks import (
    ClearLevelTask,
    SpawnGridTask,
    SetActorColorTask,
)
from unreallib.materials import COLORS


def run_upsert_demo():
    """
    Run a demonstration of upsert functionality
    
    First execution: Creates a 3x3 grid of cubes
    Second execution: Changes their colors to rainbow pattern
    Third execution: Updates grid to 5x5 (adds new, keeps existing)
    """
    
    # Phase 1: Initial Creation
    print("\n" + "="*60)
    print("PHASE 1: Initial Creation - Spawning 3x3 Grid")
    print("="*60)
    
    graph = WorkflowGraph()
    
    # Clear the scene first
    graph.add_task(ClearLevelTask("clear_scene"))
    
    # Create initial 3x3 grid
    graph.add_task(
        SpawnGridTask(
            name="create_grid",
            rows=3,
            cols=3,
            spacing=200.0,
            shape='cube',
            scale=1.0
        ),
        depends_on=["clear_scene"]
    )
    
    config = WorkflowConfig.get_preset_config("clean_slate")
    executor = WorkflowExecutor(graph, config)
    results = executor.execute()
    
    print("\n✓ Phase 1 Complete!")
    print(f"  Created: {results['create_grid'].output['actor_count']} actors")
    
    
    # Phase 2: Color Update (Upsert)
    print("\n" + "="*60)
    print("PHASE 2: Color Update - Rainbow Pattern")
    print("="*60)
    
    graph2 = WorkflowGraph()
    
    # Color the grid in rainbow pattern
    # Row 0: Red, Orange, Yellow
    # Row 1: Green, Cyan, Blue
    # Row 2: Purple, Magenta, Pink
    
    rainbow_colors = [
        COLORS['red'], COLORS['orange'], COLORS['yellow'],
        COLORS['green'], COLORS['cyan'], COLORS['blue'],
        COLORS['purple'], COLORS['magenta'], COLORS['pink']
    ]
    
    # Create individual color tasks for each position
    for i, color in enumerate(rainbow_colors):
        row = i // 3
        col = i % 3
        actor_label = f"workflow_grid_{row}_{col}"
        
        graph2.add_task(
            SetActorColorTask(
                name=f"color_{row}_{col}",
                actor_labels=[actor_label],
                color=color,
                opacity=1.0
            )
        )
    
    config2 = WorkflowConfig(
        clear_before_execute=False,  # Don't clear existing actors!
        save_level_after=False
    )
    executor2 = WorkflowExecutor(graph2, config2)
    results2 = executor2.execute()
    
    total_colored = sum(r.output['modified_count'] for r in results2.values())
    print(f"\n✓ Phase 2 Complete!")
    print(f"  Colored: {total_colored} actors with rainbow pattern")
    
    
    # Phase 3: Expand Grid (Upsert with new actors)
    print("\n" + "="*60)
    print("PHASE 3: Expand Grid - 3x3 → 5x5 (Upsert Mode)")
    print("="*60)
    
    graph3 = WorkflowGraph()
    
    # Expand to 5x5 - this should keep existing colored actors
    # and add new ones in default material
    graph3.add_task(
        SpawnGridTask(
            name="expand_grid",
            rows=5,
            cols=5,
            spacing=200.0,
            shape='cube',
            scale=1.0
        )
    )
    
    config3 = WorkflowConfig(
        clear_before_execute=False,  # Keep existing!
        upsert_mode=True,            # Update existing, create new
        actor_id_prefix="workflow_grid_",
        save_level_after=False
    )
    executor3 = WorkflowExecutor(graph3, config3)
    results3 = executor3.execute()
    
    print(f"\n✓ Phase 3 Complete!")
    print(f"  Total actors: {results3['expand_grid'].output.get('actor_count', 'N/A')}")
    print(f"  (Should have kept the 9 rainbow-colored cubes + added 16 new ones)")
    
    
    # Summary
    print("\n" + "="*60)
    print("UPSERT DEMO SUMMARY")
    print("="*60)
    print("This demo showed:")
    print("  1. Initial creation (3x3 grid)")
    print("  2. Updating existing actors (rainbow colors)")
    print("  3. Expanding while preserving updates (5x5 grid)")
    print("\nKey Concepts:")
    print("  - clear_before_execute=False preserves existing actors")
    print("  - upsert_mode=True updates existing, creates new")
    print("  - Actor registry tracks IDs for intelligent updates")
    print("="*60)


if __name__ == "__main__":
    run_upsert_demo()
