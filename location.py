import random

class Location:
    def __init__(self, name, effect_description, effect=None, no_destroy=None, can_play_card=None, end_of_turn_effect=None):
        self.name = name
        self.effect_description = effect_description
        self.effect = effect
        self.no_destroy = no_destroy
        self.can_play_card = can_play_card
        self.end_of_turn_effect = end_of_turn_effect
        self.cards = [[], []] 

    def add_card(self, card, player_number):
        self.cards[player_number].append(card)  # Update this method to work with the new structure

    def __repr__(self):
        return f"{self.name} (Effect: {self.effect_description})"

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
def generate_all_locations():

    # Define location effects here
    def xandar_effect(card):
        card.power += 1

    def wakanda_effect(card):
        pass  # Cards here can't be destroyed, implement this in the game logic

    def tinkerers_workshop_effect(card):
        card.owner.energy += 1

    def throne_room_effect(card):
        location = card.location
        max_power = max(c.power for c in location.cards)
        if card.power == max_power:
            card.power *= 2

    def the_vault_effect(card):
        pass  # On turn 6, cards can't be played here, implement this in the game logic

    def the_big_house_effect(card):
        if card.cost in [4, 5, 6]:
            card.location.cards.remove(card)

    def stark_tower_effect(card):
        pass  # At the end of turn 5, give all cards here +2 Power, implement this in the game logic

    def negative_zone_effect(card):
        card.power -= 3

    def murderworld_effect(card):
        pass  # At the end of turn 3, destroy all cards here, implement this in the game logic


    # Add these methods to the Location class to handle the specific effects
    def wakanda_no_destroy(self):
        pass  # Do not destroy cards in this location

    def the_vault_no_play_on_turn_six(self, current_turn):
        return current_turn != 6  # Return False if the current turn is 6

    def stark_tower_end_of_turn_five(self, current_turn):
        if current_turn == 5:
            for card in self.cards:
                card.power += 2

    def murderworld_end_of_turn_three(self, current_turn):
        if current_turn == 3:
            self.cards.clear()

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