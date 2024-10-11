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

# Save player data to JSON
def save_player(player_data, file_name):
    with open(file_name, "w") as file:
        json.dump(player_data, file, indent=4)
    print(f"Player data saved to {file_name}")


# Example function to get unlocked areas based on player level
def get_unlocked_areas(hunting_data, player_level):
    unlocked_areas = []
    for area, level_required in hunting_data["area_unlocks"].items():
        if player_level >= level_required:
            unlocked_areas.append(area)
    return unlocked_areas

# Example function to get animals available in a given area
def get_animals_in_area(hunting_data, area_name):
    return hunting_data["areas"].get(area_name, {}).get("animals", {})

# Example function to get animal unlock information
def get_animal_unlocks(hunting_data, player_level):
    unlocked_animals = []
    for animal in hunting_data["animal_unlocks"]:
        if player_level >= animal["level_required"]:
            unlocked_animals.append(animal)
    return unlocked_animals

# Hunting menu with options
def hunting_menu(player_data):
    while True:
        clear_screen()
        print("Hunting Menu:")
        print("1. View Animals")
        print("2. View Area Level Up Table")
        print("3. View Animal Level Up Table")
        print("4. Visit Hunting Ground")
        print("5. Back")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            view_animals(player_data)
        elif choice == "2":
            view_area_level_up_table()
        elif choice == "3":
            view_animal_level_up_table()
        elif choice == "4":
            visit_hunting_ground(player_data)
        elif choice == "5":
            return
        else:
            print("Invalid choice.")
            time.sleep(1)

# Function to view the area level up table
def view_area_level_up_table():
    clear_screen()
    hunting_data = load_json_data("skills/Hunting.json")
    
    print("Area Unlock Table:")
    for area, level_required in hunting_data["area_unlocks"].items():
        print(f"{area}: Unlocks at level {level_required}")
    
    input("Press any key to return to the Hunting Menu...")

# Function to view the animal level up table
def view_animal_level_up_table():
    clear_screen()
    hunting_data = load_json_data("skills/Hunting.json")
    
    print("Animal Unlock Table:")
    for animal in hunting_data["animal_unlocks"]:
        print(f"{animal['animal_name']}: Unlocks at level {animal['level_required']} - {animal['experience_per_hunt']} XP per hunt")
    
    input("Press any key to return to the Hunting Menu...")

# Function to visit hunting grounds that the player has unlocked
def visit_hunting_ground(player_data):
    clear_screen()
    hunting_data = load_json_data("skills/Hunting.json")
    
    print("Available Hunting Grounds:")
    player_level = player_data["skills"]["Hunting"]["current"]
    unlocked_grounds = [area for area, level_required in hunting_data["area_unlocks"].items() if player_level >= level_required]
    
    if not unlocked_grounds:
        print("No hunting grounds unlocked.")
    else:
        for idx, ground in enumerate(unlocked_grounds, start=1):
            print(f"{idx}. {ground}")
    
    print(f"{len(unlocked_grounds) + 1}. Back to Hunting Menu")
    
    choice = input("Select a hunting ground or go back: ").strip()
    
    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(unlocked_grounds):
            selected_ground = unlocked_grounds[choice - 1]
            travel_to_hunting_ground(player_data, selected_ground)  # Travel to the ground
            hunt_menu(player_data, selected_ground)
            travel_back_from_hunting_ground(player_data, selected_ground)  # Travel back after hunting
        elif choice == len(unlocked_grounds) + 1:
            return
        else:
            print("Invalid choice.")
            time.sleep(1)
    else:
        print("Invalid input.")
        time.sleep(1)

def hunt_menu(player_data, selected_ground):
    hunting_data = load_json_data("skills/Hunting.json")
    
    while True:
        clear_screen()
        print(f"You are at the {selected_ground}.")

        print("1. Look Around")
        print("2. Start Hunting")
        print("3. Back to Hunting Grounds List")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            # Display the ground's description and available animals, and the required tool
            description = hunting_data["areas"].get(selected_ground, {}).get("description", "No description available.")
            animals_in_ground = hunting_data["areas"].get(selected_ground, {}).get("animals", {})
            
            print(f"\n{description}")
            print("You spot the following animals:")
            
            tools_data = load_json_data("items/Tools.json")  # Load tools data
            
            for animal_name in animals_in_ground:
                # Find the corresponding animal in the animal unlocks data
                animal_info = next((animal for animal in hunting_data["animal_unlocks"] if animal["animal_name"] == animal_name), None)
                if animal_info:
                    required_tool = animal_info["tool_required"]
                    print(f"- {animal_name} (Requires: {required_tool})")
            
            input("\nPress any key to return to the hunting menu...")
        
        elif choice == "2":
            hunt(player_data, selected_ground)
        
        elif choice == "3":
            return  # Go back to the hunting grounds list
        
        else:
            print("Invalid choice.")
            time.sleep(1)

# Load tools data
def load_json_data(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{file_name} not found.")
        return {}

# Function to show a progress bar and handle hunting process
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
    # Base travel time is the distance to the hunting ground
    base_travel_time = distance  # In seconds or minutes, depending on how you want to scale it
    # Adjusted travel time is base travel time multiplied by the travel time modifier
    return base_travel_time * travel_time_modifier

def travel_to_hunting_ground(player_data, selected_ground):
    hunting_data = load_json_data("skills/Hunting.json")
    distance = hunting_data["areas"].get(selected_ground, {}).get("distance", 0)

    # Automatically reset the cart's current capacity before starting the trip to hunt
    player_data["travel"]["Current_Capacity"] = 0
    print("Cart emptied. Current Capacity reset to 0.")

    # Calculate the travel time using the distance and player's travel setup
    travel_time = calculate_travel_time(player_data, distance)

    print(f"Traveling to {selected_ground}. This will take approximately {travel_time:.2f} seconds...")
    show_progress_bar(int(travel_time))
    print(f"Arrived at {selected_ground}.")

# Travel back from the hunting ground after hunting
def travel_back_from_hunting_ground(player_data, selected_ground):
    hunting_data = load_json_data("skills/Hunting.json")
    distance = hunting_data["areas"].get(selected_ground, {}).get("distance", 0)

    # Calculate the travel time using the distance and player's travel setup
    travel_time = calculate_travel_time(player_data, distance)

    print(f"Traveling back from {selected_ground}. This will take approximately {travel_time:.2f} seconds...")
    show_progress_bar(int(travel_time))
    print(f"Returned from {selected_ground}.")

# Function to list the player's animals in their inventory and calculate their total value
def view_animals(player_data):
    clear_screen()
    
    # Load the item data to get animal information
    item_data = load_json_data("items/Items.json")
    
    # Get the player's inventory
    inventory = player_data.get("inventory", {})
    
    print("Your current animals:")
    print("-" * 40)
    
    total_inventory_value = 0
    found_animals = False
    
    # Loop through the animals in the Items.json
    for animal_name, animal_info in item_data["Material"]["Animal"].items():
        # Check if the animal is in the player's inventory
        if animal_name in inventory:
            found_animals = True
            quantity = inventory[animal_name]
            value_per_unit = animal_info["Value"]
            total_value = quantity * value_per_unit
            total_inventory_value += total_value
            
            # Print the animal details
            print(f"{animal_name}:")
            print(f"  Quantity: {quantity}")
            print(f"  Value per unit: {value_per_unit} Denarius")
            print(f"  Total value: {total_value} Denarius")
            print("-" * 40)
    
    if not found_animals:
        print("No animals found in your inventory.")
    else:
        print(f"Total value of animals: {total_inventory_value} Denarius")
    
    input("\nPress any key to return to the Hunting Menu...")

def hunt(player_data, selected_ground):
    clear_screen()

    hunting_data = load_json_data("skills/Hunting.json")
    tools_data = load_json_data("items/Tools.json")
    item_data = load_json_data("items/Items.json")  # Load the item data to get animal weights

    hunting_level = player_data["skills"]["Hunting"]["current"]
    
    # Fetch the animals available in the selected area
    animals_in_ground = hunting_data["areas"].get(selected_ground, {}).get("animals", {})
    unlocked_animals = []

    for animal_name, base_rate in animals_in_ground.items():
        animal_info = next((animal for animal in hunting_data["animal_unlocks"] if animal["animal_name"] == animal_name), None)
        if animal_info and hunting_level >= animal_info["level_required"]:
            unlocked_animals.append((animal_name, base_rate, animal_info["experience_per_hunt"], animal_info["tool_required"]))

    if not unlocked_animals:
        print("No animals available at your hunting level.")
        time.sleep(1)
        return

    print(f"Available animals in {selected_ground}:")
    for idx, (animal_name, base_rate, _, tool_required) in enumerate(unlocked_animals, start=1):
        print(f"{idx}. {animal_name} (Base rate: {base_rate}, Tool required: {tool_required})")
    print(f"{len(unlocked_animals) + 1}. Back")

    choice = input("Select an animal to hunt or go back: ").strip()

    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(unlocked_animals):
            selected_animal, base_rate, experience, tool_required = unlocked_animals[choice - 1]
            animal_weight = item_data["Material"]["Animal"][selected_animal]["Weight"]

            # Check if the player has the required tool for the selected animal
            equipped_tool = player_data["tools"].get("Hunting", {}).get(tool_required, None)  # Fetch the tool based on its type (Snare, Bow, Trap)

            # Fetch the tool info from Tools.json
            tool_info = tools_data.get("Hunting", {}).get(tool_required, {}).get(equipped_tool, None)  # Fetch from Tools.json
            
            if not tool_info:
                print(f"Error: Equipped tool {equipped_tool} does not match the required tool type {tool_required}.")
                time.sleep(2)
                return

            clear_screen()
            print(f"Hunting {selected_animal} with your {equipped_tool}... Press Ctrl+C to stop.")

            total_exp_gained = 0
            start_time = time.time()

            # Calculate hunting time and XP/hour if tool stats are available
            hunting_time_per_animal = int(base_rate * (1 - (hunting_level / 200)) * tool_info["Rate"])
            xp_per_hour = (3600 / hunting_time_per_animal) * experience  # Direct XP/hour calculation

            # Calculate time to level
            skill = player_data["skills"]["Hunting"]
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

            print(f"Hunting time per animal: {hunting_time_per_animal} seconds | Animals caught per hour: {3600 / hunting_time_per_animal:.2f}")
            print(f"Experience per hour: {xp_per_hour:.2f} XP/hour | Time to level: {time_to_next_level_formatted}")

            while True:
                try:
                    # Show progress bar and hunt the animal
                    show_progress_bar(hunting_time_per_animal)

                    # Add animal to inventory and experience to the player
                    Player.add_item(player_data, selected_animal)
                    Player.add_experience(player_data, "Hunting", experience)
                    total_exp_gained += experience

                    # Add animal weight to the cart's current capacity
                    player_data["travel"]["Current_Capacity"] += animal_weight
                    max_capacity = player_data["travel"]["Max_Capacity"]
                    print(f"Added {selected_animal} to Cart. Current capacity: {player_data['travel']['Current_Capacity']} / {max_capacity}")

                    # Check if the cart is full
                    if player_data["travel"]["Current_Capacity"] >= max_capacity:
                        print(f"\nYour cart is full with {player_data['travel']['Current_Capacity']} units of weight!")
                        travel_back_from_hunting_ground(player_data, selected_ground)
                        travel_to_hunting_ground(player_data, selected_ground)  # Return to the hunting ground with an empty cart

                except KeyboardInterrupt:
                    print("\nHunting interrupted. Returning to the previous menu.")
                    break
        elif choice == len(unlocked_animals) + 1:
            return
        else:
            print("Invalid choice.")
            time.sleep(1)
    else:
        print("Invalid input.")
        time.sleep(1)
