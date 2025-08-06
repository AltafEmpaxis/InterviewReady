import os
import platform
import subprocess
import time
import threading
import shutil
import sys
import datetime

VERSION = "1.0.0"

class LoadingAnimation:
    def __init__(self):
        self.is_running = False
        self.animation_thread = None

    def start(self, message="Building"):
        self.is_running = True
        self.animation_thread = threading.Thread(target=self._animate, args=(message,))
        self.animation_thread.start()

    def stop(self):
        self.is_running = False
        if self.animation_thread:
            self.animation_thread.join()
        print("\r" + " " * 70 + "\r", end="", flush=True)

    def _animate(self, message):
        animation = "|/-\\"
        idx = 0
        while self.is_running:
            print(f"\r{message} {animation[idx % len(animation)]}", end="", flush=True)
            idx += 1
            time.sleep(0.1)

def progress_bar(progress, total, prefix="", length=50):
    filled = int(length * progress // total)
    bar = "█" * filled + "░" * (length - filled)
    percent = f"{100 * progress / total:.1f}"
    print(f"\r{prefix} |{bar}| {percent}% Complete", end="", flush=True)
    if progress == total:
        print()

def simulate_progress(message, duration=0.5, steps=10):
    print(f"\033[94m{message}\033[0m")
    for i in range(steps + 1):
        time.sleep(duration / steps)
        progress_bar(i, steps, prefix="Progress:", length=40)

def print_logo():
    """Print a simple ASCII art logo"""
    print(r"""
  _______          _    _                 __  __                                 
 |__   __|        | |  | |               |  \/  |                                
    | | __ _ ___  | |__| |_   ___ __ ___|_/\ \_| __ _ _ __   __ _  __ _  ___ _ __
    | |/ _` / __| |  __  | | | | '_ ` _ \ '  ` / _` | '_ \ / _` |/ _` |/ _ \ '__|
    | | (_| \__ \ | |  | | |_| | | | | | | |\/| (_| | | | | (_| | (_| |  __/ |   
    |_|\__,_|___/ |_|  |_|\__,_|_| |_| |_\_/\_/\__,_|_| |_|\__,_|\__, |\___|_|   
                                                                  __/ |          
                                                                 |___/           
    """)

def clean_temp_files():
    """Clean temporary files but keep build and dist directories"""
    print("\033[93m🧹 Cleaning temporary files...\033[0m")
    
    # Get root project directory (now the current directory)
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Files to remove
    temp_files = [
        os.path.join(project_root, 'taskbar_manager.manifest'),
        os.path.join(project_root, 'version_info.txt'),
        os.path.join(project_root, 'add_defender_exclusion.ps1')
    ]
    
    # Add all .spec files in the root directory
    temp_files.extend([os.path.join(project_root, f) for f in os.listdir(project_root) if f.endswith('.spec')])
    
    for file in temp_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"\033[93m  ✓ Removed file: {file}\033[0m")
            except Exception as e:
                print(f"\033[91m  ✗ Error removing {file}: {str(e)}\033[0m")

def create_manifest_file():
    """Create a manifest file for the Windows application"""
    manifest_content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity version="1.0.0.0" processorArchitecture="*" name="TaskbarManager" type="win32"/>
  <description>Taskbar Manager Application</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="asInvoker" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">
    <application>
      <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/>
    </application>
  </compatibility>
</assembly>"""
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    manifest_file = os.path.join(project_root, "taskbar_manager.manifest")
    with open(manifest_file, "w") as f:
        f.write(manifest_content)
    return manifest_file

def create_version_file():
    """Create a version info file for the executable"""
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    version_content = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [StringStruct(u'CompanyName', u'TaskbarManager'),
          StringStruct(u'FileDescription', u'Windows Taskbar Manager'),
          StringStruct(u'FileVersion', u'{VERSION}'),
          StringStruct(u'InternalName', u'taskbar_manager'),
          StringStruct(u'LegalCopyright', u'(c) {current_date}. All rights reserved.'),
          StringStruct(u'OriginalFilename', u'TaskbarManager.exe'),
          StringStruct(u'ProductName', u'Taskbar Manager'),
          StringStruct(u'ProductVersion', u'{VERSION}')])
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    version_file = os.path.join(project_root, "version_info.txt")
    with open(version_file, "w", encoding="utf-8") as f:
        f.write(version_content)
    return version_file

def create_directory_structure():
    """Create necessary directories if they don't exist"""
    # Get the root directory (now the current directory)
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Create final directory if it doesn't exist
    final_dir = os.path.join(project_root, 'final')
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)
        print("\033[93m✓ Created final directory\033[0m")

def build():
    """Build the TaskbarManager application"""
    # Get project root directory (now the current directory)
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Clear screen and show logo
    os.system('cls' if platform.system().lower() == 'windows' else 'clear')
    print_logo()
    
    # Clean temp files only
    clean_temp_files()
    
    # Create directory structure
    create_directory_structure()
    
    print(f"\033[93m📦 Building Taskbar Manager v{VERSION}\033[0m")
    simulate_progress("Preparing build environment...")
    
    # Create necessary files
    manifest_file = create_manifest_file()
    version_file = create_version_file()
    
    # Source file path (now in src directory from root)
    source_file = os.path.join("src", "taskbar_manager.py")
        
    # Start build animation
    loading = LoadingAnimation()
    loading.start("Building Taskbar Manager")
    
    try:
        # Build command
        build_command = [
            'python', '-m', 'PyInstaller',
            '--name', f'TaskbarManager_{VERSION}',
            '--onefile',
            '--windowed',
            '--clean',
            '--noconfirm',
            '--manifest', manifest_file,
            '--version-file', version_file,
            '--disable-windowed-traceback',
            '--noupx',
            source_file
        ]
        
        # Execute build
        process = subprocess.Popen(
            build_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        stdout, stderr = process.communicate()
        loading.stop()
        
        # Check if build was successful
        output_path = os.path.join('dist', f'TaskbarManager_{VERSION}.exe')
        if os.path.exists(output_path):
            print(f"\n\033[92m✅ Build completed!")
            print(f"📦 Executable created: {output_path}\033[0m")
            
            # Copy to final directory
            final_exe = os.path.join('final', "TaskbarManager.exe")
            shutil.copy2(output_path, final_exe)
            print(f"\033[92m✅ Copied to {final_exe}\033[0m")
            
            simulate_progress("Finalizing...", duration=0.3)
            print(f"\033[92m✨ Build finished! You can find your executable in: final/TaskbarManager.exe\033[0m")
            
            # Clean temp files but keep build and dist folders
            clean_temp_files()
            return True
        else:
            print("\n\033[91m❌ Build failed: Executable not created\033[0m")
            if stdout:
                print("\033[93mOutput:\033[0m")
                print(stdout[:500] + "..." if len(stdout) > 500 else stdout)
            if stderr:
                print("\033[91mErrors:\033[0m")
                print(stderr[:500] + "..." if len(stderr) > 500 else stderr)
            return False
            
    except Exception as e:
        loading.stop()
        print(f"\n\033[91m❌ Build error: {str(e)}\033[0m")
        return False

if __name__ == "__main__":
    if build():
        print("\n\033[92m✅ Process completed successfully!\033[0m")
    else:
        print("\n\033[91m❌ Process failed.\033[0m")
        sys.exit(1) 