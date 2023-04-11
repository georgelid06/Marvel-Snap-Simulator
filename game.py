import random
from ai import AIPlayer
from location import Location


class Game:
    def __init__(self, all_cards, all_locations):
        self.all_cards = all_cards
        self.all_locations = all_locations
        self.players = [AIPlayer(self, 0), AIPlayer(self, 1)]  # Both players are AI-controlled now
        self.locations = [Location("Location 1", False), Location("Location 2", False), Location("Location 3", False)]
        self.current_turn = 0
        self.current_location = 0
        self.energy = 1


    def play_cards(self, card, player_number, location_index):
        player = self.players[player_number - 1]
        location = self.locations[location_index]
        card.owner = player_number - 1
        card.location = location
        location.cards.append(card)  # Append the card object to the list, not the list itself

        if card.ability is not None:
            if card.ability_description.startswith("On Reveal:"):
                card.ability.effect(card)
            elif card.ability_description.startswith("Ongoing:"):
                card.ability.effect(location, card)


        if location.effect is not None:
            location.effect(card, player)

        if card in player.hand:
            player.hand.remove(card)

    def reveal_location(self):
        if self.current_location >= len(self.locations):
            return

        location = self.locations[self.current_location]

        for player in self.players:
            if location.on_reveal_effect:
                location.on_reveal_effect(player)

        self.current_location += 1

    def generate_locations(self):
        return random.sample(self.all_locations, 3)

    def prepare_game(self):
        self.locations = self.generate_locations()
        for player in self.players:
            player.hand = player.draw_starting_hand(self.all_cards)
        self.reveal_location()


    def end_of_turn(self):
        for location in self.locations:
            if location.end_of_turn_effect:
                location.end_of_turn_effect(location, self.current_turn)

        self.current_turn = 3 - self.current_turn

    def play_round(self):
        for player in self.players:
            player.draw_card(self.all_cards)
            energy = self.energy
            while energy > 0:
                card, location_index = player.choose_card_and_location(energy)
                if card is None or location_index is None:
                    break

                location = self.locations[location_index]
                if location.can_play_card is None or location.can_play_card(self.current_turn):
                    cards_in_location = sum(1 for card in location.cards if card.owner == player.player_number)
                    if cards_in_location < 4:
                        energy_cost = card.energy_cost
                        self.play_cards(card, player.player_number, location_index)
                        energy -= energy_cost
                    else:
                        break
                else:
                    break

    def determine_winner(self):
        player_card_counts = [0, 0]

        for location in self.locations:
            for card in location.cards:
                player_card_counts[card.owner] += 1

        if player_card_counts[0] > player_card_counts[1]:
            return 0
        elif player_card_counts[1] > player_card_counts[0]:
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

            for owner, player_cards in enumerate(location.cards):
                if isinstance(player_cards, list):  # Check if player_cards is a list
                    for card in player_cards:
                        owner_text = f"Player {owner + 1}"
                        print(f"{card.name} ({card.power}) - {owner_text}")
                else:  # If it's a single card, handle it directly
                    card = player_cards
                    owner_text = f"Player {owner + 1}"
                    print(f"{card.name} ({card.power}) - {owner_text}")

        print("\nPlayer Hands:")
        for i, player in enumerate(self.players):
            print(f"  Player {i + 1} Hand:")
            for card in player.hand:
                print(f"    {card.name} (Power: {card.power})")
        print("\n")

    def play_game(self):
        self.prepare_game()

        for turn in range(6):  # Loop through the 6 turns
            self.current_turn = turn + 1
            print(f"Turn {self.current_turn}")

            if turn < 3:
                self.reveal_location()

            self.play_round()
            self.end_of_turn()
            self.display_game_state()
            self.energy += 1

        winner = self.determine_winner()
        if winner is not None:
            print(f"Player {winner + 1} wins!")
        else:
            print("It's a tie!")

        return winner
