import os
import fnmatch
import subprocess

def run_updater():
    print("Checking for updates...")
    subprocess.call(['python', 'updater.py'])

def build_executable():
    print("Building new executable...")

    # Path to the main Python script (entry point of your game)
    main_script = "Game.py"

    # Patterns to exclude using wildcards
    exclude_patterns = ['.git*', '__pycache__*', 'build*', 'dist*']

    # Automatically detect folders and files to include, excluding unnecessary folders
    def find_folders_to_include(base_path):
        folders = []
        for root, dirs, _ in os.walk(base_path):
            # Filter out excluded directories from the current level
            dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in exclude_patterns)]
            for dir in dirs:
                folders.append(os.path.join(root, dir))
        return folders

    # Automatically detect files in the root directory to include
    def find_files_to_include(base_path):
        files = []
        for root, _, filenames in os.walk(base_path):
            for file in filenames:
                if file.endswith(".py") and not any(fnmatch.fnmatch(file, pattern) for pattern in exclude_patterns):
                    # Add relative paths for the files
                    files.append(os.path.join(root, file))
        return files

    # Base command for PyInstaller
    command = [
        "pyinstaller",
        "--onefile",
        "--noconfirm",  # Automatically overwrite the previous build
        "--hidden-import=platform",  # Ensure the platform module is included
        "--hidden-import=os",        # Ensure os module is included
        "--hidden-import=requests"   # Ensure requests is included
    ]

    # Add all files in the root directory and subfolders
    files_to_include = find_files_to_include(".")
    for file in files_to_include:
        # Ensure the correct relative paths for PyInstaller's --add-data
        relative_path = os.path.relpath(file, ".")
        command.append(f"--add-data={relative_path};.")

    # Add all subfolders
    folders_to_include = find_folders_to_include(".")
    for folder in folders_to_include:
        relative_folder = os.path.relpath(folder, ".")
        command.append(f"--add-data={relative_folder}/*;{relative_folder}")

    # Append the main script as the last argument
    command.append(main_script)

    # Join the command into a string and run it
    command_str = " ".join(command)
    print("Running command:", command_str)

    # Run the PyInstaller command
    subprocess.run(command_str, shell=True)

if __name__ == "__main__": 
    build_executable()  # Build the new executable
