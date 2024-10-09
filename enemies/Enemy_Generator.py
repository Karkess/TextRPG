import json
import random

# Helper function to process formula input
def process_formula_input(formula_input):
    # Translate "L" to "level" in the input
    formula_input = formula_input.replace("L", "level")
    
    # If there's a comma, it means random.randint is needed for integers
    if "," in formula_input:
        base, rand_range = formula_input.split("+") if "+" in formula_input else ("0", formula_input)
        base = base.strip()
        if "*" in rand_range:
            rand_range_min, rand_range_max = rand_range.split("*")
        else:
            rand_range_min, rand_range_max = rand_range.split(",")
        rand_range_min = rand_range_min.strip()
        rand_range_max = rand_range_max.strip()
        return f"{base} + random.randint({rand_range_min}, {rand_range_max})"
    else:
        # If no comma, just return the input as is
        return formula_input.strip()

def add_enemy_to_json(file_name):
    try:
        # Load existing data from the JSON file
        with open(file_name, "r") as file:
            enemy_data = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty dictionary
        enemy_data = {}

    # Prompt for the new enemy details
    enemy_name = input("Enter the enemy name: ").strip()
    if enemy_name in enemy_data:
        print(f"Enemy '{enemy_name}' already exists in the file.")
        return

    enemy_description = input("Enter the enemy description: ").strip()

    # Ask for level range and create random.randint formula
    level_range = input("Enter the level range (e.g., 5,7): ").strip()
    level_min, level_max = map(float, level_range.split(","))
    level_formula = f"random.randint({level_min}, {level_max})"

    # Ask if player needs formula assistance
    assist_with_formulas = input("Would you like formula assistance? (Yes/yes/Y/y/(blank) for yes): ").strip().lower()
    use_formula_assistance = assist_with_formulas in ["yes", "y", ""]

    # Function to handle formula input with or without assistance
    def get_stat_input(prompt):
        if use_formula_assistance:
            user_input = input(f"{prompt} (use commas for random range, e.g., '250+5,20'): ").strip()
            return process_formula_input(user_input)
        else:
            return input(f"{prompt}: ").strip()

    health_formula = get_stat_input("Enter the base health formula")
    strength_formula = get_stat_input("Enter the base strength formula")
    magical_attack_formula = get_stat_input("Enter the base magical attack formula")
    physical_defense_formula = get_stat_input("Enter the base physical defense formula")
    magic_defense_formula = get_stat_input("Enter the base magic defense formula")
    physical_accuracy_formula = get_stat_input("Enter the base physical accuracy formula")
    magical_accuracy_formula = get_stat_input("Enter the base magical accuracy formula")
    experience_formula = get_stat_input("Enter the experience formula")

    # Prompt for attacks (enter attacks one by one)
    attacks = []
    print("Enter the enemy's attacks (type 'done' when finished):")
    while True:
        attack = input("Enter attack: ").strip()
        if attack.lower() == "done":
            break
        attacks.append(attack)

    # Prompt for drop table with 'weight' instead of 'chance'
    drop_table = []
    print("Enter the enemy's drops (item, weight, quantity), type 'done' when finished:")
    while True:
        item = input("Enter drop item name: ").strip()
        if item.lower() == "done":
            break
        weight = float(input(f"Enter drop weight for {item} (0.0 to 1.0): ").strip())
        quantity_formula = get_stat_input(f"Enter quantity formula for {item} (e.g., random.randint(1, 5)): ").strip()
        drop_table.append({"item": item, "weight": weight, "quantity": quantity_formula})

    # Create the new enemy entry
    new_enemy = {
        "description": enemy_description,
        "level": level_formula,
        "base_health": health_formula,
        "base_strength": strength_formula,
        "base_magical_attack": magical_attack_formula,
        "base_physical_defense": physical_defense_formula,
        "base_magic_defense": magic_defense_formula,
        "base_physical_accuracy": physical_accuracy_formula,
        "base_magical_accuracy": magical_accuracy_formula,
        "experience": experience_formula,
        "attacks": attacks,
        "drop_table": drop_table
    }

    # Add the new enemy to the enemy_data dictionary
    enemy_data[enemy_name] = new_enemy

    # Save the updated enemy data back to the JSON file
    with open(file_name, "w") as file:
        json.dump(enemy_data, file, indent=4)

    print(f"Enemy '{enemy_name}' added successfully!")

# Example usage
file_name = "./enemies/Enemies.json"
add_enemy_to_json(file_name)
