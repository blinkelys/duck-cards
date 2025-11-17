# setup.py
import random
import json
from entities import Player, Enemy

def load_cards(filename="./cards.json"):
    with open(filename, "r") as file:
        return json.load(file)

def setup_enemy(enemy):
    enemy_types = ["Goblin", "Orc", "Troll", "Dark Mage", "Skeleton Warrior", "Vampire", "Werewolf", "Zombie", "Demon", "Ghost"]
    enemy.name = random.choice(enemy_types)
    enemy.element = random.choice(["Fire", "Water", "Earth", "Air"])

def setup_player(player):
    player.name = input("What is your name? ")

    def choose_element():
        print("Choose your element: 1: Fire, 2: Water, 3: Earth, 4: Air")
        choice = input()
        mapping = {"1": "Fire", "2": "Water", "3": "Earth", "4": "Air"}
        if choice in mapping:
            player.element = mapping[choice]
        else:
            print("Invalid selection.")
            choose_element()
    
    choose_element()
    
    print(f"{player.name}, your chosen element is {player.element}. Is this correct? Y/n")
    confirm = input().lower()
    if confirm == "n":
        setup_player(player)

def create_deck(player, cards):
    element_cards = [c for c in cards if c['element'] == player.element]
    other_cards = [c for c in cards if c['element'] != player.element]
    
    while len(player.deck) < 20:
        card = random.choice(element_cards) if random.random() < 0.6 and element_cards else random.choice(other_cards)
        if card not in player.deck:
            player.deck.append(card)
