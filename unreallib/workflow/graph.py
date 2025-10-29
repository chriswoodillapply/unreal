"""
DAG (Directed Acyclic Graph) for workflow task dependencies
"""

from typing import Dict, List, Set
from .task import Task


class WorkflowGraph:
    """
    Represents a DAG of tasks with dependencies
    
    Manages task dependencies and provides topological sorting
    for correct execution order.
    """
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.dependencies: Dict[str, List[str]] = {}
    
    def add_task(self, task: Task, depends_on: List[str] = None):
        """
        Add a task to the workflow
        
        Args:
            task: Task instance to add
            depends_on: List of task names this task depends on
        """
        if task.name in self.tasks:
            raise ValueError(f"Task '{task.name}' already exists in workflow")
        
        self.tasks[task.name] = task
        self.dependencies[task.name] = depends_on or []
        
        # Validate dependencies exist
        for dep_name in self.dependencies[task.name]:
            if dep_name not in self.tasks:
                raise ValueError(
                    f"Task '{task.name}' depends on '{dep_name}' "
                    f"which hasn't been added to workflow yet"
                )
    
    def get_execution_order(self) -> List[str]:
        """
        Get topologically sorted execution order
        
        Returns:
            List of task names in execution order
            
        Raises:
            ValueError: If circular dependency detected
        """
        # Kahn's algorithm for topological sort
        in_degree = {name: 0 for name in self.tasks}
        
        # Calculate in-degrees
        for task_name, deps in self.dependencies.items():
            for dep in deps:
                in_degree[task_name] += 1
        
        # Queue of tasks with no dependencies
        queue = [name for name, degree in in_degree.items() if degree == 0]
        execution_order = []
        
        while queue:
            # Process task with no remaining dependencies
            current = queue.pop(0)
            execution_order.append(current)
            
            # Reduce in-degree for dependent tasks
            for task_name, deps in self.dependencies.items():
                if current in deps:
                    in_degree[task_name] -= 1
                    if in_degree[task_name] == 0:
                        queue.append(task_name)
        
        # Check for cycles
        if len(execution_order) != len(self.tasks):
            raise ValueError("Circular dependency detected in workflow!")
        
        return execution_order
    
    def validate(self) -> bool:
        """
        Validate the workflow graph
        
        Returns:
            True if valid
            
        Raises:
            ValueError: If validation fails
        """
        # Check all dependencies exist
        for task_name, deps in self.dependencies.items():
            for dep in deps:
                if dep not in self.tasks:
                    raise ValueError(
                        f"Task '{task_name}' depends on non-existent task '{dep}'"
                    )
        
        # Check for cycles by attempting topological sort
        try:
            self.get_execution_order()
            return True
        except ValueError as e:
            raise ValueError(f"Workflow validation failed: {e}")
    
    def visualize(self) -> str:
        """
        Generate a text visualization of the workflow
        
        Returns:
            String representation of the DAG
        """
        lines = ["Workflow Graph:", "=" * 60]
        
        execution_order = self.get_execution_order()
        
        for task_name in execution_order:
            task = self.tasks[task_name]
            deps = self.dependencies[task_name]
            
            if deps:
                dep_str = ", ".join(deps)
                lines.append(f"{task_name} <- [{dep_str}]")
            else:
                lines.append(f"{task_name} (root)")
        
        lines.append("=" * 60)
        return "\n".join(lines)
    
    def __len__(self) -> int:
        return len(self.tasks)
    
    def __contains__(self, task_name: str) -> bool:
        return task_name in self.tasks
    
    def __getitem__(self, task_name: str) -> Task:
        return self.tasks[task_name]
