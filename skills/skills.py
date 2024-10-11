from utils import *
import re

# Function to calculate the display length of a string, ignoring color codes
def display_length(text):
    return len(re.sub(r"\033\[[0-9;]*m", "", text))

def compare_skills(player1_data, player2_data):
    clear_screen()
    print(f"Comparing skills for {player1_data['name']} and {player2_data['name']}:")
    
    player1_skills = player1_data["skills"]
    player2_skills = player2_data["skills"]

    # Get a list of all skills
    all_skills = set(player1_skills.keys()).union(player2_skills.keys())

    # Set column widths for the skills and levels
    max_skill_length = max(len(skill) for skill in all_skills) + 2  # Add padding for readability
    name_column_width = 10  # Width for player names, make it wide enough for any skill level

    # Print the header
    print(f"{'Skill':<{max_skill_length}}{'Karkess':<{name_column_width}}{'Mira':<{name_column_width}}")
    print("=" * (max_skill_length + 2 * name_column_width))
    
    # Iterate over all skills
    for skill in all_skills:
        p1_skill_level = player1_skills.get(skill, {}).get("current", 0)
        p2_skill_level = player2_skills.get(skill, {}).get("current", 0)

        # Prepare the display of skill levels without color codes first
        p1_display = f"{p1_skill_level:<{name_column_width}}"
        p2_display = f"{p2_skill_level:<{name_column_width}}"
        
        # Compare the skill levels and apply the color codes for the winner
        if p1_skill_level > p2_skill_level:
            p1_display = f"{GREEN}{p1_skill_level:<{name_column_width}}{RESET}"
        elif p2_skill_level > p1_skill_level:
            p2_display = f"{GREEN}{p2_skill_level:<{name_column_width}}{RESET}"

        # Print the formatted row with proper spacing
        print(f"{skill:<{max_skill_length}}{p1_display}{p2_display}")

    input("\nPress Enter to return to the previous menu.")
