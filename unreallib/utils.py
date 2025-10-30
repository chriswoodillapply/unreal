"""
Actor tracking and management utilities for upsert operations
"""

import unreal
from typing import Dict, Optional, List


class ActorRegistry:
    """
    Registry for tracking workflow-created actors by ID
    
    Enables update-or-insert (upsert) operations by maintaining
    a mapping of actor IDs to Unreal actor references.
    """
    
    def __init__(self, prefix: str = "workflow_"):
        """
        Initialize actor registry
        
        Args:
            prefix: Prefix for actor labels
        """
        self.prefix = prefix
        self._actors: Dict[str, unreal.Actor] = {}
        
        # Load existing actors from level with this prefix
        self._load_existing_actors()
    
    def _load_existing_actors(self):
        """Load existing actors from the level that match our prefix"""
        all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
        loaded_count = 0
        
        for actor in all_actors:
            if actor:
                label = actor.get_actor_label()
                if label.startswith(self.prefix):
                    # This actor belongs to our registry
                    self._actors[label] = actor
                    loaded_count += 1
        
        if loaded_count > 0:
            print(f"  [ActorRegistry] Loaded {loaded_count} existing actors with prefix '{self.prefix}'")
    
    def register(self, actor_id: str, actor: unreal.Actor):
        """
        Register an actor with an ID
        
        Args:
            actor_id: Unique identifier for this actor
            actor: Unreal actor reference
        """
        full_id = f"{self.prefix}{actor_id}"
        self._actors[full_id] = actor
        
        # Set actor label in Unreal for debugging
        print(f"  [ActorRegistry] Setting label: '{full_id}' on actor {actor}")
        actor.set_actor_label(full_id)
        # Verify it was set
        actual_label = actor.get_actor_label()
        print(f"  [ActorRegistry] Verified label: '{actual_label}'")
    
    def get(self, actor_id: str) -> Optional[unreal.Actor]:
        """
        Get actor by ID
        
        Args:
            actor_id: Actor identifier
            
        Returns:
            Actor reference if found, None otherwise
        """
        full_id = f"{self.prefix}{actor_id}"
        return self._actors.get(full_id)
    
    def exists(self, actor_id: str) -> bool:
        """Check if actor exists in registry"""
        full_id = f"{self.prefix}{actor_id}"
        return full_id in self._actors
    
    def update_or_create(
        self,
        actor_id: str,
        create_fn,
        update_fn=None
    ) -> tuple[unreal.Actor, bool]:
        """
        Update existing actor or create new one
        
        Args:
            actor_id: Actor identifier
            create_fn: Function to call to create new actor
            update_fn: Optional function to call to update existing actor
            
        Returns:
            Tuple of (actor, was_created)
        """
        if self.exists(actor_id):
            # Update existing
            actor = self.get(actor_id)
            if update_fn:
                update_fn(actor)
            return actor, False
        else:
            # Create new
            actor = create_fn()
            self.register(actor_id, actor)
            return actor, True
    
    def find_by_label(self, level) -> Dict[str, unreal.Actor]:
        """
        Find all workflow actors in level by label
        
        Args:
            level: Current level
            
        Returns:
            Dictionary mapping IDs to actors
        """
        editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        all_actors = editor_actor_subsystem.get_all_level_actors()
        
        workflow_actors = {}
        for actor in all_actors:
            label = actor.get_actor_label()
            if label.startswith(self.prefix):
                workflow_actors[label] = actor
        
        return workflow_actors
    
    def clear(self):
        """Clear the registry"""
        self._actors.clear()
    
    def __len__(self) -> int:
        return len(self._actors)
    
    def __contains__(self, actor_id: str) -> bool:
        return self.exists(actor_id)
