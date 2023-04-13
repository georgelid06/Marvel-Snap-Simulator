import random
from ai import AIPlayer
from card import Card, generate_all_cards
from location import Location, generate_all_locations

class Game:
    def __init__(self):
        self.current_turn = 1
        self.all_cards = generate_all_cards()
        self.all_locations = generate_all_locations()
        self.players = [AIPlayer(self, 0), AIPlayer(self, 1)]
        self.locations = [Location("Location 1", []), Location("Location 2", []), Location("Location 3", [])]
        self.current_turn = 0
        self.current_location = 0
        self.cards_played_by_turn = {0: {}, 1: {}}



    def play_cards(self, card, player_number, location_index):
        player = self.players[player_number - 1]
        location = self.locations[location_index]

        # Ensuring the location does not already have 4 cards from the player.
        if sum(1 for card in location.cards if card.owner == player_number - 1) >= 4:
            print(f"Player {player_number} cannot play {card.name} at this location. It already has 4 cards from the player.")
            return

        if card.energy_cost <= player.energy:
            card.owner = player_number - 1
            card.location = location
            location.cards.append(card)
            location.cards_this_turn.append(card)
            player.hand.remove(card)

            if card.ability is not None:
                card.ability.effect(card, self, location)

            if location.effect is not None:
                location.effect(card, player)

            # Consume the card's energy cost from the player's energy pool
            player.energy -= card.energy_cost

            # Update the player's turn_energy_spent
            player.turn_energy_spent += card.energy_cost

            # Add the played card to the cards_played list for the player
            if self.current_turn not in self.cards_played_by_turn[player_number - 1]:
                self.cards_played_by_turn[player_number - 1][self.current_turn] = []

            self.cards_played_by_turn[player_number - 1][self.current_turn].append(card)
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
        for player in self.players:
            player.hand = player.draw_starting_hand(self.all_cards)
        self.reveal_location()

    def end_of_turn(self):
        # Increase energy for each player
        for i in range(2):
            self.cards_played_by_turn[i][self.current_turn] = []    # Reset the cards_played list for each player

        for player in self.players:
            player.energy += 1

    def play_turn(self):
        self.players[0].turn_energy_spent = 0
        self.players[1].turn_energy_spent = 0

        for player in self.players:
            card, location_index = player.choose_card_and_location()
            if card is not None and location_index is not None:
                self.play_cards(card, player.player_number, location_index)
                # Draw a new card
                player.draw_card(self.all_cards)

            # Reset energy for the next player
            player.energy = self.current_turn

        self.current_turn += 1
        self.end_of_turn()


    def display_game_state(self):
        print("Current game state:")
        for idx, location in enumerate(self.locations, 1):
            print(f"  Location {idx}: {location.name}")
            print(f"    Player 1 Power: {location.calculate_total_power(0)}")
            print(f"    Player 2 Power: {location.calculate_total_power(1)}")
            print("    Cards:")
            for card in location.cards:
                print(f"{card.name} ({card.power}) - Player {card.owner + 1}")

        print("\nPlayer Hands and Cards Played:")
        for player_number, player in enumerate(self.players, 1):
            print(f"  Player {player_number} Hand:")
            for card in player.hand:
                print(f"    {card.name} (Power: {card.power})")
            print(f"  Player {player_number} Energy Spent: {player.turn_energy_spent}")
            print(f"  Player {player_number} Cards Played on Turn {self.current_turn}:")
            if self.current_turn in self.cards_played_by_turn[player_number - 1]:
                for card in self.cards_played_by_turn[player_number - 1][self.current_turn]:
                    print(f"    {card.name} (Power: {card.power})")
            else:
                print("    No cards played")
            print("")


    def determine_winner(self):
        player1_score = sum(location.calculate_total_power(0) for location in self.locations)
        player2_score = sum(location.calculate_total_power(1) for location in self.locations)

        if player1_score > player2_score:
            return 0
        elif player1_score < player2_score:
            return 1
        else:
            return None


    def play_game(self):
        self.prepare_game()

        for turn in range(6):  # Loop through the 6 turns
            self.current_turn = turn + 1
            print(f"Turn {self.current_turn}")

            if turn < 3:
                self.reveal_location()

            self.play_turn()
            self.end_of_turn()
            self.display_game_state()

        winner = self.determine_winner()
        if winner is not None:
            print(f"Player {winner + 1} wins!")
        else:
            print("It's a tie!")

        return winner