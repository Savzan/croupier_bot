# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 20:07:12 2021

@author: Sawsen
"""

import discord
from discord.ext import commands


import logging

#cd .\dev\test_python_bot\
#py -3 test_bot_discord.py


## Enable logging in the command for the discord bot
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = commands.Bot(command_prefix='!')

@bot.command(name = 'poker', help = 'test')
async def ping(ctx):
    await ctx.send(file=discord.File('temp.png'))
    
    
text = open('token', 'r')
lines = text.readlines()
bot.run(lines[0])