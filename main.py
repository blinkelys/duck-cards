# main.py
import pyfiglet
from entities import Player, Enemy
from setup import load_cards, setup_player, setup_enemy, create_deck
from gameplay import start_game, show_stats, player_turn, enemy_turn


def initialize_game():
    """Initialize and return player, enemy, and card data."""
    player = Player()
    enemy = Enemy()
    cards = load_cards()

    return player, enemy, cards


def setup_game(player, enemy, cards):
    """Setup player, enemy, and assign decks."""
    setup_player(player)
    setup_enemy(enemy)

    create_deck(player, cards)
    create_deck(enemy, cards)


def display_title():
    """Render and print game title."""
    title = pyfiglet.figlet_format("Duck Cards")
    print(title)


def main_loop(player, enemy):
    """Main turn-based game loop."""
    start_game(player, enemy)
    show_stats(player, enemy)

    while player.health > 0 and enemy.health > 0:
        # Player turn
        player_turn(player, enemy)
        if enemy.health <= 0:
            print(f"\n{enemy.name} has been defeated! You win!")
            break

        # Enemy turn
        enemy_turn(enemy, player)
        if player.health <= 0:
            print(f"\n{player.name} has been defeated! Game Over.")
            break

        show_stats(player, enemy)

    print("\nGame Ended.")


def main():
    """Main entry point for the game."""
    display_title()

    # Initialize game components
    player, enemy, cards = initialize_game()
    setup_game(player, enemy, cards)
    main_loop(player, enemy)

# Run the game
if __name__ == "__main__":
    main()