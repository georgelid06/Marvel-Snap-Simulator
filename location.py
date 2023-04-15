import random

class Location:
    def __init__(self, name, effect_description, effect=None, on_reveal_effect=None, no_destroy=None, can_play_card=None, end_of_turn_effect=None):
        self.name = name
        self.effect_description = effect_description
        self.effect = effect
        self.on_reveal_effect = on_reveal_effect
        self.no_destroy = no_destroy
        self.can_play_card = can_play_card
        self.end_of_turn_effect = end_of_turn_effect
        self.cards = []
        self.cards_this_turn = []
        self.player1_played_card = False
        self.player2_played_card = False
        self.revealed = False

    def __str__(self):
        return f"{self.name} (Effect: {self.effect_description})"

    def __repr__(self):
        return f"{self.name} (Effect: {self.effect_description})"
    
    def calculate_total_power(self, player_number):
        total_power = sum(card.power for card in self.cards if card.owner == player_number)
        card_list = [(card.name, card.power) for card in self.cards if card.owner == player_number]
        card_list.clear
        return total_power

    def determine_winner(self):
        player_powers = [0, 0]

        for card in self.cards:
            power = card.power
            player_powers[card.owner] += power

        if player_powers[0] > player_powers[1]:
            return 0
        elif player_powers[1] > player_powers[0]:
            return 1
        else:
            return None
        
    def can_play_card_at_location(card, location, current_turn, player_energy):
        # Check if the card's energy cost is less than or equal to the player's energy
        if card.energy_cost > player_energy:
            return False

        # Check if the location has a specific rule that prevents the card from being played
        if location.name == "The Vault":
            if current_turn == 6:
                return False
        elif location.name == "The Big House":
            if card.energy_cost in [4, 5, 6]:
                return False

        # Check if the location has a general rule that prevents the card from being played
        if location.can_play_card and not location.can_play_card(location, current_turn):
            return False

        # Check if the location already has 4 cards from the player
        if sum(1 for c in location.cards if c.owner == card.owner) >= 4:
            return False

        return True

def generate_all_locations():

    # Define location effects here
    def xandar_effect(card, player, location):
        card.power += 1

    def tinkerers_workshop_effect(card, player, location):
        player.energy += 1

    def throne_room_effect(card, player, location_index):
        location = player.game.locations[location_index]

        # Find the card(s) with the highest power
        highest_power = max(location.cards, key=lambda c: c.base_power).base_power
        highest_power_cards = [c for c in location.cards if c.base_power == highest_power]

        # Double the power of the highest power card(s)
        for c in highest_power_cards:
            if c.base_power == highest_power:
                c.power = c.base_power * 2

        # Undo the doubling of the power for the other cards
        for c in location.cards:
            if c not in highest_power_cards and c.power > c.base_power:
                c.power = c.base_power

    def the_big_house_effect(card, player, location):
        if card.energy_cost in [4, 5, 6]:
            card.location.cards.remove(card)

    def negative_zone_effect(card, player, location):
        card.power -= 3
    def wakanda_no_destroy(location):
        pass  # Do not destroy cards in this location

    def the_vault_no_play_on_turn_six(location, current_turn):
        return current_turn != 6

    def stark_tower_end_of_turn_five(location_index, game, current_turn):
        if current_turn == 5:
            location = game.locations[location_index]
            for card in location.cards:
                card.power += 2

    def murderworld_end_of_turn_three(location_index, game, current_turn):
        if current_turn == 3:
            location = game.locations[location_index]
            location.cards.clear()


    # Generate all locations
    all_locations = [
        Location("Xandar", "Cards here have +1 Power.", xandar_effect),
        Location("Wakanda", "Cards here can't be destroyed.", no_destroy=wakanda_no_destroy),
        Location("Tinkerer's Workshop", "+1 Energy this turn.", effect=tinkerers_workshop_effect),
        Location("Throne Room", "Card(s) here with the highest Power have their Power doubled.", effect=throne_room_effect),
        Location("The Vault", "On turn 6, cards can't be played here.", can_play_card=the_vault_no_play_on_turn_six),
        Location("The Big House", "4, 5, and 6-Cost cards can't be played here.", effect=the_big_house_effect),
        Location("Stark Tower", "At the end of turn 5, give all cards here +2 Power.", end_of_turn_effect=stark_tower_end_of_turn_five),
        Location("Negative Zone", "Cards here have -3 Power.", effect=negative_zone_effect),
        Location("Murderworld", "At the end of turn 3, destroy all cards here.", end_of_turn_effect=murderworld_end_of_turn_three),
        # Add the remaining locations with their respective effects
        # ...
    ]
    return all_locations