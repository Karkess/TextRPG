import json
import os
import re
import math
import random
from utils import *

# Get the stats of a specific item by name from the Equipment JSON
def get_item_stats(item_name, equipment_data):
    for category in equipment_data.values():
        for slot_items in category.values():
            for item in slot_items:
                if item["name"] == item_name:
                    return item["stats"]
    return {}

# Calculate the player's stats based on base stats, class modifiers, equipment, temporary boosts, and agility
def calculate_player_stats(player_data, equipment_data):
    # Initialize the base stats
    stats = {
        "health": {"base": player_data["health"]["base"], "class": 0, "equipment": 0, "boost": 0},
        "strength": {"base": player_data["strength"]["base"], "class": 0, "equipment": 0, "boost": 0},
        "magical_attack": {"base": player_data["magical_attack"]["base"], "class": 0, "equipment": 0, "boost": 0},
        "physical_defense": {"base": player_data["physical_defense"]["base"], "class": 0, "equipment": 0, "boost": 0},
        "magic_defense": {"base": player_data["magic_defense"]["base"], "class": 0, "equipment": 0, "boost": 0},
        "physical_accuracy": {"base": player_data["physical_accuracy"]["base"], "class": 0, "equipment": 0, "boost": 0},
        "magical_accuracy": {"base": player_data["magical_accuracy"]["base"], "class": 0, "equipment": 0, "boost": 0},
        "dexterity": {"base": player_data["dexterity"]["base"], "class": 0, "equipment": 0, "boost": 0, "agility": 0},
    }

    # Add 100% of the primary class stats
    primary_class = player_data["primary_class"]
    primary_stats = player_data["classes"][primary_class]
    for key in stats.keys():
        stats[key]["class"] += primary_stats.get(key, 0)

    # Add 50% of the secondary class stats, rounding up
    secondary_class = player_data["secondary_class"]
    secondary_stats = player_data["classes"][secondary_class]
    for key in stats.keys():
        secondary_value = secondary_stats.get(key, 0)
        stats[key]["class"] += math.ceil(secondary_value * 0.5)

    # Add stats from equipped items
    for slot, item_name in player_data["equipped"]["weapons"].items():
        if item_name:
            item_stats = get_item_stats(item_name, equipment_data)
            for stat, value in item_stats.items():
                if stat in stats:
                    stats[stat]["equipment"] += value

    for slot, item_name in player_data["equipped"]["armor"].items():
        if item_name:
            item_stats = get_item_stats(item_name, equipment_data)
            for stat, value in item_stats.items():
                if stat in stats:
                    stats[stat]["equipment"] += value

    # Add temporary boosts from the player data
    if "boosts" in player_data:
        for stat, boost_value in player_data["boosts"].items():
            if stat in stats:
                stats[stat]["boost"] += boost_value

    # Add 5 to dexterity for each level in Agility
    agility_level = player_data["skills"]["Agility"]["current"]
    stats["dexterity"]["agility"] += agility_level * 5

    return stats

# Function to display weapon and offhand stats
def display_weapon_and_offhand(player_data, equipment_data):
    output = []

    # Main hand
    main_hand = player_data["equipped"]["weapons"].get("main_hand")
    if main_hand:
        main_hand_stats = get_item_stats(main_hand, equipment_data)
        if main_hand:
            main_hand_output = f"{main_hand}:"
            if "attack" in main_hand_stats:
                main_hand_output += f" Attack {main_hand_stats['attack']}"
            if "magical_attack" in main_hand_stats:
                main_hand_output += f" | Magical Attack {main_hand_stats['magical_attack']}"
            if "parry" in main_hand_stats:
                main_hand_output += f" | Parry {main_hand_stats['parry']}"
            output.append(main_hand_output)

    # Offhand
    offhand = player_data["equipped"]["weapons"].get("offhand")
    if offhand:
        offhand_stats = get_item_stats(offhand, equipment_data)
        if offhand:
            offhand_output = f"{offhand}:"
            if "attack" in offhand_stats:
                offhand_output += f" Attack {offhand_stats['attack']}"
            if "magical_attack" in offhand_stats:
                offhand_output += f" | Magical Attack {offhand_stats['magical_attack']}"
            if "parry" in offhand_stats:
                offhand_output += f" | Parry {offhand_stats['parry']}"
            if "block" in offhand_stats:
                offhand_output += f" | Block {offhand_stats['block']}"
            output.append(offhand_output)

    # Join and print output
    if output:
        print("\nWielded:")
        for line in output:
            print(line)

# Function to display stats in the requested format
def check_stats(player_data, equipment_data):
    # Print player's level and class details
    print(f"Level: {player_data['level']}")
    primary_class = player_data["primary_class"]
    primary_class_level = player_data["classes"][primary_class]["level"]
    secondary_class = player_data["secondary_class"]
    secondary_class_level = player_data["classes"][secondary_class]["level"]
    print(f"Primary Class: {primary_class} | Level: {primary_class_level}")
    print(f"Secondary Class: {secondary_class} | Level: {secondary_class_level}")

    # Calculate and display combat stats
    stats = calculate_player_stats(player_data, equipment_data)
    print("\nCombat Stats:")
    for stat, values in stats.items():
        base = values["base"]
        class_bonus = values["class"]
        equipment_bonus = values["equipment"]
        boost_bonus = values["boost"]

        # Add the Agility contribution for Dexterity
        if stat == "dexterity":
            agility_bonus = values.get("agility", 0)
            total = base + class_bonus + equipment_bonus + boost_bonus + agility_bonus
            print(f"{stat.capitalize()}: {total} ({base} Base + {class_bonus} Classes + {equipment_bonus} Equipment + {boost_bonus} Temporary Boosts + {agility_bonus} Agility)")
        else:
            total = base + class_bonus + equipment_bonus + boost_bonus
            print(f"{stat.capitalize()}: {total} ({base} Base + {class_bonus} Classes + {equipment_bonus} Equipment + {boost_bonus} Temporary Boosts)")

    # After displaying all stats, display the equipment info
    display_weapon_and_offhand(player_data, equipment_data)

# Main function to check stats, now accepting player_data as an argument
def check_player_stats(player_data):
    # Load equipment data
    equipment_data = load_json_data("items/Equipment.json")

    # Check stats
    check_stats(player_data, equipment_data)

# Combat stats calculation function
def calculate_combat_stats(player_data, equipment_data):
    # Initialize the base stats
    if isinstance(player_data["health"], dict):
        health_base = player_data["health"]["base"]
    else:
        health_base = player_data["health"]  # Handle the case where health is a plain integer

    stats = {
        "health": {"base": health_base, "class": 0, "equipment": 0, "boost": 0},
        "strength": {"base": player_data["strength"]["base"] if isinstance(player_data["strength"], dict) else player_data["strength"], "class": 0, "equipment": 0, "boost": 0},
        "magical_attack": {"base": player_data["magical_attack"]["base"] if isinstance(player_data["magical_attack"], dict) else player_data["magical_attack"], "class": 0, "equipment": 0, "boost": 0},
        "physical_defense": {"base": player_data["physical_defense"]["base"] if isinstance(player_data["physical_defense"], dict) else player_data["physical_defense"], "class": 0, "equipment": 0, "boost": 0},
        "magic_defense": {"base": player_data["magic_defense"]["base"] if isinstance(player_data["magic_defense"], dict) else player_data["magic_defense"], "class": 0, "equipment": 0, "boost": 0},
        "physical_accuracy": {"base": player_data["physical_accuracy"]["base"] if isinstance(player_data["physical_accuracy"], dict) else player_data["physical_accuracy"], "class": 0, "equipment": 0, "boost": 0},
        "magical_accuracy": {"base": player_data["magical_accuracy"]["base"] if isinstance(player_data["magical_accuracy"], dict) else player_data["magical_accuracy"], "class": 0, "equipment": 0, "boost": 0},
        "dexterity": {"base": player_data["dexterity"]["base"] if isinstance(player_data["dexterity"], dict) else player_data["dexterity"], "class": 0, "equipment": 0, "boost": 0, "agility": 0},
    }

    # Add 100% of the primary class stats (if applicable)
    if "primary_class" in player_data:
        primary_class = player_data["primary_class"]
        primary_stats = player_data["classes"][primary_class]
        for key in stats.keys():
            stats[key]["class"] += primary_stats.get(key, 0)

    # Add 50% of the secondary class stats (if applicable)
    if "secondary_class" in player_data:
        secondary_class = player_data["secondary_class"]
        secondary_stats = player_data["classes"][secondary_class]
        for key in stats.keys():
            stats[key]["class"] += math.ceil(secondary_stats.get(key, 0) * 0.5)

    # Add stats from equipped items if it's a player
    if "equipped" in player_data:
        for slot, item_name in player_data["equipped"]["weapons"].items():
            if item_name:
                item_stats = get_item_stats(item_name, equipment_data)
                for stat, value in item_stats.items():
                    if stat in stats:
                        stats[stat]["equipment"] += value

        for slot, item_name in player_data["equipped"]["armor"].items():
            if item_name:
                item_stats = get_item_stats(item_name, equipment_data)
                for stat, value in item_stats.items():
                    if stat in stats:
                        stats[stat]["equipment"] += value

    # Add temporary boosts
    if "boosts" in player_data:
        for stat, boost_value in player_data["boosts"].items():
            if stat in stats:
                stats[stat]["boost"] += boost_value

    # Add 5 to dexterity for each level in Agility if applicable
    if "skills" in player_data and "Agility" in player_data["skills"]:
        agility_level = player_data["skills"]["Agility"]["current"]
        stats["dexterity"]["agility"] += agility_level * 5

    # Calculate total stats
    total_stats = {}
    for stat, values in stats.items():
        total_stats[stat] = values["base"] + values["class"] + values["equipment"] + values["boost"]

    # Calculate fatigue and mana for combat use (but don't display them)
    total_stats["fatigue"] = 100 + 2 * total_stats["strength"] + 2 * total_stats["dexterity"]
    total_stats["mana"] = 100 + 2 * total_stats["magical_attack"] + 2 * total_stats["magic_defense"] + 2 * total_stats["magical_accuracy"]

    return total_stats


# Use combat_stats for all combat calculations
def calculate_physical_damage(user, target, attack_data):
    strength = user["combat_stats"]["strength"]  # Use combat_stats
    physical_defense = target["combat_stats"]["physical_defense"]  # Use combat_stats
    accuracy = attack_data["accuracy"]

    # Continue with the rest of the combat calculation...


    # Step 1: Calculate Multiplier
    defense_multiplier = strength / max(physical_defense, 1)  # Avoid dividing by zero
    multiplier = max(0.1, min(2.0, defense_multiplier))  # Cap multiplier between 0.1 and 2.0

    # Step 2: Dodge check
    dodge_chance = target["combat_stats"]["dexterity"] - user["combat_stats"]["physical_accuracy"]
    if random.random() * 100 < max(0, dodge_chance):
        return {"damage": 0, "missed": True, "blocked": False, "flavor_text": f"{target['name']} dodged the attack!"}

    # Step 3: Block check
    block_chance = target["combat_stats"]["dexterity"] - user["combat_stats"]["dexterity"]
    if random.random() * 100 < max(0, block_chance):
        return {"damage": 0, "missed": False, "blocked": True, "flavor_text": f"{target['name']} blocked the attack!"}

    # Step 4: Accuracy check
    final_accuracy = accuracy - (target["combat_stats"]["dexterity"] / 2)
    if random.random() * 100 > final_accuracy:
        return {"damage": 0, "missed": True, "blocked": False, "flavor_text": f"{user['name']} missed the attack!"}

    # Step 5: Calculate Damage
    base_damage = attack_data["power"] * multiplier
    return {"damage": round(base_damage), "missed": False, "blocked": False, "flavor_text": attack_data["flavor_text"]}


# Magical damage calculation
def calculate_magical_damage(user, target, attack_data):
    magical_attack = user["combat_stats"]["magical_attack"]
    magic_defense = target["combat_stats"]["magic_defense"]
    accuracy = attack_data["accuracy"]

    # Step 1: Calculate Multiplier
    defense_multiplier = magical_attack / max(magic_defense, 1)  # Avoid dividing by zero
    multiplier = max(0.1, min(2.0, defense_multiplier))  # Cap multiplier between 0.1 and 2.0

    # Step 2: Dodge check (still using dexterity for magic dodge)
    dodge_chance = target["combat_stats"]["dexterity"] - user["combat_stats"]["magical_accuracy"]
    if random.random() * 100 < max(0, dodge_chance):
        return {"damage": 0, "missed": True, "blocked": False, "flavor_text": f"{target['name']} dodged the spell!"}

    # Step 3: Accuracy check
    final_accuracy = accuracy - (target["combat_stats"]["dexterity"] / 2)
    if random.random() * 100 > final_accuracy:
        return {"damage": 0, "missed": True, "blocked": False, "flavor_text": f"{user['name']} missed the spell!"}

    # Step 4: Calculate Damage
    base_damage = attack_data["power"] * multiplier
    return {"damage": round(base_damage), "missed": False, "blocked": False, "flavor_text": attack_data["flavor_text"]}

# Execute an attack (Physical, Magical, or Special)
# Execute an attack (Physical, Magical, or Special)
def execute_attack(attacker, target, attack_name, attack_data, enemies):
    attack_type = attack_data["type"]

    # Handle different attack types
    if attack_type == "Physical":
        result = calculate_physical_damage(attacker, target, attack_data)
    elif attack_type == "Magical":
        result = calculate_magical_damage(attacker, target, attack_data)
    elif attack_type == "Special":
        from combat.SpecialAttacks import handle_special_effect
        # Handle special effects on multiple or single opponents
        if attack_data['targeting'] == "All Opponents":
            alive_enemies = [enemy for enemy in enemies if enemy['alive']]
            result = handle_special_effect(attacker, alive_enemies, attack_data['special_effect'])
            try:
                if not result["missed"] and not result["blocked"]:
                    target['combat_stats']['health'] = max(0, target['combat_stats']['health'] - result["damage"])
            except Exception as e:
                return result

        else:
            result = handle_special_effect(attacker, target, attack_data['special_effect'])
            try:
                if not result["missed"] and not result["blocked"]:
                    target['combat_stats']['health'] = max(0, target['combat_stats']['health'] - result["damage"])
            except Exception as e:
                return result
        
        # Set result for damage to 0 if it's a special effect (since special effects may not deal direct damage)
        result = {"damage": 0, "missed": False, "blocked": False, "flavor_text": attack_data.get("flavor_text", "")}

    # If the attack was not missed or blocked, deduct health for physical and magical attacks
    if not result["missed"] and not result["blocked"]:
        target['combat_stats']['health'] = max(0, target['combat_stats']['health'] - result["damage"])

    # Apply text formatting to the flavor text for all attack types
    formatted_flavor_text = apply_text_formatting(result["flavor_text"])

    # Return the final combat message with formatted text for all attack types
    return formatted_flavor_text.format(
        user=attacker['name'], 
        target=target['name'], 
        damage=result["damage"]
    )




def select_basic_ai_attack(enemy):
    weights = enemy["AI"]["weights"]
    attacks = list(weights.keys())
    weight_values = list(weights.values())
    
    # Select a random attack based on the weights
    chosen_attack = random.choices(attacks, weights=weight_values, k=1)[0]
    return chosen_attack
