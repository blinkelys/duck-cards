# main.py
from entities import Player, Enemy
from setup import load_cards, setup_player, setup_enemy, create_deck
from gameplay import start_game, show_stats, player_turn, enemy_turn
import pyfiglet

# Initialize
player = Player()
enemy = Enemy()

# Trigger card loading and setup
cards = load_cards()

# Display game title
title = pyfiglet.figlet_format("Duck Cards")
print(title)

# Setup
setup_player(player)
setup_enemy(enemy)
create_deck(player, cards)
create_deck(enemy, cards)

# Start game
start_game(player, enemy)
show_stats(player, enemy)

# Turn-based loop
while player.health > 0 and enemy.health > 0:
    player_turn(player, enemy)
    if enemy.health <= 0:
        print(f"\n{enemy.name} has been defeated! You win!")
        break

    enemy_turn(enemy, player)
    if player.health <= 0:
        print(f"\n{player.name} has been defeated! Game Over.")
        break

    show_stats(player, enemy)

print("\nGame Ended.")