import os
import platform
import re
import sys
import json
# utils.py

# Reset all attributes
RESET = "\033[0m"

# Text styles
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
INVERT = "\033[7m"
HIDDEN = "\033[8m"
STRIKETHROUGH = "\033[9m"
DOUBLE_UNDERLINE = "\033[21m"

# Foreground (Text) colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Bright Foreground colors
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Background colors
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

# Bright Background colors
BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"

# Function to replace placeholders with actual ANSI escape codes
def apply_text_formatting(text):
    # Regex pattern to match placeholders in the form {PLACEHOLDER}
    pattern = r"\{([A-Z_]+)\}"

    # Function to replace each match with the corresponding ANSI escape code from utils
    def replace_match(match):
        placeholder = match.group(1)  # Extract the placeholder name (e.g., "RED")
        return globals().get(placeholder, match.group(0))  # Replace if found, otherwise keep unchanged

    # Use re.sub to replace all placeholders in the text
    return re.sub(pattern, replace_match, text)

# Extended 256-color support (Foreground)
def FG_COLOR_EXT(code):
    return f"\033[38;5;{code}m"

# Extended 256-color support (Background)
def BG_COLOR_EXT(code):
    return f"\033[48;5;{code}m"

# Utility function to format text with color and style
def format_text(text, *styles):
    return f"{''.join(styles)}{text}{RESET}"

# Utility function to clear the screen
def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# Function to clear the current line in the terminal
def clear_current_line():
    sys.stdout.write("\r" + " " * 50 + "\r")  # Overwrite the line with spaces and move cursor back to the start
    sys.stdout.flush()
    
# Utility function to get resource path (compatible with PyInstaller executable)
def resource_path(relative_path):
    """ Get the absolute path to a resource, works for PyInstaller bundle """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# General JSON loader function
def load_json_data(file_name):
    try:
        with open(resource_path(file_name), "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{file_name} not found.")
        return {}

# Function to print skills with custom formatting
def print_skills(player_data):
    print("\nSkills Overview:")
    for skill, details in player_data["skills"].items():
        level = details["current"]
        experience = details["experience"]
        # Example of using text formatting: making the skill name bold and green
        print(f"{BOLD}{GREEN}{skill}{RESET}: Level {level}, Experience {experience}")

# Utility function to format text with style and color
def format_text(text, color=WHITE, style=""):
    return f"{style}{color}{text}{RESET}"
