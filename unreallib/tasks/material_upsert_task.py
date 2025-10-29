"""
MaterialUpsertTask - Ensures a parameterized material instance exists and is available to later tasks.

Strategy:
- Try to load a target material instance asset path (e.g. /Game/Workflow/MI_RuntimeColorBase)
- If it does not exist and allow_create=True, attempt to create it from a specified parent master material
- Validate that the expected vector parameter exists (or create a simple one if creating)
- Store the material path in task output and workflow context under key 'material_path'

NOTE: Creating new materials requires running inside the Unreal Editor (not cooked runtime).
"""
from unreallib.workflow.task import Task, TaskResult, TaskStatus
from typing import Optional

class MaterialUpsertTask(Task):
    def __init__(
        self,
        name: str,
        material_path: str = "/Game/Workflow/MI_RuntimeColorBase",
        parent_material_path: str = "/Engine/BasicShapes/BasicShapeMaterial",
        vector_parameter_name: str = "Color",
        allow_create: bool = True
    ):
        super().__init__(
            name,
            material_path=material_path,
            parent_material_path=parent_material_path,
            vector_parameter_name=vector_parameter_name,
            allow_create=allow_create
        )
        self.material_path = material_path
        self.parent_material_path = parent_material_path
        self.vector_parameter_name = vector_parameter_name
        self.allow_create = allow_create

    def execute(self, context: dict) -> TaskResult:
        import unreal

        editor_asset_lib = unreal.EditorAssetLibrary
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        existing = editor_asset_lib.does_asset_exist(self.material_path)

        created = False
        material_instance = None

        if existing:
            material_instance = editor_asset_lib.load_asset(self.material_path)
        else:
            if not self.allow_create:
                return TaskResult(
                    status=TaskStatus.FAILED,
                    error=f"Material not found and creation disabled: {self.material_path}",
                    metadata={
                        'task_type': 'material_upsert',
                        'material_path': self.material_path,
                        'created': False
                    }
                )
            # Create directory if needed
            pkg_path = "/".join(self.material_path.split("/")[:-1])
            if not editor_asset_lib.does_directory_exist(pkg_path):
                editor_asset_lib.make_directory(pkg_path)
            parent = editor_asset_lib.load_asset(self.parent_material_path)
            if not parent:
                return TaskResult(
                    status=TaskStatus.FAILED,
                    error=f"Parent material not found: {self.parent_material_path}",
                    metadata={'task_type': 'material_upsert'}
                )
            asset_name = self.material_path.split("/")[-1]
            package_path = pkg_path
            material_instance = asset_tools.create_asset(
                asset_name=asset_name,
                package_path=package_path,
                asset_class=unreal.MaterialInstanceConstant,
                factory=unreal.MaterialInstanceConstantFactoryNew(),
                calling_context=None
            )
            material_instance.set_editor_property('parent', parent)
            created = True

        # Validate parameter exists; if not, we warn (cannot add parameter dynamically without editing graph)
        param_collection = unreal.MaterialEditingLibrary
        # We cannot truly add new scalar/vector parameters to a compiled material graph at runtime unless editing parent.
        # So we just log if missing.
        vec_name = self.vector_parameter_name
        has_param = False
        try:
            # Query parameters (works for instances)
            for p in unreal.MaterialEditingLibrary.get_vector_parameter_names(material_instance):
                if p == vec_name:
                    has_param = True
                    break
        except Exception:
            pass
        if not has_param:
            unreal.log_warning(f"[MaterialUpsertTask] Vector parameter '{vec_name}' not found in {self.material_path}. Colors may not apply.")

        # Store in context so downstream color tasks can use it
        context['material_path'] = self.material_path
        context['material_vector_parameter'] = vec_name

        return TaskResult(
            status=TaskStatus.SUCCESS,
            output={
                'material_path': self.material_path,
                'created': created,
                'vector_parameter_name': vec_name,
                'has_parameter': has_param
            },
            metadata={
                'task_type': 'material_upsert'
            }
        )
