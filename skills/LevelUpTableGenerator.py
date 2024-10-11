import json

# Your functions for generating differences and total XP
def generate_level_up_differences(max_level, starting_difference, growth_rate):
    level_differences = {}
    current_difference = starting_difference

    for level in range(1, max_level + 1):
        level_differences[str(level)] = int(current_difference)

        # Every 10 levels, increase the difference by the growth rate
        if level % 10 == 0:
            current_difference *= growth_rate
        else:
            current_difference += starting_difference * 0.1  # Slight increase between levels

    return level_differences

def generate_total_xp_from_differences(level_differences):
    total_xp_table = {}
    cumulative_xp = 0

    for level, difference in level_differences.items():
        cumulative_xp += difference
        total_xp_table[level] = cumulative_xp

    return total_xp_table

# Define max level and starting parameters
max_level = 250
starting_difference = 100  # Starting XP difference for level 1
growth_rate = 2  # Double every 10 levels

# Generate level differences and total XP table
level_differences = generate_level_up_differences(max_level, starting_difference, growth_rate)
total_xp_table = generate_total_xp_from_differences(level_differences)

# Generate level-up table similar to the old one for JSON
def generate_level_up_table_json(total_xp_table):
    level_up_table = {}
    
    for level, total_xp in total_xp_table.items():
        level_up_table[str(level)] = total_xp
    
    return level_up_table

# Generate the level-up table JSON format
level_up_table_json = generate_level_up_table_json(total_xp_table)

# Save the level-up table to a JSON file
file_path = "./LevelUpTable2.json"
with open(file_path, "w") as file:
    json.dump(level_up_table_json, file, indent=4)

file_path
