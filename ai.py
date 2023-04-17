import random
from location import Location

class AIPlayer:
    def __init__(self, game, player_number, all_cards):
        self.game = game
        self.player_number = player_number + 1
        self.location_powers = [0, 0, 0]
        self.turn_energy_spent = 0
        self.energy = 1  # Add this line to initialize energy
        self.deck = self.draw_starting_deck(all_cards)
        self.hand = self.draw_starting_hand(self.deck)

    def calculate_hawkeye_effect(self, card, location, turn):
        hawkeye_cards = [c for c in location.cards if c.name == "Hawkeye" and c.turn_played == turn - 1 and not c.hawkeye_effect_applied and c.location == location.location_number]
        if hawkeye_cards:
            for hawkeye_card in hawkeye_cards:
                if hawkeye_card.owner == card.owner:
                    return 2
        return 0

    def evaluate_card_location_score(self, card, location, location_index):
        if location is None:
            return 0

        score = card.power

        # Consider the Hawkeye effect when evaluating the score
        hawkeye_power_bonus = self.calculate_hawkeye_effect(card, location, self.game.current_turn)
        score += hawkeye_power_bonus

        # Consider other card abilities that affect power
        if card.ability is not None:
            if card.ability.ability_type == "On Play" or card.ability.ability_type == "On Reveal":
                power_bonus = card.ability.effect(card, self.game, card.owner, location_index)
                if power_bonus is not None and power_bonus > 0:
                    score += power_bonus

        # Calculate the opponent's total power at the location
        opponent_total_power = location.calculate_total_power(1 - self.player_number)

        if opponent_total_power > 0:
            score += (score - opponent_total_power) / opponent_total_power

        return score


    def choose_card_and_location(self):
        def evaluate_combinations(remaining_energy, current_cards, current_locations, current_score, card_index):
            if card_index >= len(self.hand):
                return current_cards, current_locations, current_score

            card = self.hand[card_index]
            card.owner = self.player_number  # Add this line to assign the card owner before evaluation

            # Without the current card
            best_cards, best_locations, best_score = evaluate_combinations(remaining_energy, current_cards, current_locations, current_score, card_index + 1)

            # With the current card (if there's enough energy)
            if card.energy_cost <= remaining_energy:
                for location_index, location in enumerate(self.game.locations):
                    score = self.evaluate_card_location_score(card, location, location_index)
                    new_total_score = current_score + score
                    new_cards, new_locations, new_score = evaluate_combinations(remaining_energy - card.energy_cost, current_cards + [card_index], current_locations + [location_index], new_total_score, card_index + 1)

                    if new_score > best_score:
                        best_score = new_score
                        best_cards = new_cards
                        best_locations = new_locations

            return best_cards, best_locations, best_score

        best_card_indices, best_location_indices, _ = evaluate_combinations(self.energy, [], [], 0, 0)

        if best_card_indices and best_location_indices:
            return best_card_indices, best_location_indices
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
