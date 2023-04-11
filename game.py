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
        location = self.locations[location_index]
        location.add_card(card, player_number)
        card.location = location

        # Apply the location's effect on the card
        if location.effect:
            location.effect(card)

    def generate_locations(self):
        return random.sample(self.all_locations, 3)

    def prepare_game(self):
        for player in self.players:
            player.hand = player.draw_starting_hand(self.all_cards)

        self.reveal_location()

    def end_of_turn(self):
        for location in self.locations:
            if location.end_of_turn_effect:
                location.end_of_turn_effect(self.current_turn)

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
        location_wins = [0, 0]

        for location in self.locations:
            winner = location.determine_winner()
            if winner is not None:
                location_wins[winner] += 1

        if location_wins[0] > location_wins[1]:
            return 0
        elif location_wins[1] > location_wins[0]:
            return 1
        else:
            return None

    def display_game_state(self):
        print(f"Turn: {self.turn}")
        print("Locations:")
        for i, location in enumerate(self.locations):
            print(f"  Location {i + 1}: {location.name} (Effect: {location.effect})")
            print(f"    Player 1 Power: {self.players[0].location_powers[i]}")
            print(f"    Player 2 Power: {self.players[1].location_powers[i]}")
            print("    Cards:")
            for card in location.cards:
                print(f"      {card.name} (Power: {card.power}, Owner: Player {card.owner + 1})")
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
