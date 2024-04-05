from discord.ext import commands
from lavalink import Timescale, DefaultPlayer, Vibrato

from ..core.setup import Setup



class Nightcore(Setup):
    @commands.command(name='nightcore', description='Turns on/off nightcore filter for the track', aliases=['nc'])
    async def nightcore(self, ctx:commands.Context):
        await self.nightcore_btn(ctx.guild.id)
        await ctx.message.delete()

    async def nightcore_btn(self, guild_id, *args):
        player: DefaultPlayer = self.bot.lavalink.player_manager.get(guild_id)
        if player.get_filter(Timescale):
            await player.clear_filters()
        else:
            await player.update_filter(Timescale, speed=1.1, pitch=1.2)
        
    async def slowed_and_reverb(self, guild_id, *args):
        player: DefaultPlayer = self.bot.lavalink.player_manager.get(guild_id)
        if player.get_filter(Timescale):
            await player.clear_filters()
        else:
            await player.update_filter(Timescale, speed=0.95, pitch=0.9)
            await player.update_filter(Vibrato, frequency=0.8, depth=0.4)
        

            

