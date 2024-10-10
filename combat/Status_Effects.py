import json
import math
from utils import load_json_data

def apply_status_effect(character, effect_name, effect_type, duration, stacks=1):
    status_effects = load_json_data("./combat/Status_Effects.json")

    if effect_type == "buff":
        effect_info = status_effects['Buffs'].get(effect_name)
    elif effect_type == "debuff":
        effect_info = status_effects['Debuffs'].get(effect_name)

    if not effect_info:
        print(f"Status effect {effect_name} not found!")
        return

    # Ensure status_effects is initialized
    if 'status_effects' not in character:
        character['status_effects'] = {'buffs': {}, 'debuffs': {}}

    # Check the type of effect
    effect_category = 'buffs' if effect_type == "buff" else 'debuffs'

    # Ensure the effect category is initialized
    if effect_category not in character['status_effects']:
        character['status_effects'][effect_category] = {}

    existing_effect = character['status_effects'][effect_category].get(effect_name)

    if existing_effect:
        refresh_info = effect_info.get('On_Refresh', {})

        # Handle stacks on refresh
        if isinstance(effect_info.get('Stacks'), int):
            if refresh_info.get('Stacks') == "stack":
                existing_effect['stacks'] = min(
                    existing_effect['stacks'] + stacks,
                    effect_info['Stacks']  # This is now the max stack
                )
            elif refresh_info.get('Stacks') == "refresh":
                existing_effect['stacks'] = stacks

        # Handle duration on refresh
        if refresh_info.get('Duration') == "refresh":
            existing_effect['duration'] = duration
        elif refresh_info.get('Duration') == "stack":
            existing_effect['duration'] += duration
    else:
        # Apply a new status effect
        character['status_effects'][effect_category][effect_name] = {
            'duration': duration,
            'stacks': stacks if isinstance(effect_info.get('Stacks'), int) else 1
        }

    print(f"{effect_name} applied to {character['name']}. Stacks: {stacks}, Duration: {duration}")




# Remove a status effect
def remove_status_effect(character, effect_name, effect_type):
    status_effects = load_json_data("./combat/Status_Effects.json")
    
    if effect_type == "buff":
        effect_info = status_effects['Buffs'].get(effect_name)
    elif effect_type == "debuff":
        effect_info = status_effects['Debuffs'].get(effect_name)
    
    if not effect_info or not effect_info.get('Removable', True):
        print(f"{effect_name} cannot be removed!")
        return
    
    if effect_name in character['status_effects'][effect_type]:
        del character['status_effects'][effect_type][effect_name]
        print(f"{effect_name} removed from {character['name']}.")


# Strength Boost Effect
def apply_strength_boost(character, stacks):
    boost_value = 0.1 * stacks
    character['combat_stats']['strength'] = round(character['combat_stats']['strength'] * (1 + boost_value))
    print(f"{character['name']} gains {boost_value * 100}% strength boost from Strength Boost.")

# Poison Damage Effect
def apply_poison_damage(character, stacks):
    poison_damage = math.floor(character['combat_stats']['health'] * 0.05 * stacks)  # Calculate poison damage
    character['combat_stats']['health'] -= poison_damage  # Apply damage to current_health
    print(f"{character['name']} takes {poison_damage} poison damage from Poison.")

def heal(character, amount):
    current_health = character['combat_stats']['health']
    max_health = character['stats']['health']
    new_health = min(current_health + amount, max_health)
    character['combat_stats']['health'] = new_health
    return f"{character['name']} restores {amount} health (Current: {new_health}/{max_health})."

