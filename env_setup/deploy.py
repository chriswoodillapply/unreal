"""
Deploy Script - Copy latest libraries to target Unreal project

Copies unreallib, workflows, examples, and remotecontrol to a target project.
Useful for updating existing projects with latest code.

Usage:
    python deploy.py <target_project_path>
    python deploy.py "C:/Users/cwood/Documents/Unreal Projects/Test1"
"""

import sys
import shutil
from pathlib import Path


def deploy_to_project(target_project_path: str):
    """
    Deploy latest libraries to target project
    
    Args:
        target_project_path: Path to target Unreal project root
    """
    # Convert to Path
    target_project = Path(target_project_path)
    
    if not target_project.exists():
        print(f"❌ Error: Target project not found: {target_project}")
        return False
    
    # Get source directory (this script's parent's parent)
    source_scripts = Path(__file__).parent.parent
    target_scripts = target_project / "scripts"
    
    # Create scripts directory if it doesn't exist
    target_scripts.mkdir(exist_ok=True)
    
    print("=" * 70)
    print("DEPLOYING LATEST LIBRARIES")
    print("=" * 70)
    print(f"\nSource: {source_scripts}")
    print(f"Target: {target_scripts}\n")
    
    # List of directories to copy
    directories_to_copy = [
        ('unreallib', 'Core library with actors, materials, workflow system'),
        ('workflows', 'JSON workflow definitions'),
        ('examples', 'Example scripts'),
        ('remotecontrol', 'Remote control module'),
    ]
    
    success_count = 0
    
    for dir_name, description in directories_to_copy:
        source_dir = source_scripts / dir_name
        target_dir = target_scripts / dir_name
        
        if not source_dir.exists():
            print(f"⚠️  Skipping {dir_name}: Source not found")
            continue
        
        try:
            # Remove target if it exists (for clean copy)
            if target_dir.exists():
                print(f"🗑️  Removing old {dir_name}...")
                shutil.rmtree(target_dir)
            
            # Copy directory
            print(f"📦 Copying {dir_name}...", end=" ")
            shutil.copytree(source_dir, target_dir)
            
            # Count files
            file_count = sum(1 for _ in target_dir.rglob('*.py'))
            print(f"✓ ({file_count} Python files)")
            print(f"   {description}")
            
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error copying {dir_name}: {e}")
    
    print("\n" + "=" * 70)
    print(f"DEPLOYMENT COMPLETE: {success_count}/{len(directories_to_copy)} directories copied")
    print("=" * 70)
    
    # Show next steps
    print("\n📋 Next Steps:")
    print(f"   1. Open Unreal project: {target_project.name}")
    print("   2. Test with: python -m remotecontrol examples/run_workflow.py --method file")
    print("   3. Check workflows folder for available JSON workflows")
    
    return success_count == len(directories_to_copy)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python deploy.py <target_project_path>")
        print("\nExample:")
        print('  python deploy.py "C:/Users/cwood/Documents/Unreal Projects/Test1"')
        print('  python deploy.py "../Test1"')
        sys.exit(1)
    
    target_path = sys.argv[1]
    success = deploy_to_project(target_path)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
