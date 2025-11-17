# main.py
from entities import Player, Enemy
from setup import load_cards, setup_player, setup_enemy, create_deck
from gameplay import start_game, show_stats

# Initialize
player = Player()
enemy = Enemy()
cards = load_cards()

# Setup
setup_player(player)
setup_enemy(enemy)
create_deck(player, cards)

# Start game
start_game(player, enemy)
show_stats(player, enemy)
