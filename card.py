from ai import AIPlayer
import random

class Card:
    def __init__(self, name, energy_cost, power, ability_description, ability=None):
        self.name = name
        self.energy_cost = energy_cost
        self.power = power
        self.base_power = power
        self.bonus_power = 0
        self.ongoing_power = 0
        self.location_power = 0
        self.ability_description = ability_description
        self.ability = ability
        self.owner = None
        self.turn_played = 0
        self.location = None
        self.location_effect_applied = False  # Add this flag
        self.hawkeye_effect_applied = False
        self.blue_marvel_effect_applied = False  # Add this flag

    def __repr__(self):
        return f"{self.name} (Energy: {self.energy_cost}, Power: {self.power}, Ability: {self.ability_description})"

class Ability:
    def __init__(self, effect, ability_type):
        self.effect = effect
        self.ability_type = ability_type

def generate_all_cards():
    # Define the card abilities/effects here
    def medusa_effect(card, game, card_owner, location_index):  # Add location_index parameter
        if card.location == 1:  # Middle location
            return 2
        return 0

    def punisher_effect(card, game, card_owner, location_index):
        location = game.locations[card.location]
        enemy_card_count = sum(1 for c in location.cards if c.owner != card_owner and c != card)  # Include the current card
        punisher_power = 1 * enemy_card_count
        card.ongoing_power = punisher_power

    def sentinel_effect(card, game, card_owner, location_index):
        if card_owner is not None:
            player = game.players[card.owner]            
            if sentinel_card is not None:
                new_sentinel = Card(sentinel_card.name, sentinel_card.energy_cost, sentinel_card.power, sentinel_card.ability_description, sentinel_card.ability)
                player.hand.append(new_sentinel)

    def star_lord_effect(card, game, card_owner, location_index):
        location = location_index
        opponent = 1 if card_owner == 0 else 0
        if any(c.owner == opponent and c.turn_played == game.current_turn for c in location.cards):
            return 3
        return 0
    
    def gamora_effect(card, game, card_owner, location_index):
        location = location_index
        opponent = 1 if card_owner == 0 else 0
        if any(c.owner == opponent and c.turn_played == game.current_turn for c in location.cards):
            return 5
        return 0
    
    def blue_marvel_effect(card, game, card_owner, location_index):
        for location in game.locations:
            friendly_cards = [c for c in location.cards if c.owner == card_owner and c != card]
            for c in friendly_cards:
                if not c.blue_marvel_effect_applied:
                    c.bonus_power += 1
                    c.blue_marvel_effect_applied = True
            card.blue_marvel_effect_applied = True
    
    def ant_man_effect(card, game, card_owner, location_index):
        location = game.locations[card.location]
        friendly_cards = [c for c in location.cards if c.owner == card_owner and c != card]
        if len(friendly_cards) >= 3:
            print("HEREHEREHERE")
            return 3
        return 0

    def colossus_effect(card, game, card_owner, location_index):
        # This effect is passive and does not modify power directly
        pass

    def ironheart_effect(card, game, card_owner, location_index):
        for location in game.locations:
            friendly_cards = [c for c in location.cards if c.owner == card_owner and c != card]
        if len(friendly_cards) >= 3:
            selected_cards = random.sample(friendly_cards, 3)
            for c in selected_cards:
                c.bonus_power += 2
        if 0 < len(friendly_cards) < 3:
            for c in friendly_cards:
                c.bonus_power += 2
        else:
            return


    medusa_ability = Ability(medusa_effect, "On Reveal")
    punisher_ability = Ability(punisher_effect, "Ongoing")
    sentinel_ability = Ability(sentinel_effect, "On Reveal")
    star_lord_ability = Ability(star_lord_effect, "On Reveal")
    gamora_ability = Ability(gamora_effect, "On Reveal")
    ant_man_ability = Ability(ant_man_effect, "Ongoing")
    colossus_ability = Ability(colossus_effect, "Ongoing")
    ironheart_ability = Ability(ironheart_effect, "On Reveal")
    blue_marvel_ability = Ability(blue_marvel_effect, "Ongoing")



    all_cards = [
        ##starter cards
        Card("Abomination", 5, 9, "No ability"),
        Card("Cyclops", 3, 4, "No ability"),
        Card("Hawkeye", 1, 1, "On Reveal: If you play a card here next turn, +2 Power."),
        Card("Hulk", 6, 12, "No ability"),
        Card("Iron Man", 5, 0, "Ongoing: Your total Power is doubled at this Location."),
        Card("Medusa", 2, 2, "On Reveal: If this is at the middle Location, +2 Power.", medusa_ability),
        Card("Misty Knight", 1, 2, "No ability"),
        Card("The Punisher", 3, 2, "Ongoing: +1 Power for each opposing card at this Location.", punisher_ability),
        Card("Quicksilver", 1, 2, ""),
        Card("Sentinel", 2, 3, "On Reveal: Add another Sentinel to your hand.", sentinel_ability),
        Card("Shocker", 2, 3, "No ability"),
        Card("Star Lord", 2, 2, "On Reveal: If your opponent played a card here this turn, +3 Power.", star_lord_ability),
        Card("The Thing", 4, 6, "No ability"),

        ##recruit season
        Card("Gamora", 5, 7, "On Reveal: If your opponent played a card here this turn, +5 Power", gamora_ability),
        Card("Ant-Man", 1, 1, "Ongoing: If you have three other cards here, +3 Power.", ant_man_ability),
        Card("Colossus", 2, 3, "Ongoing: Can’t be destroyed, moved, or have its Power reduced.", colossus_ability),
        Card("Ironheart", 3, 0, "On Reveal: Give 3 other friendly cards +2 Power.", ironheart_ability),
        Card("Blue Marvel", 5, 3, "Ongoing: Your other cards have +1 Power.", blue_marvel_ability),

    ]

    sentinel_card = next(card for card in all_cards if card.name == "Sentinel")

    return all_cards