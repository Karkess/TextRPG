import json
import time
import os
import sys
import Player
from utils import clear_screen, clear_current_line, load_json_data

# Save player data to JSON
def save_player(player_data, file_name):
    with open(file_name, "w") as file:
        json.dump(player_data, file, indent=4)
    print(f"Player data saved to {file_name}")


# Example function to get unlocked areas based on player level
def get_unlocked_areas(fishing_data, player_level):
    unlocked_areas = []
    for area, level_required in fishing_data["area_unlocks"].items():
        if player_level >= level_required:
            unlocked_areas.append(area)
    return unlocked_areas

# Example function to get fish available in a given area
def get_fish_in_area(fishing_data, area_name):
    return fishing_data["areas"].get(area_name, {}).get("fish", {})

# Example function to get fish unlock information
def get_fish_unlocks(fishing_data, player_level):
    unlocked_fish = []
    for fish in fishing_data["fish_unlocks"]:
        if player_level >= fish["level_required"]:
            unlocked_fish.append(fish)
    return unlocked_fish

# Fishing menu with options
def fishing_menu(player_data):
    while True:
        clear_screen()
        print("Fishing Menu:")
        print("1. View Fish")
        print("2. View Area Level Up Table")
        print("3. View Fish Level Up Table")
        print("4. Visit Fishing Spot")
        print("5. Back")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            view_fish(player_data)
        elif choice == "2":
            view_area_level_up_table()
        elif choice == "3":
            view_fish_level_up_table()
        elif choice == "4":
            visit_fishing_spot(player_data)
        elif choice == "5":
            return
        else:
            print("Invalid choice.")
            time.sleep(1)

# Function to view the area level up table
def view_area_level_up_table():
    clear_screen()
    fishing_data = load_json_data("skills/Fishing.json")
    
    print("Area Unlock Table:")
    for area, level_required in fishing_data["area_unlocks"].items():
        print(f"{area}: Unlocks at level {level_required}")
    
    input("Press any key to return to the Fishing Menu...")

# Function to view the fish level up table
def view_fish_level_up_table():
    clear_screen()
    fishing_data = load_json_data("skills/Fishing.json")
    
    print("Fish Unlock Table:")
    for fish in fishing_data["fish_unlocks"]:
        print(f"{fish['fish_name']}: Unlocks at level {fish['level_required']} - {fish['experience_per_gather']} XP per catch")
    
    input("Press any key to return to the Fishing Menu...")

# Function to visit fishing spots that the player has unlocked
def visit_fishing_spot(player_data):
    clear_screen()
    fishing_data = load_json_data("skills/Fishing.json")
    
    print("Available Fishing Spots:")
    player_level = player_data["skills"]["Fishing"]["current"]
    unlocked_spots = [area for area, level_required in fishing_data["area_unlocks"].items() if player_level >= level_required]
    
    if not unlocked_spots:
        print("No fishing spots unlocked.")
    else:
        for idx, spot in enumerate(unlocked_spots, start=1):
            print(f"{idx}. {spot}")
    
    print(f"{len(unlocked_spots) + 1}. Back to Fishing Menu")
    
    choice = input("Select a fishing spot or go back: ").strip()
    
    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(unlocked_spots):
            selected_spot = unlocked_spots[choice - 1]
            travel_to_fishing_spot(player_data, selected_spot)  # Travel to the spot
            fish_menu(player_data, selected_spot)
            travel_back_from_fishing_spot(player_data, selected_spot)  # Travel back after fishing
        elif choice == len(unlocked_spots) + 1:
            return
        else:
            print("Invalid choice.")
            time.sleep(1)
    else:
        print("Invalid input.")
        time.sleep(1)

def fish_menu(player_data, selected_spot):
    fishing_data = load_json_data("skills/Fishing.json")
    
    while True:
        clear_screen()
        print(f"You are at the {selected_spot}.")

        print("1. Look Around")
        print("2. Start Fishing")
        print("3. Back to Fishing Spots List")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            # Display the spot's description and available fish
            description = fishing_data["areas"].get(selected_spot, {}).get("description", "No description available.")
            fish_in_spot = fishing_data["areas"].get(selected_spot, {}).get("fish", {})
            
            print(f"\n{description}")
            print("You spot the following fish:")
            for fish_name in fish_in_spot:
                print(f"- {fish_name}")
            
            input("\nPress any key to return to the fishing menu...")
        
        elif choice == "2":
            fish(player_data, selected_spot)
        
        elif choice == "3":
            return  # Go back to the fishing spots list
        
        else:
            print("Invalid choice.")
            time.sleep(1)

# Function to show a progress bar and handle fishing process
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
    # Base travel time is the distance to the fishing spot
    base_travel_time = distance  # In seconds or minutes, depending on how you want to scale it
    # Adjusted travel time is base travel time multiplied by the travel time modifier
    return base_travel_time * travel_time_modifier

def travel_to_fishing_spot(player_data, selected_spot):
    fishing_data = load_json_data("skills/Fishing.json")
    distance = fishing_data["areas"].get(selected_spot, {}).get("distance", 0)

    # Automatically reset the cart's current capacity before starting the trip to fish
    player_data["travel"]["Current_Capacity"] = 0
    print("Cart emptied. Current Capacity reset to 0.")

    # Calculate the travel time using the distance and player's travel setup
    travel_time = calculate_travel_time(player_data, distance)

    print(f"Traveling to {selected_spot}. This will take approximately {travel_time:.2f} seconds...")
    show_progress_bar(int(travel_time))
    print(f"Arrived at {selected_spot}.")

# Travel back from the fishing spot after fishing
def travel_back_from_fishing_spot(player_data, selected_spot):
    fishing_data = load_json_data("skills/Fishing.json")
    distance = fishing_data["areas"].get(selected_spot, {}).get("distance", 0)

    # Calculate the travel time using the distance and player's travel setup
    travel_time = calculate_travel_time(player_data, distance)

    print(f"Traveling back from {selected_spot}. This will take approximately {travel_time:.2f} seconds...")
    show_progress_bar(int(travel_time))
    print(f"Returned from {selected_spot}.")

# Function to list the player's fish in their inventory and calculate their total value
def view_fish(player_data):
    clear_screen()
    
    # Load the item data to get fish information
    item_data = load_json_data("items/Items.json")
    
    # Get the player's inventory
    inventory = player_data.get("inventory", {})
    
    print("Your current fish:")
    print("-" * 40)
    
    total_inventory_value = 0
    found_fish = False
    
    # Loop through the fish in the Items.json
    for fish_name, fish_info in item_data["Material"]["Fish"].items():
        # Check if the fish is in the player's inventory
        if fish_name in inventory:
            found_fish = True
            quantity = inventory[fish_name]
            value_per_unit = fish_info["Value"]
            total_value = quantity * value_per_unit
            total_inventory_value += total_value
            
            # Print the fish details
            print(f"{fish_name}:")
            print(f"  Quantity: {quantity}")
            print(f"  Value per unit: {value_per_unit} Denarius")
            print(f"  Total value: {total_value} Denarius")
            print("-" * 40)
    
    if not found_fish:
        print("No fish found in your inventory.")
    else:
        print(f"Total value of fish: {total_inventory_value} Denarius")
    
    input("\nPress any key to return to the Fishing Menu...")

def fish(player_data, selected_spot):
    clear_screen()

    fishing_data = load_json_data("skills/Fishing.json")
    tools_data = load_json_data("items/Tools.json")
    item_data = load_json_data("items/Items.json")  # Load the item data to get fish weights

    fishing_level = player_data["skills"]["Fishing"]["current"]
    equipped_tool = player_data["tools"].get("Fishing", None)

    if not equipped_tool:
        print("No fishing tool equipped!")
        time.sleep(1)
        return

    tool_stats = tools_data.get("Fishing", {}).get(equipped_tool, None)
    if not tool_stats:
        print(f"Tool '{equipped_tool}' not found in Tools.json.")
        time.sleep(1)
        return

    fish_in_spot = fishing_data["areas"].get(selected_spot, {}).get("fish", {})
    unlocked_fish = []

    for fish_name, base_rate in fish_in_spot.items():
        fish_info = next((fish for fish in fishing_data["fish_unlocks"] if fish["fish_name"] == fish_name), None)
        if fish_info and fishing_level >= fish_info["level_required"]:
            unlocked_fish.append((fish_name, base_rate, fish_info["experience_per_gather"]))

    if not unlocked_fish:
        print("No fish available at your fishing level.")
        time.sleep(1)
        return

    print(f"Available fish in {selected_spot}:")
    for idx, (fish_name, base_rate, _) in enumerate(unlocked_fish, start=1):
        print(f"{idx}. {fish_name} (Base rate: {base_rate})")
    print(f"{len(unlocked_fish) + 1}. Back")

    choice = input("Select a fish to catch or go back: ").strip()

    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(unlocked_fish):
            selected_fish, base_rate, experience = unlocked_fish[choice - 1]
            fish_weight = item_data["Material"]["Fish"][selected_fish]["Weight"]

            clear_screen()
            print(f"Fishing for {selected_fish}... Press Ctrl+C to stop.")

            total_exp_gained = 0
            start_time = time.time()

            # Calculate fishing time and XP/hour
            tool_rate = tool_stats["Rate"]
            fishing_time_per_fish = int(base_rate * (1 - (fishing_level / 200)) * tool_rate)
            xp_per_hour = (3600 / fishing_time_per_fish) * experience  # Direct XP/hour calculation

            # Calculate time to level
            skill = player_data["skills"]["Fishing"]
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

            print(f"Fishing time per fish: {fishing_time_per_fish} seconds | Fish caught per hour: {3600 / fishing_time_per_fish:.2f}")
            print(f"Experience per hour: {xp_per_hour:.2f} XP/hour | Time to level: {time_to_next_level_formatted}")

            while True:
                try:
                    # Show progress bar and catch the fish
                    show_progress_bar(fishing_time_per_fish)

                    # Add fish to inventory and experience to the player
                    Player.add_item(player_data, selected_fish)
                    Player.add_experience(player_data, "Fishing", experience)
                    total_exp_gained += experience

                    # Add fish weight to the cart's current capacity
                    player_data["travel"]["Current_Capacity"] += fish_weight
                    max_capacity = player_data["travel"]["Max_Capacity"]
                    print(f"Added {selected_fish} to Cart. Current capacity: {player_data['travel']['Current_Capacity']} / {max_capacity}")

                    # Check if the cart is full
                    if player_data["travel"]["Current_Capacity"] >= max_capacity:
                        print(f"\nYour cart is full with {player_data['travel']['Current_Capacity']} units of weight!")
                        travel_back_from_fishing_spot(player_data, selected_spot)
                        travel_to_fishing_spot(player_data, selected_spot)  # Return to the spot with an empty cart

                except KeyboardInterrupt:
                    print("\nFishing interrupted. Returning to the previous menu.")
                    break
        elif choice == len(unlocked_fish) + 1:
            return
        else:
            print("Invalid choice.")
            time.sleep(1)
    else:
        print("Invalid input.")
        time.sleep(1)
