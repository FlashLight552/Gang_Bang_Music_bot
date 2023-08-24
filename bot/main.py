import discord
from discord.ext import commands
from discord.utils import get

import os
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix=os.environ['command_prefix'], intents=discord.Intents.all())

@bot.event
async def on_ready():
    os.environ["bot_name"] = str(bot.user.name)
    os.environ["bot_avatar"] = str(bot.user.display_avatar)
    
    print(f'{bot.user} has logged in.')
    
    cogs = os.listdir('cogs')
    for cog in cogs:
        if not cog.startswith('__'):
            await bot.load_extension(f'cogs.{cog}')
    
    print(f'Cogs has loaded.')

    await bot.change_presence(activity=discord.Game('with your pussy ^_^'))

@bot.event
async def on_member_join(member):
    role = get(member.guild.roles, name='Потанцивальные кОбаны')
    await member.add_roles(role)

bot.run(os.environ['discord_token'])