import random
from ai import AIPlayer

class Game:
    def __init__(self, all_cards, all_locations):
        self.all_cards = all_cards
        self.all_locations = all_locations
        self.players = [AIPlayer(self, 0), AIPlayer(self, 1)]  # Both players are AI-controlled now
        self.locations = self.generate_locations()
        self.current_turn = 1
        self.current_location = 0

    def play_cards(self, card, player_number, location_index):
        player = self.players[player_number - 1]
        location = self.locations[location_index]
        card.owner = player_number - 1
        card.location = location
        location.cards.append(card)  # Append the card object to the list, not the list itself
        if location.effect is not None:  # Check if the effect function is not None
            location.effect(card, player)  # Pass both the card and player objects
        if card in player.hand:  # Check if the card is in the player's hand
            player.hand.remove(card)

    def reveal_location(self):
        location = self.locations[self.current_location]

        for player in self.players: 
            if location.on_reveal_effect:
                location.on_reveal_effect(player)
        
        self.current_location += 1


    def generate_locations(self):
        return random.sample(self.all_locations, 3)

    def prepare_game(self):
        for player in self.players:
            player.hand = player.draw_starting_hand(self.all_cards)
        self.reveal_location()

    def end_of_turn(self):
        for location in self.locations:
            if location.end_of_turn_effect:
                location.end_of_turn_effect(location, self.current_turn)

        self.current_turn += 1

    def next_turn(self):
        if self.current_turn >= 6:
            return False

        for player in self.players:
            player.draw_card(self.all_cards)

        self.current_turn += 1

        if self.current_turn in [2, 3]:
            self.reveal_location()

        return True

    def reveal_location(self):
        self.current_location += 1

    def play_round(self):
        for player in self.players:
            energy = self.current_turn
            while energy > 0:
                card, location_index = player.choose_card_and_location(energy)
                if card is None or location_index is None:
                    break

                if len(self.locations[location_index].cards[player.player_number]) < 4:
                    energy_cost = card.energy_cost
                    self.play_cards(card, player.player_number, location_index)
                    energy -= energy_cost
                else:
                    break


    def determine_winner(self):
        player_powers = [0, 0]

        for cards_list in self.cards:
            for card in cards_list:
                power = card.power
                player_powers[card.owner] += power

        if player_powers[0] > player_powers[1]:
            return 0
        elif player_powers[1] > player_powers[0]:
            return 1
        else:
            return None

    def display_game_state(self):
        print("Current game state:")
        for i, location in enumerate(self.locations):
            print(f"  Location {i + 1}: {location.name}")
            print(f"    Player 1 Power: {location.calculate_total_power(0)}")
            print(f"    Player 2 Power: {location.calculate_total_power(1)}")
            print("    Cards:")
            print(f"    DEBUG: location.cards: {location.cards}")  # Add this line for debugging
            for card in location.cards:  # Use the original loop
                owner_text = f"Player {card.owner + 1}" if card.owner is not None else "No owner"
                print(f"      {card.name} (Power: {card.power}, Owner: {owner_text})")
        print("\nPlayer Hands:")
        for i, player in enumerate(self.players):
            print(f"  Player {i + 1} Hand:")
            for card in player.hand:
                print(f"    {card.name} (Power: {card.power})")
        print("\n")


    def play_game(self):
        self.prepare_game()
        while self.next_turn():
            self.play_round()
            self.end_of_turn()
            self.display_game_state()

        winner = self.determine_winner()
        if winner is not None:
            print(f"Player {winner + 1} wins!")
        else:
            print("It's a tie!")

        return winner
