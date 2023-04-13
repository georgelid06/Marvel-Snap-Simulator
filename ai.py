import random

class AIPlayer:
    def __init__(self, game, player_number):
        self.game = game
        self.player_number = player_number + 1
        self.location_powers = [0, 0, 0]
        self.turn_energy_spent = 0
        self.energy = 1  # Add this line to initialize energy
        self.deck = self.draw_starting_hand(self.game.all_cards)
        self.hand = self.deck[:4]
        self.deck = self.deck[4:]

    def choose_card_and_location(self):  # Remove energy_pool argument
        playable_cards = [card for card in self.hand if card.energy_cost <= self.energy]  # Replace energy_pool with self.energy
        if not playable_cards:
            return None, None

        chosen_card = random.choice(playable_cards)
        chosen_location_index = random.choice(range(len(self.game.locations)))

        # Ensuring the location does not already have 4 cards from the player.
        while sum(1 for card in self.game.locations[chosen_location_index].cards if card.owner == self.player_number - 1) >= 4:
            chosen_location_index = random.choice(range(len(self.game.locations)))

        return chosen_card, chosen_location_index

    def draw_starting_hand(self, all_cards):
        starting_hand = random.sample(all_cards, 12)
        quicksilver_card = next((card for card in starting_hand if card.name == "Quicksilver"), None)
        if quicksilver_card:
            starting_hand.remove(quicksilver_card)
            starting_hand = [quicksilver_card] + starting_hand
        return starting_hand

    def draw_card(self, all_cards):
        new_card = random.choice(all_cards)
        if len(self.hand) < 7:
            self.hand.append(new_card)
