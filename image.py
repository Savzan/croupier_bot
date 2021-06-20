# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Choix de l'atlas des cartes
base_deck_style = 'deck2.png'


# Definition des paramètres des decks
class Decks:
    def __init__(self, nb, div, decalage):
            self.cards = nb
            self.div_rows = div
            self.offset = decalage
            self.row = self.cards / 4
            self.image = Image.open(base_deck_style)
            self.pool = []
    
    #Modify the style for the cards
    def change_picture(self, path):
        self.image = Image.open(path)
    
    #Print the selected card
    def draw(self, i):
        if i > self.cards :
            return print('erreur in cards number')
        # Caractéristiques des atlas
        length = self.image.size[0]
        height = self.image.size[1]
        
        # Definitions des coins haut gauche et bas droit de chaque carte 
        x = ((i%self.div_rows + self.offset) %13) * np.floor(length/13)
        x2 =((i%self.div_rows + self.offset) %13 + 1) * np.floor(length/13)
        y = np.floor(i/self.row) *  np.floor(height/4)
        y2 = (np.floor(i/self.row)+1) * np.floor(height/4)
        box = (x,y, x2, y2)
       
        # Edition de l'image atlas
        part = self.image.crop(box)
        
        # Log 
        plt.imshow(part)
        plt.show()
        return
    
    #Fill a temp pool to only retrieve cards you want
    def fill_pool(self, first, last):
        i = first
        while i < last :
            self.pool.append(i)
            i += 1
        


# Define if the game use 52 or 32 cards
deck_size = "high"

if deck_size == "high" :
    deck = Decks(52, 13, 0)
    
if deck_size == "low" :
    deck = Decks(32, 8, 6)


deck.fill_pool(0, 13)

while len(deck.pool):
    elem = np.random.randint(0, len(deck.pool))
    deck.draw(deck.pool[elem])
    deck.pool.pop(elem)
    

        
    
    
    