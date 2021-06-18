# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 20:07:12 2021

@author: Sawsen
"""

import discord
from discord.ext import commands
import logging

## Enable logging in the command for the discord bot
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = commands.Bot(command_prefix='')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run('ODU1MTU4MjIzMTE5NTgxMTk0.YMuaKA.74Ha5MQIw6Pfup-VUA2E4L6dWiU')