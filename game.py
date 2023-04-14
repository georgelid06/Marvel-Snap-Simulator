import random
import copy
from card import Card, generate_all_cards
from location import Location, generate_all_locations
from ai import AIPlayer


class Game:
    def __init__(self):
        self.current_turn = 1
        self.all_cards = generate_all_cards()
        self.all_locations = generate_all_locations()
        self.players = [AIPlayer(self, 0, self.all_cards.copy()), AIPlayer(self, 1, self.all_cards.copy())]
        self.locations = [Location("Location 1", []), Location("Location 2", []), Location("Location 3", [])]
        self.current_turn = 0
        self.current_location = 0
        self.prepare_game()

    def play_cards(self, card_index, player_number, location_index):
        player = self.players[player_number - 1]
        card = player.hand[card_index]  # Get the card from the hand using the index
        location = self.locations[location_index]

        # Ensuring the location does not already have 4 cards from the player.
        if sum(1 for card in location.cards if card.owner == player_number - 1) >= 4:
            print(f"Player {player_number} cannot play {card.name} at this location. It already has 4 cards from the player.")
            return

        if card.energy_cost <= player.energy:
            card_copy = copy.deepcopy(card)  # Make a copy of the card
            card_copy.owner = player_number - 1
            card_copy.location = location_index
            location.cards.append(card_copy)
            card.location = location_index  # Set the location attribute

            location.cards_this_turn.append(card_copy)  # Add this line
            player.hand.remove(card)

            if card_copy.ability is not None:
                card_copy.ability.effect(card_copy, self, card_copy.owner)  # Updated this line

            if location.effect is not None:
                location.effect(card_copy, player, location_index)  # Updated this line

            # Consume the card's energy cost from the player's energy pool
            player.energy -= card.energy_cost

            # Update the player's turn_energy_spent
            player.turn_energy_spent += card.energy_cost

            #print("CARD PLAYED BY PLAYER:", card_copy.owner, "CARD =", card_copy)
        else:
            print(f"Player {player_number} cannot play {card.name} yet. It costs more energy than the current turn.")

    def reveal_location(self):
        if self.current_location >= len(self.locations):
            return

        location = self.locations[self.current_location]
        location.revealed = True

        self.current_location += 1

    def generate_locations(self):
        return random.sample(self.all_locations, 3)

    def prepare_game(self):
        self.locations = self.generate_locations()
        for _ in range(3):
            self.reveal_location()

    def end_of_turn(self):        
        # Reset energy for each player according to the current turn
        for player in self.players:
            player.energy = self.current_turn + 1
            player.turn_energy_spent = 0

        # Reset the cards_this_turn list for each location
        for location in self.locations:
            location.cards_this_turn = []

        for player in self.players:
            player.draw_card()


    def play_turn(self):
        for player_number, player in enumerate(self.players, 1):
            player.played_cards = []
            player.played_card_locations = []
            while True:
                chosen_card_index, location_index = player.choose_card_and_location()
                if chosen_card_index is not None and location_index is not None:
                    card = player.hand[chosen_card_index]
                    if card.energy_cost <= player.energy:
                        self.play_cards(chosen_card_index, player_number, location_index)
                        player.played_cards.append(card)
                        player.played_card_locations.append(location_index)
                    else:
                        print(f"Player {player_number} cannot play {card.name} yet. It costs more energy than the current turn.")
                        break
                else:
                    break

        # Determine the order in which players reveal cards
        player1_wins = 0
        player2_wins = 0
        for location in self.locations:
            if location.calculate_total_power(0) > location.calculate_total_power(1):
                player1_wins += 1
            elif location.calculate_total_power(0) < location.calculate_total_power(1):
                player2_wins += 1

        if player1_wins > player2_wins:
            reveal_order = [1, 2]
        elif player1_wins < player2_wins:
            reveal_order = [2, 1]
        else:
            player1_total_power = sum(location.calculate_total_power(0) for location in self.locations)
            player2_total_power = sum(location.calculate_total_power(1) for location in self.locations)
            if player1_total_power >= player2_total_power:
                reveal_order = [1, 2]
            else:
                reveal_order = [2, 1]

        # Reveal cards and apply card and location effects in the determined order
        for player_number in reveal_order:
            self.reveal_cards(player_number)

    def display_game_state(self):
            print("Turn", self.current_turn)
            print("\nCards at each location:")
            print("Player 1 (above) / Player 2 (below)")

            player1_cards_by_location = []
            player2_cards_by_location = []

            for location in self.locations:
                player1_cards = [f"{card.name} ({card.power})" if card.owner == 0 else "" for card in location.cards]
                player2_cards = [f"{card.name} ({card.power})" if card.owner == 1 else "" for card in location.cards]

                max_cards = max(len(player1_cards), len(player2_cards))
                player1_cards += [''] * (max_cards - len(player1_cards))
                player2_cards += [''] * (max_cards - len(player2_cards))

                player1_cards_by_location.append(player1_cards)
                player2_cards_by_location.append(player2_cards)

            max_rows = max(len(cards) for cards in player1_cards_by_location + player2_cards_by_location)

            for row in range(max_rows):
                for player1_cards in player1_cards_by_location:
                    print("{:^20}".format(player1_cards[row] if row < len(player1_cards) else ""), end=" ")
                print()

            for location in self.locations:
                print("{:^20}".format(location.name), end=" ")
            print()

            for row in range(max_rows):
                for player2_cards in player2_cards_by_location:
                    print("{:^20}".format(player2_cards[row] if row < len(player2_cards) else ""), end=" ")
                print()

            # Display decks and hands of both players
            print("\nPlayer 1 deck and hand:")
            print("Deck:", [card.name for card in self.players[0].deck])
            print("Hand:", [f"{card.name} ({card.power})" for card in self.players[0].hand])
            print("\n")
            print("Player 2 deck and hand:")
            print("Deck:", [card.name for card in self.players[1].deck])
            print("Hand:", [f"{card.name} ({card.power})" for card in self.players[1].hand])
            print("\n")

    def reveal_cards(self, player_number):
        player = self.players[player_number - 1]
        for card in player.played_cards:
            location = self.locations[card.location]  # Use the location attribute
            if card.ability is not None:
                card.ability.effect(card, self, player_number - 1)  # Updated this line


    def determine_winner(self):
        player1_score = sum(location.calculate_total_power(0) for location in self.locations)
        player2_score = sum(location.calculate_total_power(1) for location in self.locations)
        print("Player 1 had a total power of:", player1_score)
        print("Player 2 had a total power of:", player2_score)

        if player1_score > player2_score:
            return 0
        elif player1_score < player2_score:
            return 1
        else:
            return None


    def play_game(self):
        for turn in range(6):  # Loop through the 6 turns
            self.current_turn = turn + 1
            print(f"Turn {self.current_turn}")
            self.play_turn()
            self.display_game_state()
            self.end_of_turn()
        self.determine_winner()
