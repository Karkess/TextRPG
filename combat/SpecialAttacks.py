import sys
import re
from combat.Status_Effects import *
import traceback
import random
import time
from utils import *

def handle_special_effect(user, targets, effect):
    try:
        # Replace placeholders in the effect string
        formatted_effect = effect.replace("{user}", "user").replace("{targets}", "targets")
        
        # Use pipe '|' as the delimiter for multiple function calls
        function_calls = re.split(r'\|\s*', formatted_effect)
        
        results = []
        for function_call in function_calls:
            # Match the function name and arguments more robustly using regex
            match = re.match(r'(\w+)\((.*)\)', function_call.strip())
            if match:
                function_name, args = match.groups()

                # Split the arguments string by commas and trim spaces
                args = [arg.strip() for arg in args.split(',')]

                # Resolve the arguments by checking if they refer to variables like 'user' or 'targets'
                resolved_args = []
                for arg in args:
                    # Check if the argument is 'user' or 'targets', then append the actual variables
                    if arg == "user":
                        resolved_args.append(user)
                    elif arg == "targets":
                        resolved_args.append(targets)
                    else:
                        # If it's not a placeholder, assume it's a literal like number or string
                        try:
                            resolved_args.append(eval(arg))  # Evaluate literals like numbers or strings
                        except Exception as e:
                            resolved_args.append(arg)

                # Dynamically call the function by name using getattr
                if hasattr(sys.modules[__name__], function_name):
                    effect_function = getattr(sys.modules[__name__], function_name)
                    result = effect_function(*resolved_args)
                    results.append(result)
                else:
                    return f"{function_name} is not implemented."
            else:
                return f"Invalid function call syntax: {function_call}"

        # Concatenate all results into a single string
        return '\n'.join(results)
    
    except Exception as e:
        traceback.print_exc()
        return f"{effect} could not be executed."

def cast_heal(user, target, amount):
    heal_message = heal(target, amount)
    return f"{user['name']} heals {target['name']}.\n{heal_message}"

def self_heal(user, amount):
    heal_message = heal(user, amount)
    return f"{heal_message}"

def apply_status_test_boosts(user, target, effect_name, effect_type, duration, stacks):
    apply_status_effect(target, effect_name, effect_type, duration, stacks)  # Assuming this function is implemented
    return f"{user['name']} applied {effect_name} to {target['name']}."

def vampiric_pact(user, targets):
    total_damage_dealt = 0
    results = []  # This will store only the final messages to return

    # Deal damage 10 times to each target
    for target in targets:
        clear_screen()
        total_target_damage = 0
        for _ in range(10):
            # Calculate random damage between 1% and 5% of remaining health
            remaining_health = target['combat_stats']['health']
            damage = int(remaining_health * random.uniform(0.01, 0.05))  # Integer for cleaner display

            # Subtract damage from target's health
            target['combat_stats']['health'] = max(0, target['combat_stats']['health'] - damage)

            # Add to total damage dealt to the target
            total_target_damage += damage

            # Generate the hit message with purple text (but don't store it in results)
            hit_message = format_text(
                f"{target['name']} takes {damage} damage as the darkness constricts them tighter.",
                color=MAGENTA
            )
            print(hit_message)

            # Wait for 0.5 seconds between hits
            time.sleep(0.5)

        total_damage_dealt += total_target_damage
        # Add message about total life drained in red
        drain_message = format_text(
            f"{target['name']} had {total_target_damage} life drained from them by beings existing as shadows.",
            color=RED
        )
        clear_screen()
        time.sleep(1.5)
        print(drain_message)
        time.sleep(3.5)
        clear_screen()
        time.sleep(1.5)
        results.append(drain_message)

    # Add a 1.5 second pause after all damage is dealt before healing message
    clear_screen()
    print('\n'.join(results))
    time.sleep(2.5)
    clear_screen()

    # Heal the user for the total damage dealt
    current_health = user['combat_stats']['health']
    max_health = user['stats']['health']

    # Calculate the new health after healing
    new_health = min(current_health + total_damage_dealt, max_health)
    user['combat_stats']['health'] = new_health

    # Generate the healing message in purple with the amount healed in green
    heal_message = apply_text_formatting(f"{MAGENTA}{user['name']} was healed {GREEN}{total_damage_dealt}{MAGENTA} through a vampiric pact with the darkness. \nTheir fate is sealed.{RESET}")

    print(f"\n\n{heal_message}")  # Print the healing message immediately
    time.sleep(4.5)
    results.append(heal_message)

    # Return the results as a concatenated string (no individual hit messages included)
    return '\n'.join(results)

