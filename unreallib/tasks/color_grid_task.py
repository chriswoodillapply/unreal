"""
Color Grid Task - Applies colors to actors in a grid pattern
"""

from typing import Optional
from unreallib.workflow.task import Task, TaskResult, TaskStatus


class ColorGridTask(Task):
    """Task to apply colors to actors in a grid pattern"""
    
    def __init__(
        self,
        name: str,
        prefix: str = "workflow_",
        color_map: Optional[dict] = None
    ):
        """
        Initialize color grid task
        
        Args:
            name: Task identifier
            prefix: Prefix for actor labels to target
            color_map: Dictionary mapping actor IDs to colors
        """
        # Pass params to base class so they're properly stored in context
        super().__init__(name, prefix=prefix, color_map=color_map or {})
        self.prefix = prefix
        self.color_map = color_map or {}
    
    def execute(self, context: dict) -> TaskResult:
        """Apply colors based on color map. If a material_path and parameter name exist in context, apply dynamic instance based on that material instance."""
        import unreal
        from unreallib import materials
        
        print("=" * 60)
        print("COLOR_GRID_TASK VERSION: 2024-10-29-SIMPLIFIED-v2")
        print("=" * 60)
        print(f"ColorGridTask: Looking for actors with prefix '{self.prefix}'")
        print(f"ColorGridTask: Color map has {len(self.color_map)} entries")
        
        editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        all_actors = editor_actor_subsystem.get_all_level_actors()
        
        modified_count = 0
        matching_actors = []
        
        for actor in all_actors:
            label = actor.get_actor_label()
            if label.startswith(self.prefix):
                matching_actors.append(label)
                # Check if we have a color for this actor
                for actor_id, color_data in self.color_map.items():
                    full_id = f"{self.prefix}{actor_id}"
                    if label == full_id:
                        color = color_data.get('color', (1.0, 1.0, 1.0))
                        opacity = color_data.get('opacity', 1.0)
                        print(f"  Setting color for '{label}' to {color}")
                        # Use materials.set_actor_color which creates dynamic materials correctly
                        materials.set_actor_color(actor, color, opacity)
                        modified_count += 1
                        break
        
        print(f"ColorGridTask: Found {len(matching_actors)} matching actors")
        print(f"ColorGridTask: Modified {modified_count} actors")
        if len(matching_actors) > 0:
            print(f"  Matching actors: {matching_actors[:5]}...")
        
        return TaskResult(
            status=TaskStatus.SUCCESS,
            output={
                'modified_count': modified_count,
                'color_map_size': len(self.color_map),
                'matching_actors': matching_actors
            },
            metadata={'task_type': 'color_grid'}
        )
