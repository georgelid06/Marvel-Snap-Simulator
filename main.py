from card import generate_all_cards
from location import generate_all_locations
from game import Game

all_cards = generate_all_cards()
all_locations = generate_all_locations()
game = Game()
game.play_game()