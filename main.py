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

