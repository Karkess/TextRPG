import time
from combat.GearMenu import gear_menu
from combat.CombatLogic import check_player_stats  # Import the stat-checking function
from utils import clear_screen  # Import clear_screen from utils.py
from combat.CombatManager import combat_loop  # Import the combat loop

# Combat menu with options
def combat_menu(player_data):
    while True:
        clear_screen()  # Clear the screen before displaying the menu
        print("Combat Menu:")
        print("1. Random Battle")
        print("2. Dungeons")
        print("3. Quests")
        print("4. Gear")
        print("5. Check Stats")  # Added an option for checking stats
        print("6. Bestiary")
        print("7. Back")

        choice = input("Select an option: ").strip()

        if choice == "1":
            # For a random battle, we will instantiate a battle with a "Goblin"
            clear_screen()
            print("Starting Random Battle against a Goblin!")
            time.sleep(1)

            # Example: Starting a combat loop with a player and a Goblin enemy
            combat_loop(player_data, ["Goblin", "Eye Gouger"])

            input("\nPress Enter to Return")
        elif choice == "2":
            print("Dungeons (placeholder).")
            time.sleep(1)
        elif choice == "3":
            print("Quests (placeholder).")
            time.sleep(1)
        elif choice == "4":
            gear_menu(player_data)
        elif choice == "5":
            clear_screen()
            check_player_stats(player_data)
            input("\nPress Enter to Return")
        elif choice == "6":
            print("Bestiary (placeholder).")
            time.sleep(1)
        elif choice == "7":
            print("Returning to previous menu...")
            break
        else:
            print("Invalid choice. Please select a valid option.")
            time.sleep(1)
