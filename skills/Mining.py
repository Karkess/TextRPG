import json
import time
import os
import sys
import Player
from utils import clear_screen, load_json_data

# Function to clear the current line in the terminal
def clear_current_line():
    sys.stdout.write("\r" + " " * 50 + "\r")  # Overwrite the line with spaces and move cursor back to the start
    sys.stdout.flush()

# Example function to get unlocked areas based on player level
def get_unlocked_areas(mining_data, player_level):
    unlocked_areas = []
    for area, level_required in mining_data["area_unlocks"].items():
        if player_level >= level_required:
            unlocked_areas.append(area)
    return unlocked_areas

# Example function to get ores available in a given area
def get_ores_in_area(mining_data, area_name):
    return mining_data["areas"].get(area_name, {}).get("ores", {})

# Example function to get ore unlock information
def get_ore_unlocks(mining_data, player_level):
    unlocked_ores = []
    for ore in mining_data["ore_unlocks"]:
        if player_level >= ore["level_required"]:
            unlocked_ores.append(ore)
    return unlocked_ores

# Mining menu with options
def mining_menu(player_data):
    while True:
        clear_screen()
        print("Mining Menu:")
        print("1. View Ores")
        print("2. View Area Level Up Table")
        print("3. View Ore Level Up Table")
        print("4. Visit Mine")
        print("5. Back")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            view_ores(player_data)
        elif choice == "2":
            view_area_level_up_table()
        elif choice == "3":
            view_ore_level_up_table()
        elif choice == "4":
            visit_mine(player_data)
        elif choice == "5":
            return
        else:
            print("Invalid choice.")
            time.sleep(1)

# Function to view the area level up table
def view_area_level_up_table():
    clear_screen()
    mining_data = load_json_data("skills/Mining.json")
    
    print("Area Unlock Table:")
    for area, level_required in mining_data["area_unlocks"].items():
        print(f"{area}: Unlocks at level {level_required}")
    
    input("Press any key to return to the Mining Menu...")

# Function to view the ore level up table
def view_ore_level_up_table():
    clear_screen()
    mining_data = load_json_data("skills/Mining.json")
    
    print("Ore Unlock Table:")
    for ore in mining_data["ore_unlocks"]:
        print(f"{ore['ore_name']}: Unlocks at level {ore['level_required']} - {ore['experience_per_gather']} XP per gather")
    
    input("Press any key to return to the Mining Menu...")

# Function to visit mines that the player has unlocked
def visit_mine(player_data):
    clear_screen()
    mining_data = load_json_data("skills/Mining.json")
    
    print("Available Mines:")
    player_level = player_data["skills"]["Mining"]["current"]
    unlocked_mines = [area for area, level_required in mining_data["area_unlocks"].items() if player_level >= level_required]
    
    if not unlocked_mines:
        print("No mines unlocked.")
    else:
        for idx, mine in enumerate(unlocked_mines, start=1):
            print(f"{idx}. {mine}")
    
    print(f"{len(unlocked_mines) + 1}. Back to Mining Menu")
    
    choice = input("Select a mine or go back: ").strip()
    
    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(unlocked_mines):
            selected_mine = unlocked_mines[choice - 1]
            clear_screen()
            travel_to_mine(player_data, selected_mine)  # Travel to the mine
            mine_menu(player_data, selected_mine)
            travel_back_from_mine(player_data, selected_mine)  # Travel back after mining
        elif choice == len(unlocked_mines) + 1:
            return
        else:
            print("Invalid choice.")
            time.sleep(1)
    else:
        print("Invalid input.")
        time.sleep(1)

def mine_menu(player_data, selected_mine):
    mining_data = load_json_data("skills/Mining.json")
    
    while True:
        clear_screen()
        print(f"You are at the {selected_mine}.")

        print("1. Look Around")
        print("2. Start Mining")
        print("3. Back to Mines List")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            # Display the mine's description and available ores
            description = mining_data["areas"].get(selected_mine, {}).get("description", "No description available.")
            ores_in_mine = mining_data["areas"].get(selected_mine, {}).get("ores", {})
            clear_screen()
            print(f"{description}")
            print("You spot the following ores:")
            for ore_name in ores_in_mine:
                print(f"- {ore_name}")
            
            input("\nPress any key to return to the mine menu...")
        
        elif choice == "2":
            mine_ore(player_data, selected_mine)
        
        elif choice == "3":
            return  # Go back to the mines list
        
        else:
            print("Invalid choice.")
            time.sleep(1)

# Function to show a progress bar and handle mining process
def show_progress_bar(total_time):
    for i in range(total_time):
        time.sleep(1)
        progress = (i + 1) / total_time * 100
        sys.stdout.write(f"\rProgress: [{int(progress)}%] ")
        sys.stdout.flush()

    # Clear the progress bar line after completion
    clear_current_line()

# Function to calculate travel time using the player's cart/animal setup
def calculate_travel_time(player_data, distance):
    # Get the travel time modifier from Player.py (e.g., based on the cart and animals)
    travel_time_modifier = Player.calculate_travel_stats(player_data)
    # Base travel time is the distance to the mine
    base_travel_time = distance  # In seconds or minutes, depending on how you want to scale it
    # Adjusted travel time is base travel time multiplied by the travel time modifier
    return base_travel_time * travel_time_modifier

def travel_to_mine(player_data, selected_mine):
    mining_data = load_json_data("skills/Mining.json")
    distance = mining_data["areas"].get(selected_mine, {}).get("distance", 0)

    # Automatically reset the cart's current capacity before starting the trip to mine
    player_data["travel"]["Current_Capacity"] = 0
    print("Cart emptied. Current Capacity reset to 0.")

    # Calculate the travel time using the distance and player's travel setup
    travel_time = calculate_travel_time(player_data, distance)

    print(f"Traveling to {selected_mine}. This will take approximately {travel_time:.2f} seconds...")
    show_progress_bar(int(travel_time))
    print(f"Arrived at {selected_mine}.")

# Travel back from the mine after mining
def travel_back_from_mine(player_data, selected_mine):
    mining_data = load_json_data("skills/Mining.json")
    distance = mining_data["areas"].get(selected_mine, {}).get("distance", 0)

    # Calculate the travel time using the distance and player's travel setup
    travel_time = calculate_travel_time(player_data, distance)

    print(f"Traveling back from {selected_mine}. This will take approximately {travel_time:.2f} seconds...")
    show_progress_bar(int(travel_time))
    print(f"Returned from {selected_mine}.")

# Function to list the player's ores in their inventory and calculate their total value
def view_ores(player_data):
    clear_screen()
    
    # Load the item data to get ore information
    item_data = load_json_data("items/Items.json")
    
    # Get the player's inventory
    inventory = player_data.get("inventory", {})
    
    print("Your current ores:")
    print("-" * 40)
    
    total_inventory_value = 0
    found_ores = False
    
    # Loop through the ores in the Items.json
    for ore_name, ore_info in item_data["Material"]["Ore"].items():
        # Check if the ore is in the player's inventory
        if ore_name in inventory:
            found_ores = True
            quantity = inventory[ore_name]
            value_per_unit = ore_info["Value"]
            total_value = quantity * value_per_unit
            total_inventory_value += total_value
            
            # Print the ore details
            print(f"{ore_name}:")
            print(f"  Quantity: {quantity}")
            print(f"  Value per unit: {value_per_unit} Denarius")
            print(f"  Total value: {total_value} Denarius")
            print("-" * 40)
    
    if not found_ores:
        print("No ores found in your inventory.")
    else:
        print(f"Total value of ores: {total_inventory_value} Denarius")
    
    input("\nPress any key to return to the Mining Menu...")

def mine_ore(player_data, selected_mine):
    clear_screen()

    mining_data = load_json_data("skills/Mining.json")
    tools_data = load_json_data("items/Tools.json")
    item_data = load_json_data("items/Items.json")  # Load the item data to get ore weights

    mining_level = player_data["skills"]["Mining"]["current"]
    equipped_tool = player_data["tools"].get("Mining", None)

    if not equipped_tool:
        print("No mining tool equipped!")
        time.sleep(1)
        return

    tool_stats = tools_data.get("Mining", {}).get(equipped_tool, None)
    if not tool_stats:
        print(f"Tool '{equipped_tool}' not found in Tools.json.")
        time.sleep(1)
        return

    ores_in_mine = mining_data["areas"].get(selected_mine, {}).get("ores", {})
    unlocked_ores = []

    for ore_name, base_rate in ores_in_mine.items():
        ore_info = next((ore for ore in mining_data["ore_unlocks"] if ore["ore_name"] == ore_name), None)
        if ore_info and mining_level >= ore_info["level_required"]:
            unlocked_ores.append((ore_name, base_rate, ore_info["experience_per_gather"]))

    if not unlocked_ores:
        print("No ores available at your mining level.")
        time.sleep(1)
        return

    print(f"Available ores in {selected_mine}:")
    for idx, (ore_name, base_rate, _) in enumerate(unlocked_ores, start=1):
        print(f"{idx}. {ore_name} (Base rate: {base_rate})")
    print(f"{len(unlocked_ores) + 1}. Back")

    choice = input("Select an ore to mine or go back: ").strip()

    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(unlocked_ores):
            selected_ore, base_rate, experience = unlocked_ores[choice - 1]
            ore_weight = item_data["Material"]["Ore"][selected_ore]["Weight"]

            clear_screen()
            print(f"Mining {selected_ore}... Press Ctrl+C to stop.")

            total_exp_gained = 0
            start_time = time.time()

            # Calculate mining time and XP/hour
            tool_rate = tool_stats["Rate"]
            mining_time_per_ore = int(base_rate * (1 - (mining_level / 200)) * tool_rate)
            xp_per_hour = (3600 / mining_time_per_ore) * experience  # Direct XP/hour calculation

            # Calculate time to level
            skill = player_data["skills"]["Mining"]
            current_level = skill["current"]
            current_xp = skill["experience"]

            # Load the level-up table to get the XP needed for the next level
            level_up_table = load_json_data("./skills/LevelUpTable.json")
            xp_for_next_level = level_up_table.get(str(current_level + 1), None)

            if xp_for_next_level:
                xp_needed = xp_for_next_level - current_xp
                time_to_next_level = xp_needed / xp_per_hour * 60  # Time in minutes

                # Convert time to level into hours and minutes
                hours = int(time_to_next_level // 60)
                minutes = int(time_to_next_level % 60)
                time_to_next_level_formatted = f"{hours}h {minutes}m"
            else:
                time_to_next_level_formatted = "MAX level reached"

            print(f"Mining time per ore: {mining_time_per_ore} seconds | Ore gathered per hour: {3600 / mining_time_per_ore:.2f}")
            print(f"Experience per hour: {xp_per_hour:.2f} XP/hour | Time to level: {time_to_next_level_formatted}")

            while True:
                try:
                    # Show progress bar and mine the ore
                    show_progress_bar(mining_time_per_ore)

                    # Add ore to inventory and experience to the player
                    Player.add_item(player_data, selected_ore)
                    Player.add_experience(player_data, "Mining", experience)
                    total_exp_gained += experience

                    # Add ore weight to the cart's current capacity
                    player_data["travel"]["Current_Capacity"] += ore_weight
                    max_capacity = player_data["travel"]["Max_Capacity"]
                    print(f"Added {selected_ore} to Cart. Current capacity: {player_data['travel']['Current_Capacity']} / {max_capacity}")

                    # Check if the cart is full
                    if player_data["travel"]["Current_Capacity"] >= max_capacity:
                        print(f"\nYour cart is full with {player_data['travel']['Current_Capacity']} units of weight!")
                        travel_back_from_mine(player_data, selected_mine)
                        travel_to_mine(player_data, selected_mine)  # Return to the mine with an empty cart

                except KeyboardInterrupt:
                    print("\nMining interrupted. Returning to the previous menu.")
                    break
        elif choice == len(unlocked_ores) + 1:
            return
        else:
            print("Invalid choice.")
            time.sleep(1)
    else:
        print("Invalid input.")
        time.sleep(1)
