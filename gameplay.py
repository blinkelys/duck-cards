# gameplay.py
def start_game(player, enemy):
    print(f"Your enemy is a {enemy.name} with {enemy.element} element.")
    print("Dealing initial hand...")
    for _ in range(3):
        if player.deck:
            card = player.deck.pop(0)
            player.hand.append(card)
    show_hand(player)

def show_stats(player, enemy):
    print(f"{player.name} - Health: {player.health}, Mana: {player.mana}, Element: {player.element}")
    print(f"{enemy.name} - Health: {enemy.health}, Mana: {enemy.mana}, Element: {enemy.element}")

def show_hand(player):
    print("Your current hand:")
    for card in player.hand:
        print(f"- {card['name']} ({card['element']})")

def draw_card(player):
    if player.deck:
        card = player.deck.pop(0)
        player.hand.append(card)
        print(f"Drew card: {card['name']} ({card['element']})")
    else:
        print("No more cards in deck!")

def place_card(player):
    show_hand(player)
    print("Select a card to play by number:")
    for idx, card in enumerate(player.hand):
        print(f"{idx + 1}: {card['name']} ({card['element']})")
    
    selection = input()
    try:
        index = int(selection) - 1
        if 0 <= index < len(player.hand):
            card = player.hand.pop(index)
            player.activeCards.append(card)
            print(f"Played card: {card['name']} ({card['element']})")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")
