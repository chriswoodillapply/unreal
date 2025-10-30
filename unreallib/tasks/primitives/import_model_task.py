"""
Primitive task: Import or spawn a 3D model/static mesh
"""

from typing import Dict, Any
from unreallib.workflow.task import Task, TaskResult, TaskStatus
import unreal


class ImportModelTask(Task):
    """
    Import a 3D model file or spawn an existing static mesh asset
    
    Primitive operation that handles:
    1. Importing external files (FBX, OBJ, etc.) into the project
    2. Spawning existing static mesh assets from content browser
    """
    
    def __init__(
        self,
        name: str,
        source: str = None,  # File path or asset path
        location: tuple = (0, 0, 0),
        rotation: tuple = (0, 0, 0),
        scale: tuple = (1.0, 1.0, 1.0),
        actor_id: str = None,
        use_registry: bool = True,
        import_settings: Dict[str, Any] = None
    ):
        """
        Initialize import model task
        
        Args:
            name: Task name
            source: Path to file (e.g., "C:/Models/chair.fbx") or asset (e.g., "/Game/Models/Chair")
            location: (x, y, z) location
            rotation: (pitch, yaw, roll) rotation in degrees
            scale: (x, y, z) scale (can be uniform or per-axis)
            actor_id: Optional ID for actor registry (enables upsert)
            use_registry: Whether to register actor for upsert operations
            import_settings: Optional dict of import settings for FBX/OBJ files
        """
        super().__init__(
            name,
            source=source,
            location=location,
            rotation=rotation,
            scale=scale,
            actor_id=actor_id,
            use_registry=use_registry,
            import_settings=import_settings or {}
        )
        
        self.source = source
        self.location = location
        self.rotation = rotation
        self.scale = scale
        self.actor_id = actor_id
        self.use_registry = use_registry
        self.import_settings = import_settings or {}
    
    def execute(self, context: Dict[str, Any]) -> TaskResult:
        """Import or spawn a 3D model"""
        from unreallib.utils import ActorRegistry
        
        if not self.source:
            return TaskResult(
                status=TaskStatus.FAILURE,
                output={'error': 'No source specified (file path or asset path)'}
            )
        
        # Determine if source is a file path or asset path
        is_file = self.source.endswith(('.fbx', '.obj', '.FBX', '.OBJ'))
        
        if is_file:
            # Import external file
            static_mesh = self._import_file(self.source)
            if not static_mesh:
                return TaskResult(
                    status=TaskStatus.FAILURE,
                    output={'error': f'Failed to import file: {self.source}'}
                )
        else:
            # Load existing asset
            static_mesh = unreal.EditorAssetLibrary.load_asset(self.source)
            if not static_mesh:
                return TaskResult(
                    status=TaskStatus.FAILURE,
                    output={'error': f'Failed to load asset: {self.source}'}
                )
        
        # Check if we should use upsert mode
        config = context.get('workflow_config')
        use_upsert = self.use_registry and config and config.upsert_mode
        
        if use_upsert and self.actor_id:
            # Use actor registry for upsert
            prefix = config.actor_id_prefix if config else "workflow_"
            registry = ActorRegistry(prefix=prefix)
            
            def create_actor():
                return self._spawn_static_mesh_actor(static_mesh)
            
            def update_actor(actor):
                self._update_actor_transform(actor)
                # Only update mesh if it's a StaticMeshActor with a single mesh
                # Blueprint actors have multiple components, don't try to update them
                if not isinstance(static_mesh, unreal.Blueprint):
                    mesh_component = actor.get_component_by_class(unreal.StaticMeshComponent)
                    if mesh_component and isinstance(static_mesh, unreal.StaticMesh):
                        mesh_component.set_static_mesh(static_mesh)
            
            actor, was_created = registry.update_or_create(
                self.actor_id,
                create_actor,
                update_actor
            )
            
            action = "created" if was_created else "updated"
        else:
            # Simple spawn without registry
            actor = self._spawn_static_mesh_actor(static_mesh)
            action = "created"
        
        return TaskResult(
            status=TaskStatus.SUCCESS,
            output={
                'actor': actor,
                'action': action,
                'location': self.location,
                'source': self.source,
                'mesh': static_mesh
            }
        )
    
    def _import_file(self, file_path: str):
        """Import a 3D model file and return the static mesh"""
        import os
        
        # Set destination path - each model gets its own subfolder to avoid conflicts
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        destination_path = f'/Game/Imported/{base_name}'
        
        # Delete the entire folder if it exists (cleans up all materials, textures, etc.)
        if unreal.EditorAssetLibrary.does_directory_exist(destination_path):
            print(f"  Cleaning up existing folder: {destination_path}")
            unreal.EditorAssetLibrary.delete_directory(destination_path)
        
        # Make sure the parent directory exists
        parent_path = '/Game/Imported'
        if not unreal.EditorAssetLibrary.does_directory_exist(parent_path):
            unreal.EditorAssetLibrary.make_directory(parent_path)
        
        # Create import task
        task = unreal.AssetImportTask()
        task.set_editor_property('filename', file_path)
        task.set_editor_property('destination_path', destination_path)
        task.set_editor_property('destination_name', base_name)
        
        # Don't show dialog
        task.set_editor_property('automated', True)
        task.set_editor_property('save', True)
        task.set_editor_property('replace_existing', True)
        
        # Import settings for FBX
        if file_path.lower().endswith('.fbx'):
            options = unreal.FbxImportUI()
            options.set_editor_property('import_mesh', True)
            options.set_editor_property('import_materials', self.import_settings.get('import_materials', True))
            options.set_editor_property('import_textures', self.import_settings.get('import_textures', True))
            options.set_editor_property('import_as_skeletal', False)  # Import as static mesh
            
            # Get static mesh import settings
            static_mesh_options = options.get_editor_property('static_mesh_import_data')
            
            # Set mesh hierarchy preservation
            combine_meshes = self.import_settings.get('combine_meshes', False)
            print(f"  Import setting: combine_meshes = {combine_meshes}")
            
            if static_mesh_options:
                try:
                    # In UE, combine_meshes controls whether to merge FBX hierarchy into one mesh
                    # False = preserve separate meshes as individual assets
                    static_mesh_options.set_editor_property('combine_meshes', combine_meshes)
                    
                    # Also try setting import_mesh_lo_ds which might affect hierarchy
                    # And ensure we're not forcing single mesh creation
                    if not combine_meshes:
                        # Try to preserve hierarchy by not combining
                        try:
                            static_mesh_options.set_editor_property('import_mesh_lo_ds', False)
                        except:
                            pass
                    
                    print(f"  ✓ Set combine_meshes={combine_meshes}")
                except Exception as e:
                    print(f"  ✗ Could not set combine_meshes: {e}")
            
            task.options = options
        
        # Execute import
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
        
        # Get the imported assets - find ALL StaticMesh assets
        imported_meshes = []
        if task.get_editor_property('imported_object_paths'):
            print(f"  Imported {len(task.get_editor_property('imported_object_paths'))} assets")
            for asset_path in task.get_editor_property('imported_object_paths'):
                asset = unreal.EditorAssetLibrary.load_asset(asset_path)
                if asset and isinstance(asset, unreal.StaticMesh):
                    print(f"  Found StaticMesh: {asset_path}")
                    imported_meshes.append(asset)
        
        if len(imported_meshes) == 0:
            print(f"  Warning: No StaticMesh found in imported assets")
            return None
        
        # Always try to use or create a Blueprint for consistency
        print(f"  Found {len(imported_meshes)} mesh(es)")
        
        # Get folder paths for Blueprint detection/creation
        first_mesh_path = imported_meshes[0].get_path_name()
        folder_path = '/'.join(first_mesh_path.split('/')[:-1])
        base_name = folder_path.split('/')[-1]
        parent_folder = '/'.join(folder_path.split('/')[:-1])
        
        # Try common Blueprint naming patterns (case variations)
        blueprint_names = [
            f"{base_name}_Blueprint",
            f"{base_name}_blueprint", 
            f"{base_name}_BP",
            f"BP_{base_name}"
        ]
        
        # Check in both the model folder and parent /Game/Imported folder
        folders_to_check = [folder_path, parent_folder]
        
        for check_folder in folders_to_check:
            print(f"  Looking for Blueprint in: {check_folder}")
            for bp_name in blueprint_names:
                bp_path = f"{check_folder}/{bp_name}"
                if unreal.EditorAssetLibrary.does_asset_exist(bp_path):
                    blueprint = unreal.EditorAssetLibrary.load_asset(bp_path)
                    if blueprint and isinstance(blueprint, unreal.Blueprint):
                        print(f"  ✓ Found existing Blueprint: {bp_path}")
                        return blueprint
        
        # No Blueprint found - create one with all imported meshes
        print(f"  No Blueprint found, creating one with {len(imported_meshes)} component(s)")
        blueprint = self._create_blueprint_with_meshes(imported_meshes, parent_folder, base_name)
        if blueprint:
            return blueprint
        
        # Fallback to first mesh if Blueprint creation fails
        print(f"  ⚠ Blueprint creation failed, using first mesh as StaticMeshActor fallback")
        return imported_meshes[0]
    
    def _create_blueprint_with_meshes(self, meshes, folder_path, base_name):
        """Create a Blueprint actor with multiple mesh components using actor-to-Blueprint conversion"""
        bp_name = f"{base_name}_Blueprint"
        bp_path = f"{folder_path}/{bp_name}"
        
        print(f"  Creating Blueprint with {len(meshes)} components at: {bp_path}")
        
        # Delete existing Blueprint if it exists
        if unreal.EditorAssetLibrary.does_asset_exist(bp_path):
            print(f"  Removing existing Blueprint: {bp_path}")
            unreal.EditorAssetLibrary.delete_asset(bp_path)
        
        try:
            # Create an empty Blueprint using BlueprintFactory
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
            blueprint_factory = unreal.BlueprintFactory()
            blueprint_factory.set_editor_property('parent_class', unreal.Actor)
            
            # Create the Blueprint asset
            blueprint = asset_tools.create_asset(
                asset_name=bp_name,
                package_path=folder_path,
                asset_class=unreal.Blueprint,
                factory=blueprint_factory
            )
            
            if not blueprint:
                print(f"  ✗ Failed to create Blueprint asset")
                return None
            
            print(f"  ✓ Created Blueprint: {bp_path}")
            
            # Add StaticMeshComponents for each mesh using SubobjectDataSubsystem
            subsys = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
            bfl = unreal.SubobjectDataBlueprintFunctionLibrary
            
            # Find the root component
            handles = subsys.k2_gather_subobject_data_for_blueprint(context=blueprint)
            root = None
            for h in handles:
                data = bfl.get_data(h)
                if bfl.is_root_component(data) or bfl.is_default_scene_root(data):
                    root = h
                    break
            
            if not root:
                print(f"  ✗ Could not find root component")
                return None
            
            print(f"  Adding {len(meshes)} mesh component(s)...")
            
            # Add each mesh as a StaticMeshComponent
            for i, mesh in enumerate(meshes):
                # Create component
                params = unreal.AddNewSubobjectParams(
                    parent_handle=root,
                    new_class=unreal.StaticMeshComponent,
                    blueprint_context=blueprint
                )
                new_handle, reason = subsys.add_new_subobject(params)
                
                if reason and not reason.is_empty():
                    print(f"    ✗ Failed to add component {i}: {reason}")
                    continue
                
                # Rename and configure
                comp_name = f"SMC_{mesh.get_name()}"
                subsys.rename_subobject(new_handle, comp_name)
                
                # Get template and set mesh
                data = bfl.get_data(new_handle)
                tmpl = bfl.get_object_for_blueprint(data, blueprint)
                tmpl.set_editor_property("static_mesh", mesh)
                tmpl.set_editor_property("mobility", unreal.ComponentMobility.STATIC)
                
                print(f"    ✓ Added component {i+1}/{len(meshes)}: {comp_name}")
            
            # Compile and save
            unreal.BlueprintEditorLibrary.compile_blueprint(blueprint)
            unreal.EditorAssetLibrary.save_loaded_asset(blueprint)
            
            print(f"  ✓ Blueprint created with {len(meshes)} component(s)")
            
            return blueprint
            
        except Exception as e:
            print(f"  ✗ Error creating Blueprint: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _spawn_static_mesh_actor(self, static_mesh_or_list):
        """Spawn a static mesh actor in the level - handles single mesh, Blueprint, or list of meshes"""
        
        # Check if it's a Blueprint
        if isinstance(static_mesh_or_list, unreal.Blueprint):
            print(f"  Spawning Blueprint actor")
            # Get the generated class from the Blueprint
            blueprint_class = static_mesh_or_list.generated_class()
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
                blueprint_class,
                unreal.Vector(*self.location),
                unreal.Rotator(*self.rotation)
            )
            
        elif isinstance(static_mesh_or_list, list):
            # This shouldn't happen anymore, but keep as fallback
            print(f"  Warning: Got mesh list instead of Blueprint, using first mesh")
            first_mesh = static_mesh_or_list[0]
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
                unreal.StaticMeshActor.static_class(),
                unreal.Vector(*self.location),
                unreal.Rotator(*self.rotation)
            )
            mesh_component = actor.get_component_by_class(unreal.StaticMeshComponent)
            if mesh_component:
                mesh_component.set_static_mesh(first_mesh)
            
        else:
            # Single mesh - use standard StaticMeshActor
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
                unreal.StaticMeshActor.static_class(),
                unreal.Vector(*self.location),
                unreal.Rotator(*self.rotation)
            )
            
            # Set the static mesh
            mesh_component = actor.get_component_by_class(unreal.StaticMeshComponent)
            if mesh_component:
                mesh_component.set_static_mesh(static_mesh_or_list)
        
        # Set scale
        if isinstance(self.scale, (list, tuple)) and len(self.scale) == 3:
            actor.set_actor_scale3d(unreal.Vector(*self.scale))
        else:
            # Uniform scale
            s = self.scale if isinstance(self.scale, (int, float)) else 1.0
            actor.set_actor_scale3d(unreal.Vector(s, s, s))
        
        return actor
    
    def _update_actor_transform(self, actor):
        """Update actor's transform"""
        actor.set_actor_location(
            unreal.Vector(*self.location),
            False,
            False
        )
        actor.set_actor_rotation(
            unreal.Rotator(*self.rotation),
            False
        )
        
        if isinstance(self.scale, (list, tuple)) and len(self.scale) == 3:
            actor.set_actor_scale3d(unreal.Vector(*self.scale))
        else:
            s = self.scale if isinstance(self.scale, (int, float)) else 1.0
            actor.set_actor_scale3d(unreal.Vector(s, s, s))
