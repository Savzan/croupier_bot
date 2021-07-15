# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 20:07:12 2021

@author: Sawsen
"""

import discord
from discord.ext import commands
from cards import Poker

import logging

#cd .\dev\test_python_bot\
#py -3 test_bot_discord.py

client = discord.Client()

poker = Poker()

## Enable logging in the command for the discord bot
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = commands.Bot(command_prefix='$')
#CLIENT REQUESTS
#Log the number of servers the bot is connected to
@client.command(name = 'poker', help = 'Launch a game of poker')
async def begin_poker_play(ctx):
    poker = Poker()


#BOT COMMANDS
#Draw the card for each player in the game and send them as private message
@bot.command(name = 'poker', help = 'test')
async def draw_player_cards(ctx):
    await ctx.send(file=discord.File('temp.png'))
 

#Send the flop up to the river directly to the server
@bot.command(name = 'river')
async def show_river(ctx):
    while len(poker.river) < 3:
        poker.flop()  
    await ctx.send(file=discord.File('river.png'))



token_file = open('token', 'r')
token = token_file.readlines()[0]

bot.run(token)
client.run(token)