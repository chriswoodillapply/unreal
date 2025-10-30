"""
Task for applying different materials to actors in a grid or pattern
"""

import unreal
from typing import Dict
from unreallib.workflow.task import Task, TaskResult, TaskStatus


class ApplyMaterialsTask(Task):
    """
    Apply different materials to actors based on a material map
    
    Example params:
        {
            "prefix": "workflow_grid_",
            "material_map": {
                "0_0": "/Engine/BasicShapes/BasicShapeMaterial",
                "0_1": "/Engine/EngineMaterials/WorldGridMaterial",
                "1_0": "/Game/StarterContent/Materials/M_Metal_Gold"
            }
        }
    """
    
    def __init__(self, name: str, prefix: str = "", material_map: Dict[str, str] = None):
        """
        Args:
            name: Task identifier
            prefix: Actor label prefix to filter actors (e.g., "workflow_grid_")
            material_map: Dict mapping actor IDs to material paths
                         Key format: "row_col" (e.g., "0_0", "1_2")
                         Value: Material asset path
        """
        super().__init__(name, prefix=prefix, material_map=material_map or {})
        self.prefix = prefix
        self.material_map = material_map or {}
    
    def execute(self, context: dict) -> TaskResult:
        """Apply materials based on material map."""
        from unreallib import materials
        
        print("=" * 60)
        print("APPLY_MATERIALS_TASK")
        print("=" * 60)
        print(f"ApplyMaterialsTask: Looking for actors with prefix '{self.prefix}'")
        print(f"ApplyMaterialsTask: Material map has {len(self.material_map)} entries")
        
        editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        all_actors = editor_actor_subsystem.get_all_level_actors()
        
        # Debug: print actor labels to see what's in the scene
        print(f"ApplyMaterialsTask: Total actors in scene: {len(all_actors)}")
        print(f"ApplyMaterialsTask: Looking for actors starting with: '{self.prefix}'")
        
        # Find ALL actors with our prefix
        prefix_actors = []
        for actor in all_actors:
            label = actor.get_actor_label()
            if label.startswith(self.prefix):
                prefix_actors.append(label)
        
        if prefix_actors:
            print(f"  ✓ Found {len(prefix_actors)} actors with prefix '{self.prefix}':")
            for label in prefix_actors[:15]:  # Show first 15
                print(f"    - {label}")
        else:
            print(f"  ✗ NO actors found with prefix '{self.prefix}'")
            print(f"  DEBUG: Showing 5 random actor labels from scene:")
            import random
            sample = random.sample(all_actors, min(5, len(all_actors)))
            for actor in sample:
                print(f"    - '{actor.get_actor_label()}'")
        
        modified_count = 0
        matching_actors = []
        errors = []
        
        for actor in all_actors:
            label = actor.get_actor_label()
            if label.startswith(self.prefix):
                matching_actors.append(label)
                # Check if we have a material for this actor
                for actor_id, material_path in self.material_map.items():
                    full_id = f"{self.prefix}{actor_id}"
                    if label == full_id:
                        print(f"  Applying material to '{label}': {material_path}")
                        try:
                            materials.set_actor_material(actor, material_path)
                            modified_count += 1
                        except Exception as e:
                            error_msg = f"Failed to apply material to {label}: {str(e)}"
                            print(f"  ✗ {error_msg}")
                            errors.append(error_msg)
                        break
        
        print(f"ApplyMaterialsTask: Found {len(matching_actors)} matching actors")
        print(f"ApplyMaterialsTask: Modified {modified_count} actors")
        if errors:
            print(f"ApplyMaterialsTask: {len(errors)} errors occurred")
        
        return TaskResult(
            status=TaskStatus.SUCCESS if modified_count > 0 else TaskStatus.FAILED,
            output={
                'modified_count': modified_count,
                'material_map_size': len(self.material_map),
                'matching_actors': matching_actors,
                'errors': errors
            },
            metadata={'task_type': 'apply_materials'}
        )
