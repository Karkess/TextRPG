import os
import requests
import shutil
from utils import resource_path

# Define URLs for the version and the executable
VERSION_URL = "https://raw.githubusercontent.com/Karkess/TextRPG/main/version.txt"
REPO_URL = "https://github.com/Karkess/TextRPG/archive/refs/heads/main.zip"

# Correct paths based on the current directory
BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), os.pardir))  # One level up from ./dist
LOCAL_VERSION_FILE = os.path.join(BASE_DIR, "version.txt")
LOCAL_EXECUTABLE = os.path.join(BASE_DIR, "dist", "Game.exe")

EXCLUDED_FOLDERS = [os.path.join(BASE_DIR, "dist", "saves"), os.path.join(BASE_DIR, "saves"), os.path.join(BASE_DIR, ".git")]

# Function to check for updates
def check_for_update():
    try:
        print(f"Current working directory: {os.getcwd()}")
        print(f"Base directory: {BASE_DIR}")
        print(f"Local version file path: {LOCAL_VERSION_FILE}")

        # Get the latest version from GitHub
        response = requests.get(VERSION_URL)
        response.raise_for_status()
        latest_version = response.text.strip()
        print(f"Latest version from GitHub: {latest_version}")

        # Read the local version from the file
        if os.path.exists(LOCAL_VERSION_FILE):
            with open(LOCAL_VERSION_FILE, "r") as file:
                current_version = file.read().strip()
            print(f"Local version: {current_version}")
        else:
            print(f"Local version file not found. Assuming version 0.0.0.")
            current_version = "0.0.0"

        # Compare versions
        if current_version != latest_version:
            print(f"New version available: {latest_version}.")
            update_prompt = input("Do you want to download and install the update? (y/n): ").strip().lower()
            if update_prompt == 'y':
                download_and_install_update()
            else:
                print("Continuing without updating...")
        else:
            print("You have the latest version.")
    except Exception as e:
        print(f"Error while checking for updates: {e}")

# Function to download and install the latest update
def download_and_install_update():
    try:
        print("Downloading the latest version...")
        response = requests.get(REPO_URL, stream=True)
        response.raise_for_status()

        # Save the downloaded zip file to ./dist
        zip_path = os.path.join(BASE_DIR, "dist", "latest.zip")
        with open(zip_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)

        print(f"Download complete. Zip file saved at {zip_path}")
        
        # Extract the zip file to ./dist/latest_update/
        extract_path = os.path.join(BASE_DIR, "dist", "latest_update")
        shutil.unpack_archive(zip_path, extract_path)

        # Locate the extracted root folder (e.g., ./dist/latest_update/TextRPG-main/)
        extracted_root_folder = os.path.join(extract_path, "TextRPG-main")
        print(f"Extracted root folder: {extracted_root_folder}")

        # Remove all old files except the excluded ones (e.g., saves folders and .git)
        for root, dirs, files in os.walk(BASE_DIR, topdown=True):
            dirs[:] = [d for d in dirs if os.path.join(root, d) not in EXCLUDED_FOLDERS]
            for file in files:
                file_path = os.path.join(root, file)
                if not any(excluded in file_path for excluded in EXCLUDED_FOLDERS):
                    os.remove(file_path)
                    print(f"Removing old file: {file_path}")

        # Move files from the extracted root folder to the base directory
        for root, dirs, files in os.walk(extracted_root_folder):
            for file in files:
                src_file = os.path.join(root, file)
                relative_path = os.path.relpath(src_file, extracted_root_folder)
                dest_file = os.path.join(BASE_DIR, relative_path)
                dest_dir = os.path.dirname(dest_file)
                os.makedirs(dest_dir, exist_ok=True)
                shutil.move(src_file, dest_file)
                print(f"Moving {src_file} to {dest_file}")

        # Clean up: remove the zip file and extracted update folder
        os.remove(zip_path)
        shutil.rmtree(extract_path)

        print("Update installed successfully.")
    except Exception as e:
        print(f"Error during update: {e}")

if __name__ == "__main__":
    check_for_update()
