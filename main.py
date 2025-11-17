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
    def chooseElement()_    
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
    
    def confrimPlayer():   
        print(player)
        print("Is this correct? Y/n")
        selection = input().lower()
        if selection == "y":
            pass
        elif selection == "n":
            playerSetup()
        else:
            print("Please choose a valid option!")
    confrimPlayer()