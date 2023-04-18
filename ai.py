import random
from location import Location

class AIPlayer:
    def __init__(self, game, player_number, all_cards):
        self.game = game
        self.player_number = player_number + 1
        self.location_powers = [0, 0, 0]
        self.turn_energy_spent = 0
        self.energy = 1
        self.deck = self.draw_starting_deck(all_cards)
        self.hand = self.draw_starting_hand(self.deck)
        self.played_cards=[]

    def choose_card_and_location(self):
        valid_plays = []
        for card_index, card in enumerate(self.hand):
            if card.energy_cost <= self.energy:
                for location_index, location in enumerate(self.game.locations):
                    if Location.can_play_card_at_location(card, location, self.game.current_turn, self.energy):
                        valid_plays.append((card_index, location_index))

        if valid_plays:
            chosen_card_index, chosen_location_index = random.choice(valid_plays)
            return [chosen_card_index], [chosen_location_index]
        else:
            return None, None

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