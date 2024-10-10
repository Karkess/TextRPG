import json
import time
import os
import sys
import Player
from utils import clear_screen, load_json_data, clear_current_line

# Save player data to JSON
def save_player(player_data, file_name):
    with open(file_name, "w") as file:
        json.dump(player_data, file, indent=4)
    print(f"Player data saved to {file_name}")

# Example function to get unlocked areas based on player level
def get_unlocked_areas(gathering_data, player_level):
    unlocked_areas = []
    for area, level_required in gathering_data["area_unlocks"].items():
        if player_level >= level_required:
            unlocked_areas.append(area)
    return unlocked_areas

# Example function to get resources available in a given area
def get_resources_in_area(gathering_data, area_name):
    return gathering_data["areas"].get(area_name, {}).get("resources", {})

# Example function to get resource unlock information
def get_resource_unlocks(gathering_data, player_level):
    unlocked_resources = []
    for resource in gathering_data["resource_unlocks"]:
        if player_level >= resource["level_required"]:
            unlocked_resources.append(resource)
    return unlocked_resources

# Gathering menu with options
def gathering_menu(player_data):
    while True:
        clear_screen()
        print("Gathering Menu:")
        print("1. View Resources")
        print("2. View Area Level Up Table")
        print("3. View Resource Level Up Table")
        print("4. Visit Gathering Area")
        print("5. Back")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            view_resources(player_data)
        elif choice == "2":
            view_area_level_up_table()
        elif choice == "3":
            view_resource_level_up_table()
        elif choice == "4":
            visit_gathering_area(player_data)
        elif choice == "5":
            return
        else:
            print("Invalid choice.")
            time.sleep(1)

# Function to view the area level up table
def view_area_level_up_table():
    clear_screen()
    gathering_data = load_json_data("skills/Gathering.json")
    
    print("Area Unlock Table:")
    for area, level_required in gathering_data["area_unlocks"].items():
        print(f"{area}: Unlocks at level {level_required}")
    
    input("Press any key to return to the Gathering Menu...")

# Function to view the resource level up table
def view_resource_level_up_table():
    clear_screen()
    gathering_data = load_json_data("skills/Gathering.json")
    
    print("Resource Unlock Table:")
    for resource in gathering_data["resource_unlocks"]:
        print(f"{resource['resource_name']}: Unlocks at level {resource['level_required']} - {resource['experience_per_gather']} XP per gather")
    
    input("Press any key to return to the Gathering Menu...")

# Function to visit gathering areas that the player has unlocked
def visit_gathering_area(player_data):
    clear_screen()
    gathering_data = load_json_data("skills/Gathering.json")
    
    print("Available Gathering Areas:")
    player_level = player_data["skills"]["Gathering"]["current"]
    unlocked_areas = [area for area, level_required in gathering_data["area_unlocks"].items() if player_level >= level_required]
    
    if not unlocked_areas:
        print("No gathering areas unlocked.")
    else:
        for idx, area in enumerate(unlocked_areas, start=1):
            print(f"{idx}. {area}")
    
    print(f"{len(unlocked_areas) + 1}. Back to Gathering Menu")
    
    choice = input("Select a gathering area or go back: ").strip()
    
    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(unlocked_areas):
            selected_area = unlocked_areas[choice - 1]
            travel_to_gathering_area(player_data, selected_area)  # Travel to the area
            gather_menu(player_data, selected_area)
            travel_back_from_gathering_area(player_data, selected_area)  # Travel back after gathering
        elif choice == len(unlocked_areas) + 1:
            return
        else:
            print("Invalid choice.")
            time.sleep(1)
    else:
        print("Invalid input.")
        time.sleep(1)

def gather_menu(player_data, selected_area):
    gathering_data = load_json_data("skills/Gathering.json")
    
    while True:
        clear_screen()
        print(f"You are at the {selected_area} gathering area.")

        print("1. Look Around")
        print("2. Start Gathering")
        print("3. Back to Gathering Areas List")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            # Display the area's description and available resources
            description = gathering_data["areas"].get(selected_area, {}).get("description", "No description available.")
            resources_in_area = gathering_data["areas"].get(selected_area, {}).get("resources", {})
            print(f"\n{description}")
            print("You spot the following resources:")

            # Get tools data to display the tool required for each resource
            tools_data = load_json_data("./items/Tools.json")

            for resource_name in resources_in_area:
                # Find the corresponding resource in the resource unlocks data
                resource_info = next((resource for resource in gathering_data["resource_unlocks"] if resource["resource_name"] == resource_name), None)
                
                if resource_info:
                    required_tool = resource_info["tool_required"]
                    print(f"- {resource_name} (Requires: {required_tool})")
            
            input("\nPress any key to return to the gathering menu...")

        elif choice == "2":
            gather_resource(player_data, selected_area)
        
        elif choice == "3":
            return  # Go back to the gathering areas list
        
        else:
            print("Invalid choice.")
            time.sleep(1)


import sys
import time

# Load tools data
def load_json_data(file_name):
    try:
        with open(file_name, "r") as file:
            tools_data = json.load(file)
            return tools_data
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")  # Error handling if the file isn't found
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")  # Error handling if JSON format is wrong
        return {}

# Function to show a progress bar and handle gathering process
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
    # Base travel time is the distance to the gathering area
    base_travel_time = distance  # In seconds or minutes, depending on how you want to scale it
    # Adjusted travel time is base travel time multiplied by the travel time modifier
    return base_travel_time * travel_time_modifier

def travel_to_gathering_area(player_data, selected_area):
    gathering_data = load_json_data("skills/Gathering.json")
    distance = gathering_data["areas"].get(selected_area, {}).get("distance", 0)

    # Automatically reset the cart's current capacity before starting the trip to gather
    player_data["travel"]["Current_Capacity"] = 0
    print("Cart emptied. Current Capacity reset to 0.")

    # Calculate the travel time using the distance and player's travel setup
    travel_time = calculate_travel_time(player_data, distance)

    print(f"Traveling to {selected_area}. This will take approximately {travel_time:.2f} seconds...")
    show_progress_bar(int(travel_time))
    print(f"Arrived at {selected_area}.")

# Travel back from the gathering area after gathering
def travel_back_from_gathering_area(player_data, selected_area):
    gathering_data = load_json_data("skills/Gathering.json")
    distance = gathering_data["areas"].get(selected_area, {}).get("distance", 0)

    # Calculate the travel time using the distance and player's travel setup
    travel_time = calculate_travel_time(player_data, distance)

    print(f"Traveling back from {selected_area}. This will take approximately {travel_time:.2f} seconds...")
    show_progress_bar(int(travel_time))
    print(f"Returned from {selected_area}.")

# Function to list the player's gathered materials in their inventory and calculate their total value
def view_resources(player_data):
    clear_screen()
    
    # Load the item data to get resource information
    item_data = load_json_data("items/Items.json")
    
    # Get the player's inventory
    inventory = player_data.get("inventory", {})
    
    print("Your current resources (Wood and Ingredients):")
    print("-" * 40)
    
    total_inventory_value = 0
    found_resources = False
    
    # Specify the categories relevant to gathering
    gathering_categories = ["Wood", "Ingredients"]
    
    # Loop through only the relevant categories in the Items.json (Wood and Ingredients)
    for category_name in gathering_categories:
        category_items = item_data["Material"].get(category_name, {})
        for resource_name, resource_info in category_items.items():
            # Check if the resource is in the player's inventory
            if resource_name in inventory:
                found_resources = True
                quantity = inventory[resource_name]
                value_per_unit = resource_info["Value"]
                total_value = quantity * value_per_unit
                total_inventory_value += total_value
                
                # Print the resource details
                print(f"{resource_name} ({category_name}):")
                print(f"  Quantity: {quantity}")
                print(f"  Value per unit: {value_per_unit} Denarius")
                print(f"  Total value: {total_value} Denarius")
                print("-" * 40)
    
    if not found_resources:
        print("No resources found in your inventory.")
    
    input("\nPress any key to return to the Gathering Menu...")

def gather_resource(player_data, selected_area):
    clear_screen()

    gathering_data = load_json_data("skills/Gathering.json")
    tools_data = load_json_data("./items/Tools.json")
    item_data = load_json_data("items/Items.json")  # Load the item data to get resource weights

    gathering_level = player_data["skills"]["Gathering"]["current"]
    
    # Check if the player has gathering tools equipped
    equipped_tools = player_data["tools"].get("Gathering", {})

    if not equipped_tools:
        print("No gathering tools equipped!")
        time.sleep(1)
        return

    resources_in_area = gathering_data["areas"].get(selected_area, {}).get("resources", {})
    unlocked_resources = []

    # Loop through the resources available in the area
    for resource_name, base_rate in resources_in_area.items():
        resource_info = next((resource for resource in gathering_data["resource_unlocks"] if resource["resource_name"] == resource_name), None)
        
        if resource_info and gathering_level >= resource_info["level_required"]:
            required_tool_type = resource_info["tool_required"]  # Check required tool type for this resource
            
            # Check if the player has the correct tool type equipped
            equipped_tool = equipped_tools.get(required_tool_type, None)
            tool_info = tools_data.get("Gathering", {}).get(required_tool_type, {}).get(equipped_tool, None)  # Fetch from Tools.json
            
            if not tool_info:
                print(f"Equipped tool {equipped_tool} does not match the required tool type {required_tool_type}.")
            else:
                # Tool is correct, proceed to gather the resource
                unlocked_resources.append((resource_name, base_rate, resource_info["experience_per_gather"], equipped_tool, tool_info))

    if not unlocked_resources:
        print("No resources available or no suitable tools equipped.")
        time.sleep(1)
        return

    print(f"Available resources in {selected_area}:")
    for idx, (resource_name, base_rate, _, equipped_tool, _) in enumerate(unlocked_resources, start=1):
        print(f"{idx}. {resource_name} (Base rate: {base_rate}, Tool: {equipped_tool})")
    print(f"{len(unlocked_resources) + 1}. Back")

    choice = input("Select a resource to gather or go back: ").strip()

    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(unlocked_resources):
            selected_resource, base_rate, experience, equipped_tool, tool_info = unlocked_resources[choice - 1]
            
            # Retrieve the weight from either the "Wood" or "Ingredients" category
            resource_weight = None
            if selected_resource in item_data["Material"].get("Wood", {}):
                resource_weight = item_data["Material"]["Wood"][selected_resource]["Weight"]
            elif selected_resource in item_data["Material"].get("Ingredients", {}):
                resource_weight = item_data["Material"]["Ingredients"][selected_resource]["Weight"]

            if resource_weight is None:
                print(f"Error: Resource weight for {selected_resource} not found.")
                return

            clear_screen()
            print(f"Gathering {selected_resource} with your {equipped_tool}... Press Ctrl+C to stop.")

            total_exp_gained = 0

            # Calculate gathering time and XP/hour
            tool_rate = tool_info["Rate"]
            gathering_time_per_resource = int(base_rate * (1 - (gathering_level / 200)) * tool_rate)
            xp_per_hour = (3600 / gathering_time_per_resource) * experience  # Direct XP/hour calculation

            # Calculate time to level
            skill = player_data["skills"]["Gathering"]
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

            print(f"Gathering time per resource: {gathering_time_per_resource} seconds | Resources gathered per hour: {3600 / gathering_time_per_resource:.2f}")
            print(f"Experience per hour: {xp_per_hour:.2f} XP/hour | Time to level: {time_to_next_level_formatted}")

            while True:
                try:
                    # Show progress bar and gather the resource
                    show_progress_bar(gathering_time_per_resource)

                    # Add resource to inventory and experience to the player
                    Player.add_item(player_data, selected_resource)
                    Player.add_experience(player_data, "Gathering", experience)
                    total_exp_gained += experience

                    # Add resource weight to the cart's current capacity
                    player_data["travel"]["Current_Capacity"] += resource_weight
                    max_capacity = player_data["travel"]["Max_Capacity"]
                    print(f"Added {selected_resource} to Cart. Current capacity: {player_data['travel']['Current_Capacity']} / {max_capacity}")

                    # Check if the cart is full
                    if player_data["travel"]["Current_Capacity"] >= max_capacity:
                        print(f"\nYour cart is full with {player_data['travel']['Current_Capacity']} units of weight!")
                        travel_back_from_gathering_area(player_data, selected_area)
                        travel_to_gathering_area(player_data, selected_area)  # Return to the area with an empty cart

                except KeyboardInterrupt:
                    print("\nGathering interrupted. Returning to the previous menu.")
                    break
        elif choice == len(unlocked_resources) + 1:
            return
        else:
            print("Invalid choice.")
            time.sleep(1)
    else:
        print("Invalid input.")
        time.sleep(1)
