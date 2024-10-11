import subprocess
import os
import json
import time
from utils import clear_screen, print_skills
from Player import create_new_player
from Player import save_player
from skills.skills import compare_skills
from skills.Mining import mining_menu
from skills.Hunting import hunting_menu
from skills.Fishing import fishing_menu
from skills.Gathering import gathering_menu
from combat.CombatMenu import combat_menu
from combat.CombatLogic import check_player_stats

# Load a specific save
def load_game(file_name):
    with open(f"./saves/{file_name}", "r") as file:
        return json.load(file)

def gameplay_menu(player_data):
    while True:
        clear_screen()
        print(f"Welcome {player_data['name']}!")
        print("1. Adventure")
        print("2. Skills")
        print("3. Return to Town")
        print("4. Personal Outpost")
        print("5. View Stats")
        print("6. View Inventory")
        print("7. Compare Skills")
        print("8. Exit to Main Menu")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            print("Starting Adventure...")
            combat_menu(player_data)
        elif choice == "2":
            skills_menu(player_data)
        elif choice == "3":
            print("Returning to Town...")
            time.sleep(1)  # Placeholder delay
        elif choice == "4":
            print("Going to Personal Outpost...")
            time.sleep(1)  # Placeholder delay
        elif choice == "5":
            clear_screen()
            check_player_stats(player_data)
            input("\nPress Enter to Continue to Skills")
            clear_screen()
            print_skills(player_data)
            input("\nPress Enter to Return to Main Menu")
            clear_screen()
        elif choice == "6":
            print("Viewing Inventory... (To be implemented)")
            time.sleep(1)
        elif choice == "7":
            saved_games = list_saved_games()
            if len(saved_games) >= 2:
                player1_data = load_game(saved_games[0]["file_name"])
                player2_data = load_game(saved_games[1]["file_name"])
                compare_skills(player1_data, player2_data)
            else:
                print("Not enough save files to compare.")
                time.sleep(1)
        elif choice == "8":
            return
        else:
            print("Invalid choice. Please select a valid option.")
            time.sleep(1)


# Main menu
def list_saved_games():
    saves_dir = "./saves/"
    saves = []
    if not os.path.exists(saves_dir):
        os.makedirs(saves_dir)

    # Loop through each file in the saves directory
    for file_name in os.listdir(saves_dir):
        if file_name.endswith(".json"):
            with open(os.path.join(saves_dir, file_name), "r") as file:
                data = json.load(file)
                saves.append({"name": data["name"], "level": data["level"], "file_name": file_name})
    return saves

def main_menu():
    while True:
        print("Main Menu")
        print("1. Load Game")
        print("2. New Game")
        print("3. Exit")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            clear_screen()
            saved_games = list_saved_games()
            if not saved_games:
                print("No saved games available.")
                continue
            
            print("Saved Games:")
            for idx, save in enumerate(saved_games, start=1):
                print(f"{idx}. {save['name']} - Level {save['level']}")
            print(f"{len(saved_games) + 1}. Go back")
            
            selected_save = input("Select a save to load or go back: ").strip()
            if selected_save.isdigit():
                selected_save = int(selected_save)
                if 1 <= selected_save <= len(saved_games):
                    player_data = load_game(saved_games[selected_save - 1]["file_name"])
                    gameplay_menu(player_data)
                elif selected_save == len(saved_games) + 1:
                    continue
                else:
                    print("Invalid selection.")
            else:
                print("Invalid input.")
        
        elif choice == "2":
            clear_screen()
            name = input("Enter a name for your character: ").strip()
            
            # Generate the file name in the format "{SaveNumber}-{PlayerName}-SaveData.json"
            file_name = f"./saves/{name}-SaveData.json"
            
            # Create the new player using the existing function
            player_data = create_new_player(name)
            
            # Save the new player data to the JSON file
            save_player(player_data, file_name)
            
            gameplay_menu(player_data)
        
        elif choice == "3":
            print("Exiting game...")
            break
        
        else:
            print("Invalid choice. Please select a valid option.")

def skills_menu(player_data):
    while True:
        clear_screen()
        print("Skills Menu:")
        print("1. Mining")
        print("2. Smithing")
        print("3. Crafting")
        print("4. Fletching")
        print("5. Chemistry")
        print("6. Alchemy")
        print("7. Gathering")
        print("8. Hunting")
        print("9. Fishing")
        print("10. Cooking")
        print("11. Construction")
        print("12. Back to Main Menu")
        
        choice = input("Select a skill: ").strip()
        
        if choice == "1":
            mining_menu(player_data)  # Now calling the mining menu from Mining.py
        elif choice == "2":
            print("This skill is currently unavailable.")
            time.sleep(1)
        elif choice == "3":
            print("This skill is currently unavailable.")
            time.sleep(1)
        elif choice == "4":
            print("This skill is currently unavailable.")
            time.sleep(1)
        elif choice == "5":
            print("This skill is currently unavailable.")
            time.sleep(1)
        elif choice == "6":
            print("This skill is currently unavailable.")
            time.sleep(1)
        elif choice == "7":
            gathering_menu(player_data)
        elif choice == "8":
            hunting_menu(player_data)
        elif choice == "9":
            fishing_menu(player_data)
        elif choice == "10":
            print("This skill is currently unavailable.")
            time.sleep(1)
        elif choice == "11":
            print("This skill is currently unavailable.")
            time.sleep(1)
        elif choice == "12":
            return
        else:
            print("Invalid choice.")
            time.sleep(1)


# Run the game
if __name__ == "__main__":
    clear_screen()
    main_menu()