from discord.ext import commands
from lavalink import Timescale

from ..core.setup import Setup


class Nightcore(Setup):
    @commands.command(name='nightcore', description='Turns on/off nightcore filter for the track', aliases=['nc'])
    async def nightcore(self, ctx:commands.Context):
        await self.nightcore_btn(ctx.guild.id)
        await ctx.message.delete()

    async def nightcore_btn(self, guild_id, *args):
        player = self.bot.lavalink.player_manager.get(guild_id)
        if player.get_filter(Timescale):
            await player.remove_filter(Timescale)
        else:
            await player.update_filter(Timescale, speed=1.1, pitch=1.2)
        
