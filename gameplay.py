# gameplay.py
import random

# gameplay.py (top)
ELEMENT_ADVANTAGE = {
    "Fire": "Earth",
    "Earth": "Air",
    "Air": "Water",
    "Water": "Fire"
}

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

    # Regenerate mana
    player.mana += MANA_REGEN_PER_TURN
    print(f"{player.name} regenerates {MANA_REGEN_PER_TURN} mana. Current mana: {player.mana}")

    # Draw a card
    draw_card(player)

    # Play a card
    card = place_card(player)
    if card:
        apply_card_effect(card, player, enemy)


def enemy_turn(enemy, player):
    print(f"\n--- {enemy.name}'s Turn ---")

    # Mana regen
    enemy.mana += MANA_REGEN_PER_TURN

    # Draw a card
    if enemy.deck:
        card = enemy.deck.pop(0)
        enemy.hand.append(card)

    # Choose playable cards
    playable_cards = [c for c in enemy.hand if c.get("mana_cost", 0) <= enemy.mana]
    if not playable_cards:
        print(f"{enemy.name} has no cards it can play this turn.")
        return

    # Play a random card
    card = random.choice(playable_cards)
    enemy.hand.remove(card)
    enemy.activeCards.append(card)
    print(f"{enemy.name} plays {card['name']} ({card['element']})")
    apply_card_effect(card, enemy, player)


def calculate_damage(card, attacker, defender):
    if card.get("type", "").lower() != "attack":
        return 0  # Only attack cards deal damage

    base_damage = card.get("damage", 10)
    damage = base_damage

    # Elemental advantage
    if card.get("strong_against") == defender.element:
        damage = int(damage * 1.5)
        print(f"Elemental advantage! Damage increased to {damage}")
    elif card.get("weak_against") == defender.element:
        damage = int(damage * 0.5)
        print(f"Elemental disadvantage! Damage reduced to {damage}")

    # Shields reduce damage
    if defender.activeShield:
        damage = int(damage * 0.5)
        print(f"{defender.name}'s shield absorbs damage! Damage reduced to {damage}")
        defender.activeShield = 0  # shield consumed

    # Curses increase damage (optional)
    if defender.activeCurse:
        damage = int(damage * 1.25)
        print(f"{defender.name} is cursed! Damage increased to {damage}")

    return damage

MANA_REGEN_PER_TURN = 5  # how much mana player/enemy regenerates each turn

def apply_card_effect(card, attacker, defender):
    """
    Applies the card effect to the attacker and defender
    Handles mana cost, damage, heal, and shields
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
        shield_value = card.get("damage", 0)  # use damage field as shield strength
        attacker.activeShield = shield_value
        print(f"{attacker.name} gains a shield of {shield_value} for next turn!")

    print(f"{attacker.name} now has {attacker.mana} mana remaining.")
