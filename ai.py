import random

class AIPlayer:
    def __init__(self, game, player_number, all_cards):
        self.game = game
        self.player_number = player_number + 1
        self.location_powers = [0, 0, 0]
        self.turn_energy_spent = 0
        self.energy = 1  # Add this line to initialize energy
        self.deck = self.draw_starting_deck(all_cards)
        self.hand = self.draw_starting_hand(self.deck)
        

    def choose_card_and_location(self):
        playable_cards_indices = [i for i, card in enumerate(self.hand) if card.energy_cost <= self.energy]
        playable_cards = [card for card in self.hand if card.energy_cost <= self.energy]
        if not playable_cards_indices:
            return None, None

        chosen_card_index = random.choice(playable_cards_indices)
        chosen_location_index = random.choice(range(len(self.game.locations)))

        # Ensuring the location does not already have 4 cards from the player.
        while sum(1 for card in self.game.locations[chosen_location_index].cards if card.owner == self.player_number - 1) >= 4:
            chosen_location_index = random.choice(range(len(self.game.locations)))
            chosen_card_index = random.choice(playable_cards_indices)

        return chosen_card_index, chosen_location_index

    def draw_starting_deck(self, all_cards):
        deck = random.sample(all_cards, 12)
        return deck

    def draw_starting_hand(self, deck):
        quicksilver_card = next((card for card in deck if card.name == "Quicksilver"), None)
        
        if quicksilver_card:
            deck.remove(quicksilver_card)  # Remove Quicksilver from the deck
            hand = random.sample(deck, 3)  # Draw only 3 cards
            for card in hand:  # Add this loop to remove the 3 cards from the deck
                deck.remove(card)
            hand.append(quicksilver_card)  # Add Quicksilver to the hand
        else:
            hand = random.sample(deck, 4)  # Draw 4 cards
            for card in hand:
                deck.remove(card)  # Remove drawn cards from the deck
                
        return hand



    def draw_card(self):
        if not self.deck:
            return
        new_card = random.choice(self.deck)
        if len(self.hand) < 7:
            self.hand.append(new_card)
            self.deck.remove(new_card)
