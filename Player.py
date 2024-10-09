import json
import math
import numpy as np

# Load level-up table
def load_level_up_table(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{file_name} not found.")
        return {}

# Load player data from JSON
def load_player(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{file_name} not found. Creating a new player.")
        return create_new_player()

# Save player data to JSON
def save_player(player_data, file_name):
    with open(file_name, "w") as file:
        json.dump(player_data, file, indent=4)

# Add experience to a skill and check for level-ups
def add_experience(player_data, skill_name, experience_gained):
    # Load the level-up table
    level_up_table = load_level_up_table("./skills/LevelUpTable.json")
    
    # Get the current skill level and experience
    skill = player_data["skills"].get(skill_name)
    if not skill:
        print(f"Skill '{skill_name}' not found.")
        return
    
    # Add experience
    skill["experience"] += experience_gained
    current_level = skill["current"]
    current_xp = skill["experience"]
    
    # Check for level-up
    while str(current_level + 1) in level_up_table and current_xp >= level_up_table[str(current_level + 1)]:
        current_level += 1
        print(f"Congratulations! You've reached level {current_level} in {skill_name}.")
    
    # Calculate the XP needed for the next level
    if str(current_level + 1) in level_up_table:
        xp_for_next_level = level_up_table[str(current_level + 1)] - current_xp
    else:
        xp_for_next_level = "MAX"  # If max level is reached
    
    # Print formatted status on one line
    print(f"Gained {experience_gained} {skill_name} experience.")
    print(f"{skill_name}: Level: {current_level} | Current Experience: {current_xp} | Needed for Level {current_level + 1}: {xp_for_next_level}\n")
    
    # Update skill level
    skill["current"] = current_level
    
    # Save player data after experience gain
    save_player(player_data, f"./saves/{player_data['name']}-SaveData.json")


# Add item to the player's inventory
def add_item(player_data, item_name, quantity=1):
    # Add the item to the inventory
    player_data["inventory"][item_name] = player_data["inventory"].get(item_name, 0) + quantity
    
    # Display total quantity of the item
    total_quantity = player_data["inventory"][item_name]
    print(f"Added {quantity} {item_name}(s) to inventory. Total: {total_quantity}")
    
    # Save player data after adding item
    save_player(player_data, f"./saves/{player_data['name']}-SaveData.json")

# Load travel data (carts, animals) from Travel.json
def load_travel_data(file_name="./items/Travel.json"):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{file_name} not found.")
        return {}

# Calculate total stats and travel modifier based on Travel.json
def calculate_travel_stats(player_data):
    travel_data = load_travel_data()
    
    # Get the equipped cart and animals
    cart_name = player_data["travel"].get("Cart")
    animals = player_data["travel"].get("Animals", [])
    
    # Fetch the cart's base stats
    cart = travel_data.get("Carts", {}).get(cart_name, None)
    if not cart:
        print(f"Cart '{cart_name}' not found in Travel.json")
        return

    # Initialize the base stats from the cart
    cart_speed = cart["Speed"]
    cart_capacity = cart["Weight Capacity"]
    
    # Initialize the total strength and speed values
    total_speed = cart_speed
    total_capacity = cart_capacity
    
    # Add animal bonus stats
    if animals:
        total_animal_speed = 0
        total_animal_capacity = 0
        for animal_name in animals:
            animal = travel_data.get("Animals", {}).get(animal_name, None)
            if animal:
                total_animal_speed += animal["Speed"]
                total_animal_capacity += animal["Bonus Capacity"]
        
        # Calculate the average animal speed
        total_speed += total_animal_speed / len(animals)
        # Add the bonus capacity from animals
        total_capacity += total_animal_capacity

    # Get current and max capacities from the player's travel section
    current_capacity = player_data["travel"]["Current_Capacity"]
    player_data["travel"]["Max_Capacity"] = total_capacity
    
    # Calculate the load ratio
    load_ratio = current_capacity / total_capacity

    decay_rate = 0.75  # Decay rate for load factor
    load_factor = np.exp(-load_ratio * decay_rate)
    adjusted_speed = total_speed * load_factor
    
    # Calculate the travel time modifier
    base_travel_time = 1.0  # Assume base time of 1.0
    travel_time_modifier = base_travel_time / adjusted_speed
    
    # Print the calculated stats
    print(f"Cart: {cart_name}")
    print(f"Animals: {', '.join(animals) if animals else 'None'}")
    print(f"Total Speed: {adjusted_speed}")
    print(f"Current Capacity: {current_capacity}/{total_capacity}")
    print(f"Travel Time Modifier: {travel_time_modifier:.2f} (x faster/slower)")

    return travel_time_modifier

# Display the travel details and modifier
def display_travel_stats(player_data):
    modifier = calculate_travel_stats(player_data)
    if modifier:
        print(f"Your travel time is {modifier:.2f} times the base travel time.")

# Create a new player with default values
def create_new_player(PlayerName):
    return {
        "name": f"{PlayerName}",
        "description": "A brave adventurer.",
        "level": 1,
        "health": {"base": 100, "current": 100, "max": 100},
        "strength": {"base": 10, "current": 10, "max": 10},
        "magical_attack": {"base": 5, "current": 5, "max": 5},
        "physical_defense": {"base": 8, "current": 8, "max": 8},
        "magic_defense": {"base": 6, "current": 6, "max": 6},
        "physical_accuracy": {"base": 70, "current": 70, "max": 70},
        "magical_accuracy": {"base": 60, "current": 60, "max": 60},
        "experience": 0,
        "attacks": ["Punch", "Fireball"],
        "primary_class": "Warrior",
        "secondary_class": "Mage",
        "classes": {
            "Warrior": {
                "level": 1,
                "experience": 0,
                "health_modifier": 50,
                "strength_modifier": 20,
                "magical_attack_modifier": 0,
                "physical_defense_modifier": 15,
                "magic_defense_modifier": 5,
                "physical_accuracy_modifier": 10,
                "magical_accuracy_modifier": 0,
                "attacks": ["Slash", "Power Strike"]
            },
            "Mage": {
                "level": 1,
                "experience": 0,
                "health_modifier": 20,
                "strength_modifier": 5,
                "magical_attack_modifier": 40,
                "physical_defense_modifier": 5,
                "magic_defense_modifier": 25,
                "physical_accuracy_modifier": 5,
                "magical_accuracy_modifier": 15,
                "attacks": ["Magic Missile", "Fireball"]
            }
        },
        "skills": {
            "Mining": {"current": 1, "max": 99, "experience": 0},
            "Smithing": {"current": 1, "max": 99, "experience": 0},
            "Crafting": {"current": 1, "max": 99, "experience": 0},
            "Fletching": {"current": 1, "max": 99, "experience": 0},
            "Chemistry": {"current": 1, "max": 99, "experience": 0},
            "Alchemy": {"current": 1, "max": 99, "experience": 0},
            "Gathering": {"current": 1, "max": 99, "experience": 0},
            "Hunting": {"current": 1, "max": 99, "experience": 0},
            "Fishing": {"current": 1, "max": 99, "experience": 0},
            "Cooking": {"current": 1, "max": 99, "experience": 0},
            "Construction": {"current": 1, "max": 99, "experience": 0},
            "Bartering": {"current": 1, "max": 99, "experience": 0}
        },
        "inventory": {
            "Denarius": 50
        },
        "tools": {
            "Mining": "Rusty Pickaxe"
        },
        "travel": {
            "Cart": "Handcart",
            "Animals": [],
            "Capacity": 100
        }
    }
