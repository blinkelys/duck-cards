# gameplay.py

import random

# --- Constants ---

MANA_REGEN_PER_TURN = 5

ELEMENT_ADVANTAGE = {
    "Fire": "Earth",
    "Earth": "Air",
    "Air": "Water",
    "Water": "Fire"
}


# Init game
def start_game(player, enemy):
    """Initialize the game and deal the starting hand."""
    print(f"Your enemy is a {enemy.name} with {enemy.element} element.")
    print("Dealing initial hand...")

    for _ in range(3):
        draw_card(player)
    show_hand(player)

def show_stats(player, enemy):
    """Display the current health, mana, and elements."""
    print(f"{player.name} - Health: {player.health}, Mana: {player.mana}, Element: {player.element}")
    print(f"{enemy.name} - Health: {enemy.health}, Mana: {enemy.mana}, Element: {enemy.element}")

def show_hand(player):
    """Print all cards currently in the player's hand."""
    print("Your current hand:")
    for idx, card in enumerate(player.hand):
        print(f"{idx + 1}: {card['name']} ({card['element']} {card['mana_cost']} Mana)")

# Handle cards
def draw_card(player):
    """Draw a card from the player's deck into their hand."""
    if not player.deck:
        print("No more cards in deck!")
        return

    card = player.deck.pop(0)
    player.hand.append(card)
    print(f"Drew card: {card['name']} ({card['element']} {card['mana_cost']} Mana)")

def place_card(player):
    """Allow the player to select a card to play."""
    show_hand(player)
    selection = input("Select a card to play by number (or press Enter to skip): ")

    if not selection:
        return None

    try:
        index = int(selection) - 1
        if 0 <= index < len(player.hand):
            card = player.hand.pop(index)
            player.activeCards.append(card)
            print(f"Played card: {card['name']} ({card['element']} {card['mana_cost']} Mana)")
            return card

        print("Invalid selection.")

    except ValueError:
        print("Please enter a valid number.")
    return None


# Turn logic
def player_turn(player, enemy):
    print("\n--- Your Turn ---")

    # Mana regen
    player.mana += MANA_REGEN_PER_TURN
    print(f"{player.name} regenerates {MANA_REGEN_PER_TURN} mana. Current mana: {player.mana}")

    # Draw a card for player
    draw_card(player)

    # Player chooses a card to play
    card = place_card(player)
    if card:
        apply_card_effect(card, player, enemy)

def enemy_turn(enemy, player):
    print(f"\n--- {enemy.name}'s Turn ---")
    enemy.mana += MANA_REGEN_PER_TURN
    print(f"{enemy.name} regenerates {MANA_REGEN_PER_TURN} mana. Current mana: {enemy.mana}")
    # Draw a card for enemy
    if enemy.deck:
        drawn = enemy.deck.pop(0)
        enemy.hand.append(drawn)

    # Select cards enemy can afford
    playable = [c for c in enemy.hand if c.get("mana_cost", 0) <= enemy.mana]

    if not playable:
        print(f"{enemy.name} has no cards it can play this turn.")
        return

    # Play a random card
    card = random.choice(playable)
    enemy.hand.remove(card)
    enemy.activeCards.append(card)

    print(f"{enemy.name} plays {card['name']} ({card['element']})")

    apply_card_effect(card, enemy, player)

# --- Card Effects ---
def calculate_damage(card, attacker, defender):
    """Calculate damage considering type, elemental modifiers, shields, and curses."""
    if card.get("type", "").lower() != "attack":
        return 0

    base_damage = card.get("damage", 10)
    damage = base_damage

    # Elemental advantage/disadvantage
    if card.get("strong_against") == defender.element:
        damage = int(damage * 1.5)
        print(f"Elemental advantage! Damage increased to {damage}")
    elif card.get("weak_against") == defender.element:
        damage = int(damage * 0.5)
        print(f"Elemental disadvantage! Damage reduced to {damage}")

    # Shield reduces damage
    if defender.activeShield:
        damage = int(damage * 0.5)
        print(f"{defender.name}'s shield absorbs damage! Damage reduced to {damage}")
        defender.activeShield = 0  # Shield consumed

    # Curse increases damage
    if defender.activeCurse:
        damage = int(damage * 1.25)
        print(f"{defender.name} is cursed! Damage increased to {damage}")
    return damage

def apply_card_effect(card, attacker, defender):
    """
    Applies the effect of a card:
      - Mana deduction
      - Attack (damage)
      - Heal
      - Shield
    """
    card_type = card.get("type", "").lower()
    mana_cost = card.get("mana_cost", 0)

    if attacker.mana < mana_cost:
        print(f"{attacker.name} does not have enough mana to play {card['name']}!")
        return

    attacker.mana -= mana_cost

    if card_type == "attack":
        damage = calculate_damage(card, attacker, defender)
        defender.health -= damage
        print(f"{defender.name} takes {damage} damage! Remaining health: {defender.health}")

    elif card_type == "heal":
        heal_amount = card.get("heal", 0)
        attacker.health = min(attacker.health + heal_amount, 100)
        print(f"{attacker.name} heals {heal_amount} HP! Current health: {attacker.health}")

    elif card_type == "shield":
        shield_value = card.get("damage", 0)  # Using "damage" field as shield strength
        attacker.activeShield = shield_value
        print(f"{attacker.name} gains a shield of {shield_value} for next turn!")

    print(f"{attacker.name} now has {attacker.mana} mana remaining.")