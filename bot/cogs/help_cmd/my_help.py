import os
from re import I
import discord
from discord.ext import commands


class MyHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(color=discord.Color.blurple())
        embed.title = f'*{os.environ["bot_name"]} bot*'
        embed.set_thumbnail(url=os.environ["bot_avatar"])
        embed.set_author(name=f'{os.environ["bot_name"]} Help Menu', icon_url=os.environ["bot_avatar"])
        for cog, cmds in mapping.items():
            if cog:
                embed.add_field(
                    name = cog.qualified_name,
                    value = "\n".join([f'**{cmd.name}** `{cmd.aliases or "no aliases"}` *{cmd.description or "no description"}*' for cmd in cmds]),
                    inline=False 
                )

        channel = self.get_destination()  # this method is inherited from `HelpCommand`, and gets the channel in context
        await channel.send(embed=embed)