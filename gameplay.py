import random

# ================================================
# CONSTANTS & CONFIG
# ================================================

MANA_REGEN_PER_TURN = 5

ELEMENT_ADVANTAGE = {
    "Fire": "Earth",
    "Earth": "Air",
    "Air": "Water",
    "Water": "Fire"
}

MAX_HEALTH = 100


# ================================================
# COLORS
# ================================================
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"


# ================================================
# CORE GAMEPLAY FUNCTIONS
# ================================================

def start_game(player, enemy):
    print(
        Colors.YELLOW +
        f"Your enemy is a {enemy.name} ({enemy.element})." +
        Colors.RESET
    )

    print(Colors.CYAN + "Dealing initial hand..." + Colors.RESET)
    for _ in range(3):
        draw_card(player)

    show_hand(player)


# ------------------------------------------------
# DISPLAY HELPERS
# ------------------------------------------------

def show_stats(player, enemy):
    print(Colors.MAGENTA + "\n--- Current Stats ---" + Colors.RESET)
    print(
        Colors.GREEN +
        f"{player.name}: {player.health} HP | {player.mana} Mana | Shield: {player.shield}" +
        Colors.RESET
    )
    print(
        Colors.RED +
        f"{enemy.name}: {enemy.health} HP | {enemy.mana} Mana | Shield: {enemy.shield}" +
        Colors.RESET
    )


def show_hand(player):
    print(Colors.BLUE + "\nYour current hand:" + Colors.RESET)

    if not player.hand:
        print(Colors.YELLOW + "Your hand is empty!" + Colors.RESET)
        return

    for i, card in enumerate(player.hand, 1):
        print(
            f"{Colors.CYAN}{i}: {card['name']} "
            f"({card['type']} | {card['mana_cost']} Mana){Colors.RESET}"
        )


# ------------------------------------------------
# DRAWING + PLAYING CARDS
# ------------------------------------------------

def draw_card(player):
    if not player.deck:
        print(Colors.RED + "Your deck is empty!" + Colors.RESET)
        return

    card = player.deck.pop(0)
    player.hand.append(card)

    print(
        Colors.GREEN +
        f"Drew card: {card['name']} ({card['element']} {card['mana_cost']} Mana)" +
        Colors.RESET
    )


def choose_card(player):
    show_hand(player)
    choice = input(Colors.YELLOW +
                   "Select a card number (Enter = Skip): " + Colors.RESET)

    if not choice:
        return None

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(player.hand):
            print(Colors.RED + "Invalid card." + Colors.RESET)
            return None
        return player.hand.pop(idx)

    except ValueError:
        print(Colors.RED + "Invalid input." + Colors.RESET)
        return None


# ================================================
# TURN HANDLING
# ================================================

def player_turn(player, enemy):
    print(Colors.GREEN + Colors.BOLD + "\n--- YOUR TURN ---" + Colors.RESET)

    # Regenerate mana
    player.mana += MANA_REGEN_PER_TURN
    print(
        Colors.YELLOW +
        f"You regenerate {MANA_REGEN_PER_TURN} mana. (Now {player.mana})" +
        Colors.RESET
    )

    # Draw card
    draw_card(player)

    # Apply curse effects
    resolve_curse(player)

    # Choose card
    card = choose_card(player)
    if card:
        apply_card(card, player, enemy)


def enemy_turn(enemy, player):
    print(Colors.RED + Colors.BOLD +
          f"\n--- {enemy.name.upper()} TURN ---" + Colors.RESET)

    enemy.mana += MANA_REGEN_PER_TURN
    print(
        Colors.YELLOW +
        f"{enemy.name} regenerates {MANA_REGEN_PER_TURN} mana. (Now {enemy.mana})" +
        Colors.RESET
    )

    resolve_curse(enemy)

    # Draw
    if enemy.deck:
        enemy.hand.append(enemy.deck.pop(0))

    # Choose playable card
    playable = [c for c in enemy.hand if c["mana_cost"] <= enemy.mana]

    if not playable:
        print(
            Colors.YELLOW +
            f"{enemy.name} has no playable cards!" +
            Colors.RESET
        )
        return

    card = random.choice(playable)
    enemy.hand.remove(card)

    print(
        Colors.RED +
        f"{enemy.name} plays {card['name']} ({card['type']})" +
        Colors.RESET
    )

    apply_card(card, enemy, player)


# ================================================
# CARD EFFECTS
# ================================================

def apply_card(card, attacker, defender):
    card_type = card["type"].lower()
    cost = card["mana_cost"]

    if attacker.mana < cost:
        print(
            Colors.RED +
            f"Not enough mana to play {card['name']}!" +
            Colors.RESET
        )
        return

    attacker.mana -= cost

    if card_type == "attack":
        do_attack(card, attacker, defender)

    elif card_type == "defense":
        do_shield(card, attacker)

    elif card_type == "heal":
        do_heal(card, attacker)

    elif card_type == "curse":
        do_curse(card, attacker, defender)

    print(
        Colors.YELLOW +
        f"{attacker.name} has {attacker.mana} mana remaining." +
        Colors.RESET
    )


# ------------------------------------------------
# ATTACK
# ------------------------------------------------

def do_attack(card, attacker, defender):
    damage = card.get("damage", 0)

    # Element advantage
    if ELEMENT_ADVANTAGE.get(card["element"]) == defender.element:
        damage = int(damage * 1.5)
        print(Colors.GREEN + "Elemental advantage! +50% damage." + Colors.RESET)

    elif ELEMENT_ADVANTAGE.get(defender.element) == card["element"]:
        damage = int(damage * 0.5)
        print(Colors.RED + "Elemental disadvantage! -50% damage." + Colors.RESET)

    # Ensure defender.shield exists
    if defender.shield is None:
        defender.shield = 0

    # Apply shield
    if defender.shield > 0:
        absorbed = min(damage, defender.shield)
        defender.shield -= absorbed
        damage -= absorbed

        print(
            Colors.YELLOW +
            f"{defender.name}'s shield absorbs {absorbed} damage!" +
            Colors.RESET
        )

        # FIX: Shield actually breaks
        if defender.shield <= 0:
            defender.shield = 0
            print(
                Colors.YELLOW +
                f"{defender.name}'s shield breaks!" +
                Colors.RESET
            )

    # Remaining damage
    defender.health -= damage
    print(
        Colors.RED +
        f"{defender.name} takes {damage} damage! (Now {defender.health})" +
        Colors.RESET
    )

# ------------------------------------------------
# HEAL
# ------------------------------------------------
def do_heal(card, player):
    # Use card damage if negative for heal
    heal_amount = -card.get("damage", 0)  # negative damage = heal
    player.health = min(MAX_HEALTH, player.health + heal_amount)

    print(
        Colors.GREEN +
        f"{player.name} heals {heal_amount} HP! (Now {player.health})" +
        Colors.RESET
    )


# ------------------------------------------------
# SHIELD
# ------------------------------------------------
def do_shield(card, player):
    # Safely extract shield amount from card["effect"]
    text = card.get("effect", "").lower()
    amount = 15  # fallback

    import re
    match = re.search(r'(\d+)', text)
    if match:
        amount = int(match.group(1))

    # Stack shields
    if hasattr(player, "shield") and player.shield:
        player.shield += amount
    else:
        player.shield = amount

    print(
        Colors.CYAN +
        f"{player.name} gains a shield absorbing {amount} damage! (Total {player.shield})" +
        Colors.RESET
    )


# ------------------------------------------------
# CURSE EFFECTS
# ------------------------------------------------
def do_curse(card, attacker, defender):
    effect = card["effect"].lower()

    # Mana loss curse
    if "loses" in effect and "mana" in effect:
        amount = int(effect.split("loses ")[1].split(" ")[0])
        defender.curse_mana_loss = amount
        print(
            Colors.MAGENTA +
            f"{defender.name} is cursed and will lose {amount} mana next turn!" +
            Colors.RESET
        )
    # Skip turn curse
    elif "skips" in effect and "turn" in effect:
        defender.skip_turn = True
        print(
            Colors.MAGENTA +
            f"{defender.name} is cursed and will skip their next turn!" +
            Colors.RESET
        )
    # Discard card curse
    elif "discard" in effect and "card" in effect:
        defender.discard_next = True
        print(
            Colors.MAGENTA +
            f"{defender.name} is cursed and must discard a card next turn!" +
            Colors.RESET
        )


def resolve_curse(player):
    if hasattr(player, "curse_mana_loss") and player.curse_mana_loss > 0:
        print(
            Colors.MAGENTA +
            f"{player.name} loses {player.curse_mana_loss} mana due to curse!" +
            Colors.RESET
        )
        player.mana = max(0, player.mana - player.curse_mana_loss)
        player.curse_mana_loss = 0

    if hasattr(player, "skip_turn") and player.skip_turn:
        print(
            Colors.MAGENTA +
            f"{player.name} skips their turn due to curse!" +
            Colors.RESET
        )
        player.skip_turn = False
        return True  # signal to skip turn
    return False
