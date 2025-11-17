import random
import time
import json

with open('./cards.json', 'r') as file:
    cards = json.load(file)

class player():
    name = ""
    health = 100
    mana = 20
    element = ""
    activeCurse = ""
    activeShield = ""
    activeCards = []
    deck = []
    hand = []

class enemy():
    name = ""
    health = 100
    mana = 20
    element = ""
    activeCurse = ""
    activeShield = ""
    activeCards = []
    deck = []
    hand = []

enemyTypes = ["Goblin", "Orc", "Troll", "Dark Mage", "Skeleton Warrior", "Vampire", "Werewolf", "Zombie", "Demon", "Ghost"]

def enemySetup():
    enemy.name = random.choice(enemyTypes)
    enemy.element = random.choice(["Fire", "Water", "Earth", "Air"])

enemySetup()

def playerSetup():
    print("What is your name? ")
    player.name = input()
    
    print("What is your preferred element?")
    def chooseElement():
        print("1: Fire, 2: Water, 3: Earth, 4: Air")
        playerElementPrivate = input()
        if playerElementPrivate == "1":
            player.element = "Fire"
        elif playerElementPrivate == "2":
            player.element = "Water"
        elif playerElementPrivate == "3":
            player.element = "Earth"
        elif playerElementPrivate == "4":
            player.element = "Air"
        else:
            print("Please pick one of the valid elements:")
    chooseElement()
    
    def confirmPlayer():   
        print(player.name + ", your chosen element is " + player.element + ".")
        print("Is this correct? Y/n")
        selection = input().lower()
        if selection == "y":
            pass
        elif selection == "n":
            playerSetup()
        else:
            print("Please choose a valid option!")
    confirmPlayer()

playerSetup()

def createDeck():
    elementCards = [card for card in cards if card['element'] == player.element]
    otherCards = [card for card in cards if card['element'] != player.element]
    
    while len(player.deck) < 20:
        if random.random() < 0.6 and elementCards:
            card = random.choice(elementCards)
        else:
            card = random.choice(otherCards)
        
        if card not in player.deck:
            player.deck.append(card)

createDeck()

print("Deck created with the following cards:")
for card in player.deck:
    print(f"- {card['name']} ({card['element']})")  

def setupComplete():
    print("Game setup complete. Ready to play?")
    selection = input("Y/n: ").lower()
    if selection == "y":
        print("Starting game...")
    elif selection == "n":
        print("Exiting setup.")
    else:
        print("Please choose a valid option!")
        setupComplete()

setupComplete()

# Ingame Functions
def startGame():
    print("Your enemy is a " + enemy.name + " with " + enemy.element + " element.")

    print("Dealing initial hand...")
    for _ in range(3):
        if player.deck:
            card = player.deck.pop(0)
            player.hand.append(card)
    print("Your starting hand:")
    for card in player.hand:
        print(f"- {card['name']} ({card['element']})")

startGame()

# Display Player and Enemy Stats
def showStats():
    print(f"{player.name} - Health: {player.health}, Mana: {player.mana}, Element: {player.element}")
    print(f"{enemy.name} - Health: {enemy.health}, Mana: {enemy.mana}, Element: {enemy.element}")

# Show Player Hand
def showHand():
    print("Your current hand:")
    for card in player.hand:
        print(f"- {card['name']} ({card['element']})")

# Draw a Card
def drawCard():
    if player.deck:
        card = player.deck.pop(0)
        player.hand.append(card)
        print(f"Drew card: {card['name']} ({card['element']})")
    else:
        print("No more cards in deck!")

def placeCard():
    showHand()
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
