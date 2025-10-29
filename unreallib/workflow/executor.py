"""
Workflow executor - runs tasks in dependency order
"""

from typing import Dict, Any, List, Optional
from .graph import WorkflowGraph
from .task import Task, TaskResult, TaskStatus
from .config import WorkflowConfig


class WorkflowExecutor:
    """
    Executes workflow tasks in dependency order
    
    Manages execution context and handles task outputs/failures.
    """
    
    def __init__(self, graph: WorkflowGraph, config: Optional[WorkflowConfig] = None):
        """
        Initialize executor
        
        Args:
            graph: WorkflowGraph containing tasks and dependencies
            config: Optional WorkflowConfig for execution behavior
        """
        self.graph = graph
        self.config = config or WorkflowConfig()
        self.context: Dict[str, Any] = {}
        self.results: Dict[str, TaskResult] = {}
    
    def execute(self, initial_context: Dict[str, Any] = None) -> Dict[str, TaskResult]:
        """
        Execute all tasks in the workflow
        
        Args:
            initial_context: Initial context data to pass to first tasks
            
        Returns:
            Dictionary mapping task names to their TaskResults
        """
        # Initialize context
        self.context = initial_context or {}
        self.results = {}
        
        # Add config to context
        self.context['workflow_config'] = self.config
        
        # Clear level if configured
        if self.config.clear_before_execute:
            print("\n⚙️  Config: Clearing level before execution...")
            self._clear_level()
        
        # Validate workflow
        self.graph.validate()
        
        # Get execution order
        execution_order = self.graph.get_execution_order()
        
        print("\n" + "=" * 60)
        print("Starting Workflow Execution")
        print("=" * 60)
        print(f"Config: {self.config}")
        print(f"Tasks: {len(execution_order)}")
        print(f"Order: {' → '.join(execution_order)}")
        print("=" * 60 + "\n")
        
        # Execute tasks in order
        for task_name in execution_order:
            task = self.graph[task_name]
            
            # Check if dependencies succeeded
            deps = self.graph.dependencies[task_name]
            if not self._check_dependencies(deps):
                # Skip task if dependencies failed
                result = TaskResult(
                    status=TaskStatus.SKIPPED,
                    error="Dependency failed"
                )
                self.results[task_name] = result
                print(f"[{task_name}] Skipped (dependency failed)")
                continue
            
            # Execute task
            result = task.run(self.context)
            self.results[task_name] = result
            
            # Add task output to context for downstream tasks
            if result.success and result.output is not None:
                self.context[task_name] = result.output
        
        # Save level if configured
        if self.config.save_level_after:
            print("\n⚙️  Config: Saving level after execution...")
            self._save_level()
        
        # Print summary
        self._print_summary()
        
        return self.results
    
    def _clear_level(self):
        """Clear all actors from level (pre-execution)"""
        try:
            from unreallib import level
            initial_count = level.get_actor_count()
            level.clear_all_actors()
            final_count = level.get_actor_count()
            deleted = initial_count - final_count
            print(f"  ✓ Cleared {deleted} actors from level\n")
        except Exception as e:
            print(f"  ✗ Failed to clear level: {e}\n")
    
    def _save_level(self):
        """Save current level (post-execution)"""
        try:
            from unreallib import level
            level.save_current_level()
            print("  ✓ Level saved\n")
        except Exception as e:
            print(f"  ✗ Failed to save level: {e}\n")
    
    def _check_dependencies(self, deps: List[str]) -> bool:
        """
        Check if all dependencies succeeded
        
        Args:
            deps: List of dependency task names
            
        Returns:
            True if all dependencies succeeded
        """
        for dep_name in deps:
            if dep_name not in self.results:
                return False
            if not self.results[dep_name].success:
                return False
        return True
    
    def _print_summary(self):
        """Print execution summary"""
        print("\n" + "=" * 60)
        print("Workflow Execution Summary")
        print("=" * 60)
        
        success_count = sum(1 for r in self.results.values() if r.status == TaskStatus.SUCCESS)
        failed_count = sum(1 for r in self.results.values() if r.status == TaskStatus.FAILED)
        skipped_count = sum(1 for r in self.results.values() if r.status == TaskStatus.SKIPPED)
        total_time = sum(r.execution_time for r in self.results.values())
        
        print(f"Total Tasks: {len(self.results)}")
        print(f"  Success: {success_count}")
        print(f"  Failed:  {failed_count}")
        print(f"  Skipped: {skipped_count}")
        print(f"Total Time: {total_time:.3f}s")
        print("=" * 60 + "\n")
    
    def get_task_output(self, task_name: str) -> Any:
        """
        Get output from a completed task
        
        Args:
            task_name: Name of task
            
        Returns:
            Task output if successful, None otherwise
        """
        if task_name in self.context:
            return self.context[task_name]
        return None
