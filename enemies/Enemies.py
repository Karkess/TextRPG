import json
import random

# Load JSON data
with open("enemies.json") as file:
    enemy_data = json.load(file)

# Function to create an enemy from template
def create_enemy(enemy_type):
    enemy_template = enemy_data[enemy_type]
    level = eval(enemy_template["level"])
    health = eval(enemy_template["base_health"])
    strength = eval(enemy_template["base_strength"])
    magical_attack = eval(enemy_template["base_magical_attack"])
    physical_defense = eval(enemy_template["base_physical_defense"])
    magic_defense = eval(enemy_template["base_magic_defense"])
    physical_accuracy = eval(enemy_template["base_physical_accuracy"])
    magical_accuracy = eval(enemy_template["base_magical_accuracy"])
    experience = eval(enemy_template["experience"])
    
    # Generating the drop table
    drop_table = []
    for drop in enemy_template["drop_table"]:
        drop_quantity = eval(drop["quantity"]) if isinstance(drop["quantity"], str) else drop["quantity"]
        drop_table.append((drop["item"], drop["chance"], drop_quantity))
    
    return {
        "type": enemy_type,
        "level": level,
        "health": health,
        "strength": strength,
        "magical_attack": magical_attack,
        "physical_defense": physical_defense,
        "magic_defense": magic_defense,
        "physical_accuracy": physical_accuracy,
        "magical_accuracy": magical_accuracy,
        "experience": experience,
        "attacks": enemy_template["attacks"],
        "drop_table": drop_table
    }
