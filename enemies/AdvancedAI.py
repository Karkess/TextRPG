def select_advanced_ai_attack(enemy, user):
    # Example for Cloaker's advanced AI logic
    if enemy["name"] == "Cloaker":
        if user["stats"]["health"] > (user["stats"]["max_health"] / 2):
            return "Screech"
        else:
            return "Bite"
    # Add more advanced AI behaviors for other enemies as needed
