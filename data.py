import json
import hashlib

def deck_hash(deck):
    deck_str = ''.join(sorted([card.name for card in deck], key=str.lower)) # Sort card names before hashing
    return hashlib.sha1(deck_str.encode()).hexdigest()

def update_deck_data(deck, result, total_power, decks_data):
    deck_id = deck_hash(deck)
    
    if deck_id in decks_data:
        decks_data[deck_id]["total_power"] += total_power
        decks_data[deck_id]["games_played"] += 1

        if result == "win":
            decks_data[deck_id]["wins"] += 1
        elif result == "loss":
            decks_data[deck_id]["losses"] += 1
    else:
        decks_data[deck_id] = {
            "cards": [card.name for card in deck],
            "wins": 1 if result == "win" else 0,
            "losses": 1 if result == "loss" else 0,
            "total_power": total_power,
            "games_played": 1
        }

def save_deck_data(decks_data, file_name):
    with open(file_name, 'w') as file:
        file.write("{\n")
        for idx, (key, value) in enumerate(decks_data.items()):
            file.write(f'"{key}": {json.dumps(value)}')
            if idx < len(decks_data) - 1:
                file.write(",\n")
            else:
                file.write("\n")
        file.write("}")

def load_deck_data(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, create it with an empty dictionary and return it
        with open(file_name, 'w') as file:
            json.dump({}, file)
        return {}

    
def get_average_power(deck_id, decks_data):
    total_power = decks_data[deck_id]["total_power"]
    games_played = decks_data[deck_id]["games_played"]
    return total_power / games_played

def winrate(decks_data):
    return decks_data["wins"] / (decks_data["wins"] + decks_data["losses"])

def printwinrate(decks_data):
    ranked_decks = sorted(decks_data.items(), key=lambda x: winrate(x[1]), reverse=True)

    for idx, (deck_id, deck_data) in enumerate(ranked_decks, 1):
        print(f"{idx}. Deck ID: {deck_id}")
        print(f"   Winrate: {winrate(deck_data) * 100:.2f}%")
        print(f"   Wins: {deck_data['wins']}")
        print(f"   Losses: {deck_data['losses']}")
        print(f"   Total Power: {deck_data['total_power']}")
        print(f"   Average Power: {deck_data['total_power'] / deck_data['games_played']}")
        print(f"   Games Played: {deck_data['games_played']}")
        print()
