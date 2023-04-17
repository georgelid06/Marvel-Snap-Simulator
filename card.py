from ai import AIPlayer

class Card:
    def __init__(self, name, energy_cost, power, ability_description, ability=None):
        self.name = name
        self.energy_cost = energy_cost
        self.power = power
        self.base_power = power
        self.ability_description = ability_description
        self.ability = ability
        self.owner = None
        self.turn_played = 0
        self.location = None
        self.location_effect_applied = False  # Add this flag
        self.hawkeye_effect_applied = False  # Add this flag for Hawkeye cards only

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
        bonus_power = 1 * enemy_card_count
        card.power = card.base_power + bonus_power

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

    medusa_ability = Ability(medusa_effect, "On Reveal")
    punisher_ability = Ability(punisher_effect, "Ongoing")
    sentinel_ability = Ability(sentinel_effect, "On Reveal")
    star_lord_ability = Ability(star_lord_effect, "On Reveal")


    all_cards = [
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
    ]

    sentinel_card = next(card for card in all_cards if card.name == "Sentinel")

    return all_cards