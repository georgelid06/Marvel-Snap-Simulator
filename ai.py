import random

class AIPlayer:
    def __init__(self, game, player_number):
        self.game = game
        self.player_number = player_number
        self.hand = []
        self.location_powers = [0, 0, 0]  
        self.energy = 0


    def choose_card_and_location(self, energy):
        playable_cards = [card for card in self.hand if card.energy_cost <= energy]  # Use energy instead of energy_cost
        if not playable_cards:
            return None, None

        chosen_card = random.choice(playable_cards)
        chosen_location_index = random.choice(range(len(self.game.locations)))
        return chosen_card, chosen_location_index
    
    def draw_starting_hand(self, all_cards):
        return random.sample(all_cards, 12)

    def draw_card(self, all_cards):
        new_card = random.choice(all_cards)
        if len(self.hand) < 7:
            self.hand.append(new_card)
