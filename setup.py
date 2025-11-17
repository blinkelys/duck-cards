# setup.py
import random
import json
from entities import Player, Enemy

# Load cards from cards.json
def load_cards(filename="./cards.json"):
    with open(filename, "r") as file:
        cards = json.load(file)
    return normalize_cards(cards)

    # Ensure all cards have required fields with correct types
def normalize_cards(cards):
    normalized = []
    for card in cards:
        card['type'] = card.get('type', 'attack').lower()
        card['mana_cost'] = int(card.get('mana_cost', 0))
        card['damage'] = int(card.get('damage', 0))
        card['strong_against'] = card.get('strong_against', None)
        card['weak_against'] = card.get('weak_against', None)
        normalized.append(card)
    return normalized

# Setup functions
def setup_enemy(enemy):
    # Randomly assign enemy name and element
    enemy_types = ["Goblin", "Orc", "Troll", "Dark Mage", "Skeleton Warrior", "Vampire", "Werewolf", "Zombie", "Demon", "Ghost"]
    enemy.name = random.choice(enemy_types)
    enemy.element = random.choice(["Fire", "Water", "Earth", "Air"])

# Setup player with input
def setup_player(player):
    player.name = input("What is your name? ")

    # Element selection
    def choose_element():
        print("Choose your element: 1: Fire, 2: Water, 3: Earth, 4: Air")
        choice = input()
        mapping = {"1": "Fire", "2": "Water", "3": "Earth", "4": "Air"}
        # Map user input to element
        if choice in mapping:
            player.element = mapping[choice]
        else:
            print("Invalid selection.")
            choose_element()
    
    choose_element()
    
    # Confirm selection
    print(f"{player.name}, your chosen element is {player.element}. Is this correct? Y/n")
    confirm = input().lower()
    if confirm == "n":
        setup_player(player)

# Create deck for player or enemy
def create_deck(player, cards):
    element_cards = [c for c in cards if c['element'] == player.element]
    other_cards = [c for c in cards if c['element'] != player.element]
    
    # Build a deck of 20 cards
    while len(player.deck) < 20:
        card = random.choice(element_cards) if random.random() < 0.6 and element_cards else random.choice(other_cards)
        if card not in player.deck:
            player.deck.append(card)
