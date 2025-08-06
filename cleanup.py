import os
import shutil
import sys
import platform

def print_header(text):
    """Print a header with the given text"""
    print("\n" + "=" * 70)
    print(f" {text} ".center(70, "="))
    print("=" * 70)

def cleanup():
    """Clean up the project directory and organize final files"""
    # Get project root directory (now the current directory)
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Clear screen
    os.system('cls' if platform.system().lower() == 'windows' else 'clear')
    
    print_header("Taskbar Manager - Project Cleanup")
    print("Organizing project files...\n")
    
    # Create directory structure
    final_dir = os.path.join(project_root, "final")
    src_dir = os.path.join(project_root, "src")
    
    # Create directories if they don't exist
    for directory in [final_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created {directory} directory")
    
    # Look for the executable in common locations
    executable_found = False
    locations = [
        os.path.join(project_root, "TaskbarManager_1.0.0.exe"),
        os.path.join(project_root, "dist", "TaskbarManager_1.0.0.exe"),
        os.path.join(project_root, "dist", "TaskbarManager_1.0.0_windows.exe")
    ]
    
    # Ensure the final executable exists or is copied before cleaning
    for location in locations:
        if os.path.exists(location):
            try:
                final_exe_path = os.path.join(final_dir, "TaskbarManager.exe")
                # Only copy if executable doesn't exist in final dir or is different
                if not os.path.exists(final_exe_path) or os.path.getsize(location) != os.path.getsize(final_exe_path):
                    shutil.copy2(location, final_exe_path)
                print(f"✅ Copied executable to final directory")
                else:
                    print(f"✅ Executable already exists in final directory")
                executable_found = True
                break
            except Exception as e:
                print(f"❌ Failed to copy executable: {str(e)}")
    
    if not executable_found:
        print("⚠️ No executable found to copy")
    
    # Remove temporary files
    print_header("Cleaning Build Files")
    
    # Directories to completely remove
    dirs_to_remove = [
        os.path.join(project_root, "build"),
        os.path.join(project_root, "dist")
    ]
    
    # Files to remove
    temp_files = [
        os.path.join(project_root, "taskbar_manager.manifest"),
        os.path.join(project_root, "version_info.txt"),
        os.path.join(project_root, "add_defender_exclusion.ps1")
    ]
    
    # Add all .spec files
    temp_files.extend([os.path.join(project_root, f) for f in os.listdir(project_root) if f.endswith('.spec')])
    
    # Clean build and dist directories
    cleaned_count = 0
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"✅ Completely removed directory: {os.path.basename(dir_path)}/")
                cleaned_count += 1
            except Exception as e:
                print(f"⚠️ Could not remove directory {os.path.basename(dir_path)}: {str(e)}")
    
    # Clean temporary files
    for file in temp_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✅ Removed temporary file: {os.path.basename(file)}")
                cleaned_count += 1
            except Exception as e:
                print(f"⚠️ Could not remove {os.path.basename(file)}: {str(e)}")
    
    # Clean __pycache__ directories
    pycache_dirs = []
    for root, dirs, files in os.walk(project_root):
        for dir in dirs:
            if dir == '__pycache__':
                pycache_dirs.append(os.path.join(root, dir))
    
    for pycache in pycache_dirs:
        try:
            shutil.rmtree(pycache)
            print(f"✅ Removed __pycache__ directory in: {os.path.dirname(pycache)}")
            cleaned_count += 1
        except Exception as e:
            print(f"⚠️ Could not remove {pycache}: {str(e)}")
    
    if cleaned_count == 0:
        print("✅ No files found to clean!")
    
    # Show final structure
    print_header("Project Structure")
    print("Your project has been organized:\n")
    print(f"├─ src/")
    print(f"│  └─ taskbar_manager.py")
    print(f"├─ build.py")
    print(f"├─ cleanup.py")
    print(f"├─ requirements.txt")
    print(f"├─ README.md")
    print(f"└─ final/")
    print(f"   └─ TaskbarManager.exe (Ready-to-use application)")
    
    print("\nYou can distribute the executable from the 'final' directory.")
    print("All build files have been removed to save disk space.")
    print("Run build.py again if you need to rebuild the application.")

if __name__ == "__main__":
    cleanup() 