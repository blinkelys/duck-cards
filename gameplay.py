import random
import re

# Core constants
MANA_REGEN = 5
MAX_HEALTH = 100

# Elemental strengths
ELEMENT_ADV = {
    "Fire": "Earth",
    "Earth": "Air",
    "Air": "Water",
    "Water": "Fire"
}

# Color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"

# Game start / Display
def start_game(player, enemy):
    print(f"{Colors.YELLOW}Your enemy is a {enemy.name} ({enemy.element}).{Colors.RESET}")

    print(f"{Colors.CYAN}Dealing initial hand...{Colors.RESET}")
    for _ in range(3):
        draw_card(player)

    show_hand(player)

# Display stats
def show_stats(player, enemy):
    print(f"{Colors.MAGENTA}\n--- Current Stats ---{Colors.RESET}")
    print(f"{Colors.GREEN}{player.name}: {player.health} HP | {player.mana} Mana | Shield: {player.shield}{Colors.RESET}")
    print(f"{Colors.RED}{enemy.name}: {enemy.health} HP | {enemy.mana} Mana | Shield: {enemy.shield}{Colors.RESET}")

# Display player's hand
def show_hand(player):
    print(f"{Colors.BLUE}\nYour current hand:{Colors.RESET}")

    if not player.hand:
        print(f"{Colors.YELLOW}Your hand is empty!{Colors.RESET}")
        return

    for i, card in enumerate(player.hand, 1):
        print(f"{Colors.CYAN}{i}: {card['name']} ({card['type']} | {card['mana_cost']} Mana){Colors.RESET}")

# Draw a card from deck
def draw_card(player):
    if not player.deck:
        print(f"{Colors.RED}Your deck is empty!{Colors.RESET}")
        return

    card = player.deck.pop(0)
    player.hand.append(card)
    print(f"{Colors.GREEN}Drew: {card['name']} ({card['element']} {card['mana_cost']} Mana){Colors.RESET}")

# Player card selection
def choose_card(player):
    show_hand(player)
    choice = input(f"{Colors.YELLOW}Select card number (Enter = Skip): {Colors.RESET}")

    if not choice:
        return None

    try:
        idx = int(choice) - 1
        return player.hand.pop(idx) if 0 <= idx < len(player.hand) else None
    except ValueError:
        return None

# Player turn logic
def player_turn(player, enemy):
    print(f"{Colors.GREEN}{Colors.BOLD}\n--- YOUR TURN ---{Colors.RESET}")

    player.mana += MANA_REGEN
    print(f"{Colors.YELLOW}You regenerate {MANA_REGEN} mana. (Now {player.mana}){Colors.RESET}")

    draw_card(player)

    if resolve_curse(player):
        return

    card = choose_card(player)
    if card:
        apply_card(card, player, enemy)

# Enemy turn logic
def enemy_turn(enemy, player):
    print(f"{Colors.RED}{Colors.BOLD}\n--- {enemy.name.upper()} TURN ---{Colors.RESET}")

    enemy.mana += MANA_REGEN
    print(f"{Colors.YELLOW}{enemy.name} regenerates {MANA_REGEN} mana. (Now {enemy.mana}){Colors.RESET}")

    if resolve_curse(enemy):
        return

    if enemy.deck:
        enemy.hand.append(enemy.deck.pop(0))

    playable = [c for c in enemy.hand if c["mana_cost"] <= enemy.mana]

    if not playable:
        print(f"{Colors.YELLOW}{enemy.name} has no playable cards!{Colors.RESET}")
        return

    card = random.choice(playable)
    enemy.hand.remove(card)

    print(f"{Colors.RED}{enemy.name} plays {card['name']} ({card['type']}){Colors.RESET}")
    apply_card(card, enemy, player)

# Does card effects
def apply_card(card, attacker, defender):
    cost = card["mana_cost"]
    if attacker.mana < cost:
        print(f"{Colors.RED}Not enough mana to play {card['name']}!{Colors.RESET}")
        return

    attacker.mana -= cost
    ctype = card["type"].lower()

    effect_funcs = {
        "attack": do_attack,
        "defense": do_shield,
        "heal": do_heal,
        "curse": do_curse
    }

    if ctype in effect_funcs:
        effect_funcs[ctype](card, attacker, defender)

    print(f"{Colors.YELLOW}{attacker.name} has {attacker.mana} mana remaining.{Colors.RESET}")

# Attack effects
def do_attack(card, attacker, defender):
    damage = card.get("damage", 0)

    # Element modifier
    if ELEMENT_ADV.get(card["element"]) == defender.element:
        damage = int(damage * 1.5)
        print(f"{Colors.GREEN}Elemental advantage! +50% damage.{Colors.RESET}")
    elif ELEMENT_ADV.get(defender.element) == card["element"]:
        damage = int(damage * 0.5)
        print(f"{Colors.RED}Elemental disadvantage! -50% damage.{Colors.RESET}")

    # Shield absorb
    absorbed = min(damage, defender.shield)
    defender.shield -= absorbed
    damage -= absorbed

    if absorbed:
        print(f"{Colors.YELLOW}{defender.name}'s shield absorbs {absorbed}!{Colors.RESET}")

    if defender.shield <= 0:
        defender.shield = 0

    defender.health -= damage
    print(f"{Colors.RED}{defender.name} takes {damage} damage! (Now {defender.health}){Colors.RESET}")

# Heal effects
def do_heal(card, player, *_):
    heal_amount = -card.get("damage", 0)  # negative damage acts as heal
    player.health = min(MAX_HEALTH, player.health + heal_amount)
    print(f"{Colors.GREEN}{player.name} heals {heal_amount}! (Now {player.health}){Colors.RESET}")

# Shield effects
def do_shield(card, player, *_):
    text = card.get("effect", "").lower()
    amount = 15

    match = re.search(r"(\d+)", text)
    if match:
        amount = int(match.group(1))

    player.shield += amount
    print(f"{Colors.CYAN}{player.name} gains {amount} shield! (Total {player.shield}){Colors.RESET}")

# Curse effects
def do_curse(card, attacker, defender):
    effect = card["effect"].lower()

    if "loses" in effect and "mana" in effect:
        defender.curse_mana_loss = int(effect.split("loses ")[1].split(" ")[0])
        print(f"{Colors.MAGENTA}{defender.name} will lose mana next turn!{Colors.RESET}")

    elif "skips" in effect:
        defender.skip_turn = True
        print(f"{Colors.MAGENTA}{defender.name} will skip their next turn!{Colors.RESET}")

    elif "discard" in effect:
        defender.discard_next = True
        print(f"{Colors.MAGENTA}{defender.name} must discard a card next turn!{Colors.RESET}")

# Resolve curses at turn start
def resolve_curse(player):
    if getattr(player, "curse_mana_loss", 0) > 0:
        loss = player.curse_mana_loss
        player.mana = max(0, player.mana - loss)
        print(f"{Colors.MAGENTA}{player.name} loses {loss} mana due to curse!{Colors.RESET}")
        player.curse_mana_loss = 0

    if getattr(player, "skip_turn", False):
        print(f"{Colors.MAGENTA}{player.name} skips their turn!{Colors.RESET}")
        player.skip_turn = False
        return True

    return False