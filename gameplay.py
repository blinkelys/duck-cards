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

# --- Colors ---
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"


# --- Init game ---
def start_game(player, enemy):
    print(
        Colors.YELLOW +
        f"Your enemy is a {enemy.name} with {enemy.element} element." +
        Colors.RESET
    )
    print(Colors.CYAN + "Dealing initial hand..." + Colors.RESET)

    for _ in range(3):
        draw_card(player)

    show_hand(player)


def show_stats(player, enemy):
    print(Colors.MAGENTA + "--- Current Stats ---" + Colors.RESET)
    print(
        Colors.GREEN +
        f"{player.name} - Health: {player.health}, Mana: {player.mana}, Element: {player.element}" +
        Colors.RESET
    )
    print(
        Colors.RED +
        f"{enemy.name} - Health: {enemy.health}, Mana: {enemy.mana}, Element: {enemy.element}" +
        Colors.RESET
    )


def show_hand(player):
    print(Colors.BLUE + "\nYour current hand:" + Colors.RESET)
    for idx, card in enumerate(player.hand):
        print(
            f"{Colors.CYAN}{idx + 1}: {card['name']} "
            f"({card['element']} {card['mana_cost']} Mana){Colors.RESET}"
        )


# --- Handle cards ---
def draw_card(player):
    if not player.deck:
        print(Colors.RED + "No more cards in deck!" + Colors.RESET)
        return

    card = player.deck.pop(0)
    player.hand.append(card)
    print(
        Colors.GREEN +
        f"Drew card: {card['name']} ({card['element']} {card['mana_cost']} Mana)" +
        Colors.RESET
    )


def place_card(player):
    show_hand(player)
    selection = input(
        Colors.YELLOW + "Select a card to play by number (or press Enter to skip): " + Colors.RESET
    )

    if not selection:
        return None

    try:
        index = int(selection) - 1
        if 0 <= index < len(player.hand):
            card = player.hand.pop(index)
            player.activeCards.append(card)
            print(
                Colors.GREEN +
                f"Played card: {card['name']} ({card['element']} {card['mana_cost']} Mana)" +
                Colors.RESET
            )
            return card

        print(Colors.RED + "Invalid selection." + Colors.RESET)

    except ValueError:
        print(Colors.RED + "Please enter a valid number." + Colors.RESET)

    return None


# --- Turn logic ---
def player_turn(player, enemy):
    print(Colors.GREEN + Colors.BOLD + "\n--- Your Turn ---" + Colors.RESET)

    # Mana regen
    player.mana += MANA_REGEN_PER_TURN
    print(
        Colors.YELLOW +
        f"{player.name} regenerates {MANA_REGEN_PER_TURN} mana. Current mana: {player.mana}" +
        Colors.RESET
    )

    # Draw a card
    draw_card(player)

    # Choose card
    card = place_card(player)
    if card:
        apply_card_effect(card, player, enemy)


def enemy_turn(enemy, player):
    print(
        Colors.RED + Colors.BOLD +
        f"\n--- {enemy.name}'s Turn ---" +
        Colors.RESET
    )

    enemy.mana += MANA_REGEN_PER_TURN
    print(
        Colors.YELLOW +
        f"{enemy.name} regenerates {MANA_REGEN_PER_TURN} mana. Current mana: {enemy.mana}" +
        Colors.RESET
    )

    # Draw
    if enemy.deck:
        drawn = enemy.deck.pop(0)
        enemy.hand.append(drawn)

    # Find playable
    playable = [c for c in enemy.hand if c.get("mana_cost", 0) <= enemy.mana]

    if not playable:
        print(
            Colors.YELLOW +
            f"{enemy.name} has no cards it can play this turn." +
            Colors.RESET
        )
        return

    # Play random
    card = random.choice(playable)
    enemy.hand.remove(card)
    enemy.activeCards.append(card)

    print(
        Colors.RED +
        f"{enemy.name} plays {card['name']} ({card['element']})" +
        Colors.RESET
    )

    apply_card_effect(card, enemy, player)


# --- Card Effects ---
def calculate_damage(card, attacker, defender):
    if card.get("type", "").lower() != "attack":
        return 0

    base_damage = card.get("damage", 10)
    damage = base_damage

    # Element advantage
    if card.get("strong_against") == defender.element:
        damage = int(damage * 1.5)
        print(Colors.GREEN + f"Elemental advantage! Damage increased to {damage}" + Colors.RESET)
    elif card.get("weak_against") == defender.element:
        damage = int(damage * 0.5)
        print(Colors.RED + f"Elemental disadvantage! Damage reduced to {damage}" + Colors.RESET)

    # Shield effect
    if defender.activeShield:
        damage = int(damage * 0.5)
        print(
            Colors.YELLOW +
            f"{defender.name}'s shield absorbs damage! Damage reduced to {damage}" +
            Colors.RESET
        )
        defender.activeShield = 0

    # Curse effect
    if defender.activeCurse:
        damage = int(damage * 1.25)
        print(Colors.MAGENTA + f"{defender.name} is cursed! Damage increased to {damage}" + Colors.RESET)

    return damage


def apply_card_effect(card, attacker, defender):
    card_type = card.get("type", "").lower()
    mana_cost = card.get("mana_cost", 0)

    if attacker.mana < mana_cost:
        print(
            Colors.RED +
            f"{attacker.name} does not have enough mana to play {card['name']}!" +
            Colors.RESET
        )
        return

    attacker.mana -= mana_cost

    if card_type == "attack":
        damage = calculate_damage(card, attacker, defender)
        defender.health -= damage
        print(
            Colors.RED +
            f"{defender.name} takes {damage} damage! Remaining health: {defender.health}" +
            Colors.RESET
        )

    elif card_type == "heal":
        heal_amount = card.get("heal", 0)
        attacker.health = min(attacker.health + heal_amount, 100)
        print(
            Colors.GREEN +
            f"{attacker.name} heals {heal_amount} HP! Current health: {attacker.health}" +
            Colors.RESET
        )

    elif card_type == "shield":
        shield_value = card.get("damage", 0)
        attacker.activeShield = shield_value
        print(
            Colors.CYAN +
            f"{attacker.name} gains a shield of {shield_value} for next turn!" +
            Colors.RESET
        )

    print(
        Colors.YELLOW +
        f"{attacker.name} now has {attacker.mana} mana remaining." +
        Colors.RESET
    )