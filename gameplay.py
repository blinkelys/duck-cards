# gameplay.py
import random

def start_game(player, enemy):
    print(f"Your enemy is a {enemy.name} with {enemy.element} element.")
    print("Dealing initial hand...")
    for _ in range(3):
        draw_card(player)
    show_hand(player)

def show_stats(player, enemy):
    print(f"{player.name} - Health: {player.health}, Mana: {player.mana}, Element: {player.element}")
    print(f"{enemy.name} - Health: {enemy.health}, Mana: {enemy.mana}, Element: {enemy.element}")

def show_hand(player):
    print("Your current hand:")
    for idx, card in enumerate(player.hand):
        print(f"{idx + 1}: {card['name']} ({card['element']})")

def draw_card(player):
    if player.deck:
        card = player.deck.pop(0)
        player.hand.append(card)
        print(f"Drew card: {card['name']} ({card['element']})")
    else:
        print("No more cards in deck!")

def place_card(player):
    show_hand(player)
    selection = input("Select a card to play by number (or press Enter to skip): ")
    if selection == "":
        return None
    try:
        index = int(selection) - 1
        if 0 <= index < len(player.hand):
            card = player.hand.pop(index)
            player.activeCards.append(card)
            print(f"Played card: {card['name']} ({card['element']})")
            return card
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")
    return None

def player_turn(player, enemy):
    print("\n--- Your Turn ---")
    draw_card(player)
    card = place_card(player)
    if card:
        # Simple damage calculation (example)
        damage = random.randint(5, 15)
        enemy.health -= damage
        print(f"{enemy.name} takes {damage} damage!")

def enemy_turn(enemy, player):
    print(f"\n--- {enemy.name}'s Turn ---")
    # Enemy draws a card if deck is not empty
    if enemy.deck:
        card = enemy.deck.pop(0)
        enemy.hand.append(card)
    
    # Enemy plays a random card
    if enemy.hand:
        card = random.choice(enemy.hand)
        enemy.hand.remove(card)
        enemy.activeCards.append(card)
        damage = random.randint(5, 12)
        player.health -= damage
        print(f"{enemy.name} plays {card['name']} ({card['element']}) and deals {damage} damage!")
    else:
        print(f"{enemy.name} has no cards to play.")
