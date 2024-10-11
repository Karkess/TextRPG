# ./combat/GearMenu.py
import time
from utils import clear_screen  # Import clear_screen from utils.py

# Placeholder gear menu
def gear_menu(player_data):
    while True:
        clear_screen()  # Clear the screen before displaying the menu
        print("\nGear Menu:")
        print("1. Weapons")
        print("2. Armor")
        print("3. Companion")
        print("4. Classes")
        print("5. Skills")
        print("6. Consumables")
        print("7. Back")

        choice = input("Select an option: ").strip()

        if choice == "1":
            print("Weapons (placeholder).")
            time.sleep(1)
        elif choice == "2":
            print("Armor (placeholder).")
            time.sleep(1)
        elif choice == "3":
            print("Companion (placeholder).")
            time.sleep(1)
        elif choice == "4":
            print("Classes (placeholder).")
            time.sleep(1)
        elif choice == "5":
            print("Skills (placeholder).")
            time.sleep(1)
        elif choice == "6":
            print("Consumables (placeholder).")
            time.sleep(1)
        elif choice == "7":
            print("Returning to previous menu...")
            break
        else:
            print("Invalid choice. Please select a valid option.")
            time.sleep(1)
