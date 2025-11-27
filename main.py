import os
import pyfiglet
from entities import Player, Enemy
from setup import load_cards, setup_player, setup_enemy, create_deck
from gameplay import start_game, show_stats, player_turn, enemy_turn

# ANSI color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"

def clear_screen():
    """Clear the console screen."""
    os.system("cls" if os.name == "nt" else "clear")

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
    print(Colors.CYAN + Colors.BOLD + title + Colors.RESET)

def main_loop(player, enemy):
    """Main turn-based game loop."""
    print(Colors.YELLOW + "Starting the game..." + Colors.RESET)
    start_game(player, enemy)

    print(Colors.MAGENTA)
    show_stats(player, enemy)
    print(Colors.RESET)

    while player.health > 0 and enemy.health > 0:

        input(Colors.YELLOW + "\nPress Enter to continue..." + Colors.RESET)
        clear_screen()

        # Player turn
        print(Colors.GREEN + Colors.BOLD + "Your Turn!" + Colors.RESET)
        player_turn(player, enemy)
        if enemy.health <= 0:
            print(Colors.GREEN + f"\n{enemy.name} has been defeated! You win!" + Colors.RESET)
            break

        input(Colors.YELLOW + "\nPress Enter to continue..." + Colors.RESET)
        clear_screen()

        # Enemy turn
        print(Colors.RED + Colors.BOLD + "Enemy Turn!" + Colors.RESET)
        enemy_turn(enemy, player)
        if player.health <= 0:
            print(Colors.RED + f"\n{player.name} has been defeated! Game Over." + Colors.RESET)
            break

        print(Colors.MAGENTA)
        show_stats(player, enemy)
        print(Colors.RESET)

    print(Colors.YELLOW + "\nGame Ended." + Colors.RESET)

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
