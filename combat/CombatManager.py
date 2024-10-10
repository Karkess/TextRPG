import random
import os
import json
import math
import time
from utils import *
from combat.CombatLogic import execute_attack, calculate_combat_stats, select_basic_ai_attack
from enemies.AdvancedAI import select_advanced_ai_attack  # Custom AI logic for advanced enemies
from combat.SpecialAttacks import handle_special_effect  # Handle special attacks
import importlib
from Player import save_player

# Dynamically import the Status_Effects module
status_effects_module = importlib.import_module('combat.Status_Effects')


def load_enemy_data(enemy_names):
    with open(resource_path("./enemies/Enemies.json")) as file:
        enemies_data = json.load(file)

    enemies = []
    for enemy_name in enemy_names:
        if enemy_name in enemies_data:
            enemy = enemies_data[enemy_name].copy()  # Get a copy of enemy data
            
            # First, evaluate the level
            level = eval(enemy['level'])  # Ensure level is calculated first
            enemy['level'] = level
            
            # Create a context for eval with the evaluated level and random module
            context = {"level": level, "random": random}

            # Then, evaluate other stats that depend on level
            enemy['health'] = eval(enemy['health'], context)
            enemy['strength'] = eval(enemy['strength'], context)
            enemy['magical_attack'] = eval(enemy['magical_attack'], context)
            enemy['physical_defense'] = eval(enemy['physical_defense'], context)
            enemy['magic_defense'] = eval(enemy['magic_defense'], context)
            enemy['physical_accuracy'] = eval(enemy['physical_accuracy'], context)
            enemy['magical_accuracy'] = eval(enemy['magical_accuracy'], context)
            enemy['dexterity'] = eval(enemy['dexterity'], context)
            enemy['experience'] = eval(enemy['experience'], context)

            # Add the enemy's name as a field
            enemy['name'] = enemy_name

            # Evaluate drop table items (optional, depends on how drops are handled)
            for drop in enemy['drop_table']:
                drop['quantity'] = eval(drop['quantity'], context)

            enemies.append(enemy)
        else:
            print(f"Enemy '{enemy_name}' not found in Enemies.json")
    
    return enemies

def display_combat_status(player, enemies):
    # Format the player's health, fatigue, and mana
    print(apply_text_formatting(f"\n{CYAN}{BOLD}{player['name']}{RESET}"))
    print(f"Health: {player['combat_stats']['health']} | Fatigue: {player['combat_stats']['fatigue']} | Mana: {player['combat_stats']['mana']}")
    
    # Display player buffs and debuffs with stacks and durations
    status_effects = []
    buffs = player['status_effects'].get('buffs', {})
    for buff_name, buff_info in buffs.items():
        stack_text = f"{buff_info['stacks']}x " if buff_info['stacks'] > 1 else ""
        status_effects.append(f"{GREEN}{stack_text}{buff_name} ({buff_info['duration']}){RESET}")
    
    debuffs = player['status_effects'].get('debuffs', {})
    for debuff_name, debuff_info in debuffs.items():
        stack_text = f"{debuff_info['stacks']}x " if debuff_info['stacks'] > 1 else ""
        status_effects.append(f"{RED}{stack_text}{debuff_name} ({debuff_info['duration']}){RESET}")
    
    if status_effects:
        print(f"({', '.join(status_effects)})")
    
    # Display enemies' status
    for i, enemy in enumerate(enemies):
        if enemy['alive']:
            # Apply the name color from the enemy's data
            enemy_name = apply_text_formatting(f"{enemy['name_color']}{enemy['name']}{RESET}")
            print(f"\n{enemy_name}")
            print(f"Health: {enemy['combat_stats']['health']} | Fatigue: {enemy['combat_stats']['fatigue']} | Mana: {enemy['combat_stats']['mana']}")
            
            # Display enemy buffs and debuffs with stacks and durations
            status_effects = []
            buffs = enemy['status_effects'].get('buffs', {})
            for buff_name, buff_info in buffs.items():
                stack_text = f"{buff_info['stacks']}x " if buff_info['stacks'] > 1 else ""
                status_effects.append(f"{GREEN}{stack_text}{buff_name} ({buff_info['duration']}){RESET}")
            
            debuffs = enemy['status_effects'].get('debuffs', {})
            for debuff_name, debuff_info in debuffs.items():
                stack_text = f"{debuff_info['stacks']}x " if debuff_info['stacks'] > 1 else ""
                status_effects.append(f"{RED}{stack_text}{debuff_name} ({debuff_info['duration']}){RESET}")

            if status_effects:
                print(f"({', '.join(status_effects)})")
        elif not enemy['alive']:
            print(f"\n{ITALIC}{enemy['name']} is Recently Deceased.{RESET}")


def display_combat_start(player, enemies):
    clear_screen()  # Clear the screen before displaying combat
    
    # Apply text formatting to the player's display
    print(apply_text_formatting(f"{CYAN}{BOLD}{player['name']}{RESET} - Level {player['level']}"))
    print(f"Health: {player['stats']['health']} | Fatigue: {player['stats']['fatigue']} | Mana: {player['stats']['mana']}\n")
    
    for i, enemy in enumerate(enemies):
        if enemy['alive']:
            # Format the entry message and name with the custom color
            print(apply_text_formatting(f"{enemy['entry_message']}{RESET}"))
            enemy_name = apply_text_formatting(f"{BOLD}{enemy['name_color']}{enemy['name']}{RESET}")
            print(f"{enemy_name} - Level {enemy['level']}")
            print(f"Health: {enemy['stats']['health']} | Fatigue: {enemy['stats']['fatigue']} | Mana: {enemy['stats']['mana']}\n")


# Flee logic
def attempt_flee(player, enemies):
    player_dexterity = player["combat_stats"]["dexterity"]
    total_enemy_dexterity = sum(enemy["combat_stats"]["dexterity"] for enemy in enemies)
    flee_chance = 50 + player_dexterity / 100 - total_enemy_dexterity / 100
    
    if "flee_blocked" in player and player["flee_blocked"]:
        print("Escape is impossible in this situation!")
        return False

    flee_roll = random.random() * 100
    if flee_roll < flee_chance:
        print(f"{player['name']} successfully fled!")
        return True
    else:
        print(f"{player['name']} failed to flee!")
        return False

# Player action menu
def player_action_menu(player, attacks_data):
    print("\nChoose an action:")
    print("1. Attack")
    print("2. Magic")
    print("3. Skills")
    print("4. Special")
    print("5. Consumables")
    print("6. Flee")
    
    choice = input("Enter your choice: ").strip()
    
    if choice == "1":
        return "Attack"
    elif choice == "2":
        return "Magic"
    elif choice == "3":
        return "Skills"
    elif choice == "4":
        return "Special"
    elif choice == "5":
        return "Consumables"
    elif choice == "6":
        return "Flee"
    elif choice == "":
        return "Attack"
    else:
        print("Invalid choice.")
        return None

def get_attack_by_name(attacks_data, attack_name):
    # Search for the attack by name in the attacks list
    for attack in attacks_data['attacks']:
        if attack['name'] == attack_name:
            return attack
    raise KeyError(f"Attack '{attack_name}' not found in Attacks.json")

def choose_attack(attacks, attack_type):
    print(f"\n{attack_type.capitalize()}s:")
    for idx, attack in enumerate(attacks, start=1):
        print(f"{idx}. {attack}")
    print(f"{len(attacks) + 1}. Go Back")
    
    while True:
        chosen_index = input(f"Choose an Option: ").strip()
        if chosen_index == "":
            return attacks[0]  # Default to the first option if no input is given
        elif chosen_index.isdigit() and 1 <= int(chosen_index) <= len(attacks):
            return attacks[int(chosen_index) - 1]  # Return the chosen attack
        elif chosen_index == str(len(attacks) + 1) or chosen_index.lower() == "back":
            return None  # Indicate that the player wants to go back
        else:
            print("Invalid choice. Please choose a valid option.")

def handle_targeting(player, enemies, attack_data, combat_log):
    # Handle targeting based on the attack's targeting type
    if attack_data['targeting'] == "Single Opponent":
        alive_enemies = [enemy for enemy in enemies if enemy['alive']]  # Filter only alive enemies

        # Automatically select the only target if there's only one
        if len(alive_enemies) == 1:
            target = alive_enemies[0]
            result = execute_attack(player, target, attack_data['name'], attack_data, enemies)
            action = True
        else:
            print("\nSelect a target:")
            for i, enemy in enumerate(alive_enemies, start=1):  # Start numbering from 1
                print(f"{i}. {enemy['name']} (Health: {enemy['combat_stats']['health']})")
            print(f"{len(alive_enemies) + 1}. Go Back")  # Option to go back

            while True:
                target_choice = input("Choose an Option: ").strip()
                if target_choice == "":
                    target_choice = "1"  # Default to the first target if no input is given
                if target_choice.isdigit() and 1 <= int(target_choice) <= len(alive_enemies):
                    target_index = int(target_choice) - 1
                    target = alive_enemies[target_index]  # Select the target from the filtered alive enemies list
                    result = execute_attack(player, target, attack_data['name'], attack_data, enemies)
                    action = True
                    break
                elif target_choice.lower() == "back" or target_choice == str(len(alive_enemies) + 1):
                    # Return to the main action menu, but don't return None
                    result = None
                    action = False
                    break
                else:
                    print("Invalid choice. Please choose a valid target.")

    elif attack_data['targeting'] == "All Opponents":
        # Check if it's a special move, handle all opponents at once
        if attack_data["type"] == "Special":
            alive_enemies = [enemy for enemy in enemies if enemy['alive']]  # Filter only alive enemies
            result = execute_attack(player, alive_enemies, attack_data['name'], attack_data, enemies)  # Pass all enemies
        else:
            # Loop through and apply normal attacks to each enemy
            result = ""
            for enemy in enemies:
                if enemy['alive']:  # Only attack alive enemies
                    result += execute_attack(player, enemy, attack_data['name'], attack_data, enemies) + "\n"
        action = True

    elif attack_data['targeting'] == "Single Ally":
        # Placeholder logic for ally targeting (no allies in this setup yet)
        print("This action targets a single ally. Placeholder action.")
        combat_log.append(f"{player['name']} used {attack_data['name']} on a single ally (placeholder).")
        result = None
        action = False

    elif attack_data['targeting'] == "All Allies":
        # Placeholder logic for all allies targeting (no allies in this setup yet)
        print("This action targets all allies. Placeholder action.")
        combat_log.append(f"{player['name']} used {attack_data['name']} on all allies (placeholder).")
        result = None
        action = False
    
    elif attack_data['targeting'] == "Self":
        # Automatically target self for self-targeting actions
        result = execute_attack(player, player, attack_data['name'], attack_data, enemies)
        action = True

    # Append the result of the attack to the combat log if the result exists
    if result:
        combat_log.append(result)

    return action


def check_combat_status(player, enemies, combat_log):
    # Check if player is defeated
    if player["combat_stats"]["health"] <= 0:
        defeat_message = apply_text_formatting(f"{player['name']} has been defeated!{RESET}")
        clear_screen()
        for log_entry in combat_log:
            print(log_entry)
        print("\n")
        print(defeat_message)
        return True  # Combat is over
    
    # Check if all enemies are defeated
    if all(enemy["combat_stats"]["health"] <= 0 for enemy in enemies):
        victory_message = apply_text_formatting("All enemies have been defeated!{RESET}")
        clear_screen()
        for log_entry in combat_log:
            print(log_entry)
        print("\n")
        print(victory_message)
        return True  # Combat is over

    # Handle enemy deaths
    for enemy in enemies:
        if enemy['combat_stats']['health'] <= 0 and enemy['alive']:
            enemy['alive'] = False
            death_message = apply_text_formatting(f"{enemy['death_message']}{RESET}")  # Apply formatting
            combat_log.append(death_message)  # Display death message from enemies.json

    return False  # Combat is not over

def apply_combat_status_effect(character, effect_name, effect_type, duration, stacks=1):
    """General function to apply a status effect (buff or debuff) to a character.
    The actual effect logic will be processed during combat."""
    
    # Initialize the status effect data structure if it doesn't exist
    if 'status_effects' not in character:
        character['status_effects'] = {'buffs': {}, 'debuffs': {}}

    # Determine if this is a buff or a debuff
    effect_category = 'buffs' if effect_type == 'buff' else 'debuffs'

    # Initialize status effects category if not present
    if effect_category not in character['status_effects']:
        character['status_effects'][effect_category] = {}

    # Store or update the status effect
    if effect_name in character['status_effects'][effect_category]:
        # Update the existing effect: increase stacks if stackable, reset duration
        effect_data = character['status_effects'][effect_category][effect_name]
        effect_data['stacks'] = min(effect_data['stacks'] + stacks, effect_data['max_stacks'])
        effect_data['duration'] = max(effect_data['duration'], duration)  # Refresh duration if extendable
    else:
        # Add new effect with initial stacks and duration
        character['status_effects'][effect_category][effect_name] = {
            'effect_name': effect_name,
            'stacks': stacks,
            'max_stacks': stacks,  # This could be read from a JSON file if different max stacks are required
            'duration': duration
        }

    print(f"{effect_name} applied to {character['name']}. Stacks: {stacks}, Duration: {duration}")

def process_status_effects(character, is_player=False):
    # Buffs and debuffs are processed separately
    for category in ['buffs', 'debuffs']:
        for effect_name, effect_data in list(character['status_effects'][category].items()):
            # Retrieve the actual effect logic function and apply it
            effect_info = effect_info or load_json_data("./combat/Status_Effects.json")['Common'].get(effect_name)
            if effect_info:
                effect_func = getattr(status_effects_module, effect_info['Effect'])
                effect_func(character, effect_data['stacks'])  # Apply the effect with stacks

            # Decrease duration
            effect_data['duration'] -= 1
            if effect_data['duration'] <= 0:
                print(f"{effect_name} expired on {character['name']}.")
                del character['status_effects'][category][effect_name]


# Initialize enemy stats at the start of combat
def initialize_enemy(enemy):
    enemy['combat_stats'] = calculate_combat_stats(enemy, {})
    enemy['status_effects'] = {
        'buffs': {},
        'debuffs': {}
    }

def clean_up_player_after_combat(player):
    # Step 1: Remove "stats", "initial_stats", and "combat_stats" from the player
    if 'stats' in player:
        del player['stats']
    if 'initial_stats' in player:
        del player['initial_stats']
    if 'combat_stats' in player:
        del player['combat_stats']

    # Step 2: Load status effects from the Status_Effects.json
    try:
        with open('./combat/Status_Effects.json', 'r') as file:
            status_effects_data = json.load(file)
    except FileNotFoundError:
        print("Error: Status_Effects.json not found!")
        return

    # Step 3: Remove non-persistent buffs and debuffs from the player's status effects
    buffs = status_effects_data.get("Buffs", {})
    debuffs = status_effects_data.get("Debuffs", {})

    # Remove non-persistent buffs
    player_buffs = player['status_effects'].get('buffs', {})
    for buff_name in list(player_buffs.keys()):
        buff_info = buffs.get(buff_name)
        if buff_info and not buff_info.get("Persistent", False):
            del player_buffs[buff_name]  # Remove the buff from player

    # Remove non-persistent debuffs
    player_debuffs = player['status_effects'].get('debuffs', {})
    for debuff_name in list(player_debuffs.keys()):
        debuff_info = debuffs.get(debuff_name)
        if debuff_info and not debuff_info.get("Persistent", False):
            del player_debuffs[debuff_name]  # Remove the debuff from player

    # Save updated player status
    save_player(player, f"./saves/{player['name']}-SaveData.json")


# Combat loop
def combat_loop(player, enemy_names):
    attacks_data = load_json_data("./combat/Attacks.json") # Load attacks from Attacks.json
    combat_log = []  # Store the combat log
    turn_counter = 1  # Initialize the turn counter
    
    # Calculate player's combat stats
    equipment_data = load_json_data("./items/Equipment.json")  # Load equipment data from Equipment.json
    player['stats'] = calculate_combat_stats(player, equipment_data)
    enemies = load_enemy_data(enemy_names) 
    
    for enemy in enemies:
        enemy['stats'] = calculate_combat_stats(enemy, {})  # Assuming no equipment for enemies
        enemy['alive'] = True  # Add alive status for tracking
        enemy['status_effects'] = {
            'buffs': {},
            'debuffs': {}
        }
    
    # Get the player's primary and secondary class abilities
    primary_class_attacks = player['classes'][player['primary_class']]['attacks']
    secondary_class_attacks = player['classes'][player['secondary_class']]['attacks']
    
    # Combine the attacks list, ensuring no duplicates
    all_attacks = list(set(player['attacks'] + primary_class_attacks + secondary_class_attacks))

    # Calculate initial stats for player and enemies and store them
    player_initial_stats = calculate_combat_stats(player, load_json_data("./items/Equipment.json"))
    player['initial_stats'] = player_initial_stats.copy()  # Store player's initial stats

    for enemy in enemies:
        enemy_initial_stats = calculate_combat_stats(enemy, {})
        enemy['initial_stats'] = enemy_initial_stats.copy()  # Store enemy's initial stats

    # Create a new set of combat stats based on the initial stats
    player['combat_stats'] = player['initial_stats'].copy()
    for enemy in enemies:
        enemy['combat_stats'] = enemy['initial_stats'].copy()

    # Display combat start messages before the combat loop begins
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen at the start of combat
    display_combat_start(player, enemies)  # Show the initial combat status with entry messages
    input("\nPress Enter to start the battle...")  # Pause before the battle starts
    
    # Main combat loop
    while True:
        # Clear screen for readability
        os.system('cls' if os.name == 'nt' else 'clear')


        
        # Show combat log
        for log_entry in combat_log:
            print(log_entry)

        # Apply status effects to the combat stats
        process_status_effects(player)
        for enemy in enemies:
            process_status_effects(enemy)

        # Display combat status
        display_combat_status(player, enemies)  # Constantly display updated player and enemy stats
        save_player(player, f"./saves/{player['name']}-SaveData.json")
        
        # Player turn: Display action and get input
        action = None
        while not action:
            action = player_action_menu(player, attacks_data)
        
        # Clear screen after the choice is made to refresh the stats and menu
        os.system('cls' if os.name == 'nt' else 'clear')

        # Show combat log again after clearing the screen
        for log_entry in combat_log:
            print(log_entry)
        
        if action == "Flee":
            if attempt_flee(player, enemies):
                clean_up_player_after_combat(player)
                break  # Player successfully fled, end combat
            elif action == "Consumables":
                consumable_message = apply_text_formatting(f"{player['name']} uses a consumable. Placeholder text for now.{RESET}")
                print(consumable_message)
                combat_log.append(consumable_message)
                time.sleep(1)  # Placeholder delay

        else:
            # Determine the attack type and attack data
            if action == "Attack":
                basic_attack = player["basic_attack"]
                attack_data = get_attack_by_name(attacks_data, basic_attack)
                action = handle_targeting(player, enemies, attack_data, combat_log)
                if action is False:
                    continue
            elif action == "Magic":
                magic_attacks = [attack for attack in all_attacks if get_attack_by_name(attacks_data, attack)["type"] == "Magical"]
                chosen_magic = choose_attack(magic_attacks, "magic")
                if chosen_magic is None:
                    continue 
                attack_data = get_attack_by_name(attacks_data, chosen_magic)
                action = handle_targeting(player, enemies, attack_data, combat_log)
                if action is False:
                    continue
            elif action == "Skills":
                physical_skills = [attack for attack in all_attacks if get_attack_by_name(attacks_data, attack)["type"] == "Physical"]
                chosen_skill = choose_attack(physical_skills, "skill")
                if chosen_skill is None:
                    continue 
                attack_data = get_attack_by_name(attacks_data, chosen_skill)
                action = handle_targeting(player, enemies, attack_data, combat_log)
                if action is False:
                    continue
            elif action == "Special":
                special_attacks = [attack for attack in all_attacks if get_attack_by_name(attacks_data, attack)["type"] == "Special"]
                chosen_special = choose_attack(special_attacks, "special")
                if chosen_special is None:
                    continue
                attack_data = get_attack_by_name(attacks_data, chosen_special)
                action = handle_targeting(player, enemies, attack_data, combat_log)
                if action is False:
                    continue
       
        if check_combat_status(player, enemies, combat_log):
            clean_up_player_after_combat(player)
            break

        # Companion's turn (placeholder)
        print("Your companion is preparing to act...")

        if check_combat_status(player, enemies, combat_log):
            clean_up_player_after_combat(player)
            break

        # Enemy turn
        for enemy in enemies:
            if not enemy['alive']:
                continue  # Skip actions for dead enemies
            if enemy["AI"]["type"] == "Basic":
                attack_choice = select_basic_ai_attack(enemy)
            elif enemy["AI"]["type"] == "Advanced":
                print(f"{enemy['name']} is using advanced AI.")
                # attack_choice = execute_advanced_ai(enemy, player)
            
            attack_data = get_attack_by_name(attacks_data, attack_choice)
            result = execute_attack(enemy, player, attack_choice, attack_data, enemies)
            combat_log.append(result)

        if check_combat_status(player, enemies, combat_log):
            clean_up_player_after_combat(player)
            break
        
        # Increment the turn counter after all phases have completed
        turn_counter += 1

