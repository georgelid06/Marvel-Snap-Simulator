from game import Game
from ai import AIPlayer
class Card:
    def __init__(self, name, energy_cost, power, ability_description, ability=None):
        self.name = name
        self.energy_cost = energy_cost
        self.power = power
        self.ability_description = ability_description
        self.ability = ability
        self.owner = None

    def __repr__(self):
        return f"{self.name} (Energy: {self.energy_cost}, Power: {self.power}, Ability: {self.ability_description})"


class Ability:
    def __init__(self, effect):
        self.effect = effect


def generate_all_cards():
    # Define the card abilities/effects here
    def hawkeye_effect(card):
         if card.game.current_turn == card.game.turn_played + 1:
            return 2
         else:
            return 0

    def medusa_effect(location_index):
        if location_index == 1:  # Middle location
            return 2
        return 0

    def punisher_effect(location, card):
        opposing_cards = len([c for c in location.cards if c.owner != card.owner])
        return opposing_cards

    def sentinel_effect(player):
        player.hand.append(sentinel_card)

    def star_lord_effect(location, card):
        opponent_played = any(c.owner != card.owner for c in location.cards_this_turn)
        if opponent_played:
            return 3
        return 0

    hawkeye_ability = Ability(hawkeye_effect)
    medusa_ability = Ability(medusa_effect)
    punisher_ability = Ability(punisher_effect)
    sentinel_ability = Ability(sentinel_effect)
    star_lord_ability = Ability(star_lord_effect)

    all_cards = [
        Card("Abomination", 5, 9, "No ability"),
        Card("Cyclops", 3, 4, "No ability"),
        Card("Hawkeye", 1, 1, "On Reveal: If you play a card here next turn, +2 Power.", hawkeye_ability),
        Card("Hulk", 6, 12, "No ability"),
        Card("Iron Man", 5, 0, "Ongoing: Your total Power is doubled at this Location."),
        Card("Medusa", 2, 2, "On Reveal: If this is at the middle Location, +2 Power.", medusa_ability),
        Card("Misty Knight", 1, 2, "No ability"),
        Card("The Punisher", 3, 2, "Ongoing: +1 Power for each opposing card at this Location.", punisher_ability),
        Card("Quicksilver", 1, 2, ""),  # Remove the "Starts in your opening hand" ability description
        Card("Sentinel", 2, 3, "On Reveal: Add another Sentinel to your hand.", sentinel_ability),
        Card("Shocker", 2, 3, "No ability"),
        Card("Star Lord", 2, 2, "On Reveal: If your opponent played a card here this turn, +3 Power.", star_lord_ability),
        Card("The Thing", 4, 6, "No ability"),
    ]

    # We need a reference to Quicksilver and Sentinel cards for their abilities
    sentinel_card = next(card for card in all_cards if card.name == "Sentinel")

    # Continue generating the cards here
    return all_cards