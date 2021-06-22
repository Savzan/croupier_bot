"""
Author : Sawsen
CARDS AND GAMES
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Choix de l'atlas des cartes
base_deck_style = 'deck.png'

class Player:
    def __init__(self, name):
        self.cards = []
        self.jeton = 250
        self.pseudo = name

#Define the motif of the way the atlas and deck is composed
class Atlas:
    def __init__(self, row, col, path):
        self.row = row
        self.col = col
        self.path = path
        self.image = Image.open(path)

# Definition des paramètres des decks
class Decks:
    def __init__(self, nb, decalage):
        self.nb = nb
        self.offset = decalage
        self.motif = Atlas(4, 13, base_deck_style)
        self.pool = []
    
    def picture_def(self, row, col, path):
        self.motif = Atlas(row, col, path)
    
    #Modify the style for the cards
    def change_picture(self, path):
        self.motif.image = Image.open(path)
        
    #Change atlas format
    def modify_atlas(self, row, col, path):
        self.motif = Atlas(row, col, path)
    
    #Print the selected card
    def draw(self, i):
        #Log error when the card index is out of range
        if i > self.nb :
            return print('erreur in cards number')
        
        #Apply a correction when there is an offset on the atlas
        cor = 0
        if self.offset != 0 :
            cor = 1
        
        # Caractéristiques des atlas
        length = self.motif.image.size[0]
        height = self.motif.image.size[1]
        
        
        # Definitions des coins haut gauche et bas droit de chaque carte 
        x_index = (i % (self.motif.col - self.offset) + self.offset + cor) % self.motif.col
        x = x_index * np.floor(length / self.motif.col)
        x2 =(x_index + 1) * np.floor(length / self.motif.col)
        
        y_index = np.floor(i/(self.nb/self.motif.row))
        y = y_index *  np.floor(height/self.motif.row)
        y2 = (y_index+1) * np.floor(height/self.motif.row)
        
        box = (x,y, x2, y2)
        
        return self.motif.image.crop(box)
    
    #Fill a temp pool to only retrieve cards you want
    def fill_pool(self, first, last):
        i = first
        while i < last :
            self.pool.append(i)
            i += 1
      
    #Preset for specialized pools
    def heart_pool(self):
        self.fill_pool(0, 13)
    def diamond_pool(self):
        self.fill_pool(13, 26)
    def club_pool(self):
        self.fill_pool(26, 39)
    def spade_pool(self):
        self.fill_pool(39, 52)
    def tarot_pool(self):
        self.fill_pool(0, 22)
    #Erase the current pool
    def empty_pool(self):
        self.pool = []
    
    
# Print X cards merging their pictures       
def concatcards(src, dst, number) :
    temp = Image.new('RGBA',(number * dst.size[0], dst.size[1]), (250,250,250, 0))
    temp.paste(src, (0,0))
    temp.paste(dst, (src.size[0], 0))

    return temp


def showcard(img):
    #log    
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.imshow(img)
    plt.show()
    return

# Define if the game use 52 or 32 cards
deck_size = "high"

if deck_size == "high" :
    deck = Decks(52, 0)
    deck.fill_pool(0, 52)
    
if deck_size == "low" :
    deck = Decks(32, 5)
    deck.fill_pool(0, 32)
    
if deck_size == 'tarot' :
    deck = Decks(22, 0)
    deck.modify_atlas(2, 11, "tarot.png")
    deck.tarot_pool()



#POKER GAME
class Poker:
    def __init__(self):
        #Decks stats
        self.deck = Decks(52 , 0)
        self.deck.fill_pool(0, 52)
        
        #Game stats
        self.players = []
        self.pot = 0
        self.river = []
        self.river_img = Image.new('RGBA', (1,1), (250,250,250,0))
                
    def reset(self):
        self.deck.pool = []
        self.deck.fill_pool(0,52)
        self.pot = 0
        self.river = []
        self.river_img = Image.new('RGBA', (1,1), (250,250,250,0))
        return

    def draw(self):
        # Draw one random card and remove it from the pool
        elem = np.random.randint(0, len(self.deck.pool))
        self.deck.pool.pop(elem)
        
        #Return the ID of the card in a classic deck
        return elem
    
    #Add a new card on the board, 
    #flop, turn and river
    def flop(self):
        
        #No more cards in the river
        if len(self.river) > 4:
            return
        
        #Select a card and add it to the river
        card_id = self.draw()
        self.river.append(card_id)
        
        #Add the card images to the precedent
        if len(self.river) == 1:
            self.river_img = deck.draw(card_id)
        
        if len(self.river) > 1 :
            self.river_img = concatcards(self.river_img, deck.draw(card_id), len(self.river))
            
        
        # log
        showcard(self.river_img)
        #Create the river file that is sent to the server
        self.river_img.save("river.png", format = "png")
        return
    
    #Add a player to the game
    def player_draw(self, name):
        
        new_player = Player(name)
        
        new_player.cards.append(self.draw())
        new_player.cards.append(self.draw())
        
        #Build the hand and send it to the player
        hand = concatcards(deck.draw(new_player.cards[0]), deck.draw(new_player.cards[1]) , 2)
        
        showcard(hand)
        hand.save("temp.png", format = "png")
        
        #Add the player to the list
        self.players.append(new_player)
        return
        
class QuietYear:
    def __init__(self):
        #Decks stats
        self.deck = Decks(52 , 0)
        self.season = 1
        
        self.deck.heart_pool()
        print('Spring is here')
       
    #Change the season
    def season_change(self):
        self.season += 1
        if self.season == 2:
            print('Summer is here')
            self.deck.empty_pool()
            self.deck.diamond_pool()
        if self.season == 3:
            print('Fall is here')
            self.deck.empty_pool()
            self.deck.club_pool()
        if self.season == 4:
            print('Winter is here')
            self.deck.empty_pool()
            self.deck.spade_pool()
    def draw(self):
        # Draw one random card and remove it from the pool
        elem = np.random.randint(0, len(self.deck.pool))
        showcard(deck.draw(self.deck.pool[elem]))
        
        #Remove it from the pool
        self.deck.pool.pop(elem)
        return 


text = open('quiet.txt', 'r')
lines = text.readlines()

print(lines[3])


    