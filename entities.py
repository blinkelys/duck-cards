# entities.py
class Player:
    def __init__(self):
        self.name = ""
        self.health = 100
        self.mana = 20
        self.element = ""
        self.activeCurse = ""
        self.activeShield = ""
        self.activeCards = []
        self.deck = []
        self.hand = []

class Enemy:
    def __init__(self):
        self.name = ""
        self.health = 100
        self.mana = 20
        self.element = ""
        self.activeCurse = ""
        self.activeShield = ""
        self.activeCards = []
        self.deck = []
        self.hand = []
