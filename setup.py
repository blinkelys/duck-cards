# setup.py
import random
import json
from entities import Player, Enemy

# Load cards from JSON
def load_cards(filename="./cards.json"):
    """Load cards from JSON and normalize their fields."""
    with open(filename, "r") as file:
        cards = json.load(file)
    return normalize_cards(cards)

# Normalize card data
def normalize_cards(cards):
    """Ensure all cards contain the expected fields with correct types."""
    normalized = []

    for card in cards:
        normalized.append({
            "name": card.get("name", "Unknown Card"),
            "type": card.get("type", "attack").lower(),
            "element": card.get("element", None),

            # numeric fields
            "mana_cost": int(card.get("mana_cost", 0)),
            "damage": int(card.get("damage", 0)),

            # optional fields
            "strong_against": card.get("strong_against"),
            "weak_against": card.get("weak_against"),
            "effect": card.get("effect", ""),
        })

    return normalized

# Setup Enemy
def setup_enemy(enemy):
    """Assign an enemy name and element."""
    enemy.name = random.choice([
        "Goblin", "Orc", "Troll", "Dark Mage",
        "Skeleton Warrior", "Vampire", "Werewolf",
        "Zombie", "Demon", "Ghost"
    ])

    enemy.element = random.choice(["Fire", "Water", "Earth", "Air"])

# Setup Player
def setup_player(player):
    """Initialize player name and element selection."""
    player.name = input("What is your name? ").strip()

    element_map = {
        "1": "Fire",
        "2": "Water",
        "3": "Earth",
        "4": "Air"
    }

    while True:
        print("Choose your element:\n1: Fire  2: Water  3: Earth  4: Air")
        choice = input("> ").strip()

        if choice in element_map:
            player.element = element_map[choice]
        else:
            print("Invalid selection.\n")
            continue

        confirm = input(f"{player.name}, your chosen element is {player.element}. Confirm? (Y/n): ").strip().lower()
        if confirm != "n":
            break  # accepted
        print()

    return player

# Create a deck for the player
def create_deck(player, cards):
    """
    Build a deck of 20 cards.
    Player has a 60% chance to draw from their own element.
    Deck prevents duplicates.
    """
    element_cards = [c for c in cards if c["element"] == player.element]
    other_cards = [c for c in cards if c["element"] != player.element]

    # Continue until 20 unique cards
    while len(player.deck) < 20:
        pool = element_cards if random.random() < 0.6 and element_cards else other_cards
        card = random.choice(pool)

        if card not in player.deck:
            player.deck.append(card)