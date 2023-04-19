import json

def deck_hash(deck):
    deck_str = ''.join(sorted([card.name for card in deck]))
    return hash(deck_str)

decks_data = {}

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
        json.dump(decks_data, file)

def load_deck_data(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)
    
def get_average_power(deck_id, decks_data):
    total_power = decks_data[deck_id]["total_power"]
    games_played = decks_data[deck_id]["games_played"]
    return total_power / games_played

