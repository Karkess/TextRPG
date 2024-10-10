import os
import requests
import shutil

# Define URLs for the version and the executable
VERSION_URL = "https://raw.githubusercontent.com/Karkess/TextRPG/main/version.txt"  # Update this with your repo's actual raw version.txt URL
EXECUTABLE_URL = "https://github.com/Karkess/TextRPG/releases/latest/download/Game.exe"  # Update with the location of your compiled .exe file
LOCAL_VERSION_FILE = "./version.txt"
LOCAL_EXECUTABLE = "./Game.exe"  # Path to your local executable

# Function to check for updates
def check_for_update():
    # Get the latest version from GitHub
    try:
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
            print(f"New version available: {latest_version}. Downloading update...")
            download_update()
        else:
            print("You have the latest version.")
    except Exception as e:
        print(f"Error while checking for updates: {e}")

# Function to download and update the game executable
def download_update():
    try:
        # Download the latest executable
        with requests.get(EXECUTABLE_URL, stream=True) as r:
            r.raise_for_status()
            with open("Game_new.exe", "wb") as f:
                shutil.copyfileobj(r.raw, f)

        # Replace the old executable with the new one
        if os.path.exists(LOCAL_EXECUTABLE):
            os.remove(LOCAL_EXECUTABLE)
        os.rename("Game_new.exe", LOCAL_EXECUTABLE)
        print("Update completed successfully.")
    except Exception as e:
        print(f"Error during download: {e}")

if __name__ == "__main__":
    check_for_update()
