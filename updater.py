import os
import requests
import shutil
from utils import resource_path

# Define URLs for the version and the executable
VERSION_URL = "https://raw.githubusercontent.com/Karkess/TextRPG/main/version.txt"
REPO_URL = "https://github.com/Karkess/TextRPG/archive/refs/heads/main.zip"
LOCAL_VERSION_FILE = "./version.txt"
EXCLUDED_FOLDERS = ["./dist/saves", "./saves"]  # Folders to exclude from deletion

# Function to check for updates
def check_for_update():
    try:
        # Get the latest version from GitHub
        response = requests.get(VERSION_URL)
        response.raise_for_status()
        latest_version = response.text.strip()

        # Read the local version from the file
        if os.path.exists(LOCAL_VERSION_FILE):
            with open(LOCAL_VERSION_FILE, "r") as file:
                current_version = file.read().strip()
        else:
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
        # Print the current working directory for debugging
        print("Current working directory:", os.getcwd())

        # Ensure that the ./dist folder exists, use resource_path for proper path handling
        dist_folder = resource_path("./dist")
        if not os.path.exists(dist_folder):
            os.makedirs(dist_folder)
            print(f"Created {dist_folder} folder.")

        print("Downloading the latest version...")
        response = requests.get(REPO_URL, stream=True)
        response.raise_for_status()

        # Save the downloaded zip file to ./dist using resource_path
        zip_path = resource_path(os.path.join(dist_folder, "latest.zip"))
        with open(zip_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)

        print("Download complete. Extracting files...")

        # Extract the zip file to ./dist/latest_update/ using resource_path
        extract_path = resource_path(os.path.join(dist_folder, "latest_update"))
        shutil.unpack_archive(zip_path, extract_path)

        # Locate the extracted root folder (e.g., ./dist/latest_update/TextRPG-main/)
        extracted_root_folder = os.path.join(extract_path, "TextRPG-main")

        # Remove all old files except the excluded ones (./dist/saves/ and ./saves)
        for root, dirs, files in os.walk(".", topdown=True):
            dirs[:] = [d for d in dirs if os.path.join(root, d) not in EXCLUDED_FOLDERS]
            for file in files:
                file_path = os.path.join(root, file)
                if not any(excluded in file_path for excluded in EXCLUDED_FOLDERS):
                    os.remove(file_path)

        # Move files from the extracted root folder to the current directory
        for root, dirs, files in os.walk(extracted_root_folder):
            for file in files:
                src_file = os.path.join(root, file)
                relative_path = os.path.relpath(src_file, extracted_root_folder)
                dest_file = resource_path(os.path.join(".", relative_path))
                dest_dir = os.path.dirname(dest_file)
                os.makedirs(dest_dir, exist_ok=True)
                shutil.move(src_file, dest_file)

        # Clean up: remove the zip file and extracted update folder
        os.remove(zip_path)
        shutil.rmtree(extract_path)

        print("Update installed successfully.")
    except Exception as e:
        print(f"Error during update: {e}")

        print("Update installed successfully.")
    except Exception as e:
        print(f"Error during update: {e}")

if __name__ == "__main__":
    check_for_update()
