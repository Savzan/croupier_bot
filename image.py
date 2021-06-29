"""
Author : Sawsen
CARDS AND GAMES
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter

# Choix de l'atlas des cartes
base_deck_style = 'deck.png'

class Player:
    def __init__(self, name):
        self.cards = []
        self.jeton = 250
        self.pseudo = name
        self.score = '0'

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


#%% POKER GAME
class Poker:
    def __init__(self):
        #Decks stats
        self.deck = Decks(52 , 0)
        self.deck.fill_pool(0, 52)
        
        #Game stats
        self.__players = []
        self.pot = 0
        self.river = []
        self.river_img = Image.new('RGBA', (1,1), (250,250,250,0))
        
        #Game Constant 
        # Quinte, Color, Square, Brelan, Pair, High
        self.__str_score = 'Q0 C0 S0 Sq0 B0 P000 H0'
        self.__value = ['d', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c']
                
    def reset(self):
        self.deck.pool = []
        self.deck.fill_pool(0,52)
        self.pot = 0
        self.river = []
        self.river_img = Image.new('RGBA', (1,1), (250,250,250,0))
        return

    def __draw(self):
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
        card_id = self.__draw()
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
        
        new_player.cards.append(self.__draw())
        new_player.cards.append(self.__draw())
        
        #Build the hand and send it to the player
        hand = concatcards(deck.draw(new_player.cards[0]), deck.draw(new_player.cards[1]) , 2)
        
        showcard(hand)
        hand.save("temp.png", format = "png")
        
        #Add the player to the list
        self.__players.append(new_player)
        return

    
    def __score_check(self, player):

        score = list(self.__str_score)
        
        temp = []
        temp.extend(player.cards)
        temp.extend(self.river)
        temp.sort()
        
        #Check for color
        h, d, s, c = [],[],[],[]
        
        for card in temp :
            if card < 13 :
                h.append(card)
            if card > 12  and card < 26 :
                d.append(card)
            if card > 25 and card < 39 :
                c.append(card)
            if card > 38 :
                s.append(card)
        
        color = []   
        #Create a temp array holder to determine if there is a color    
        col = []
        col.append(h)
        col.append(d)
        col.append(c)
        col.append(s)
        
        i = 0
        #Check for the longest list of the 4 for the quinte check
        while i < len(col):
            if len(col[i]) > 4 :
                color = col[i]
                if color[0] == 0 :
                    score[4] = self.__value[0]
                    break
                score[4] = self.__value[color[-1]%13]    
            i += 1
        
        
        #check for best value pair, triple, square on the board
        
        c = Counter(np.mod(temp, 13))
        print(c)
        #card number
        print(list(c.keys()))
        #number of iterations
        print(list(c.values()))
        
        i = 0
        while i < len(list(c)):
            if list(c.values())[i] == 2 :
                #Select best pair
                if score[17] == 0 :
                    score[17] = self.__value[list(c.keys())[i]]
                
                if self.__value[list(c.keys())[i]] > score[17] :
                    score[18] = score[17]
                    score[17] = self.__value[list(c.keys())[i]]
                
                if  self.__value[list(c.keys())[i]] < score[17] and self.__value[list(c.keys())[i]] > 18 :
                    score[18] = self.__value[list(c.keys())[i]] < score[17]
            
                
            if list(c.values())[i] == 3 :
                #Brelan score
                score[14] = self.__value[list(c.keys())[i]]
                
            if list(c.values())[i] == 4 :
                #Square score
                score[11] = self.__value[list(c.keys())[i]]
                
            i += 1
        
        #highest on hand
        high_hand = Counter(np.mod(player.cards, 13))
        if (list(high_hand.values())[0] > 1) and (score[18] != list(high_hand.keys())[0]):
            score[19] = self.__value[list(Counter(high_hand).keys())[-1]]
        
        score[22] = self.__value[list(high_hand.keys())[-1]]
        print(list(high_hand.keys()))
        if list(high_hand)[0] == 0 :
            score[22] = self.__value[0]
            
        
        #check for straight
        c = list(c)
        straight = []
        
        if len(c) > 4 :
            i = 0
            while i < len(c) - 4 :
                if c[i + 4]%13 == (c[i] + 4)%13:
                    score[7] = self.__value[c[i+4]%13] 
                    j = 0
                    while j < 5 :
                        straight.append(c[i+j])
                        j += 1
                
                #Test while the first card is an Ace
                if c[i] == 0:
                    #Test for the wheel straight that can only be beaten by the broadway
                    if c[i + 4]%13 == 4:
                        score[7] = self.__value[0] 
                        j = 0
                        while j < 5 :
                            straight.append(c[i+j])
                            j += 1
                        
                    #Test for the broadway straight 
                    if c[-4]%13 == 9 :
                        score[7] = 'e'
                        
                        j = 0
                        while j > -4 :
                            straight.append(c[i+j])
                            j -= 1
                    break
                i += 1
        
        
        #Check for quinte 
        a = set(color)
        b = set(straight)
        
        
        if (a.issubset(b) or b.issubset(a)) and ((len(a) and len(b)) > 4):
            score[1] = self.__value[straight[-1]%13]
            if straight[0] == 0 :
                score[1] = self.__value[0]    
        
        
        #SCORE
        str_score = ''.join(score)
        
        player.score = str_score
        print('score : ' + str_score)
        return 
    
    def winner_check(self):
        #Select the winner of the game
        winner = Player('')
        for player in self.__players :
            self.__score_check(player)
            if player.score > winner.score :
                winner = player
        return winner



poker = Poker()
print('Bob hand :')
poker.player_draw('Bob')
print('Alice hand :')
poker.player_draw('Alice')

poker.flop()
poker.flop()
poker.flop()
poker.flop()
poker.flop()

print(poker.winner_check().pseudo)


#%% Quiet Year program
    
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
