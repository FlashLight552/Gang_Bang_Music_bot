from discord.ext import commands
from lavalink import Timescale, Equalizer, DefaultPlayer, Tremolo, Vibrato

from ..core.setup import Setup



class Nightcore(Setup):
    @commands.command(name='nightcore', description='Turns on/off nightcore filter for the track', aliases=['nc'])
    async def nightcore(self, ctx:commands.Context):
        await self.nightcore_btn(ctx.guild.id)
        await ctx.message.delete()

    async def nightcore_btn(self, guild_id, *args):
        player = self.bot.lavalink.player_manager.get(guild_id)
        if player.get_filter(Timescale) or player.get_filter(Vibrato):
            await player.remove_filter(Timescale, Vibrato)
        else:
            await player.update_filter(Timescale, speed=1.1, pitch=1.2)
        
    async def slowed_and_reverb(self, guild_id, *args):
        player: DefaultPlayer = self.bot.lavalink.player_manager.get(guild_id)
        if player.get_filter(Timescale) or player.get_filter(Vibrato):
            await player.remove_filter(Timescale, Vibrato)
        else:
            await player.update_filter(Timescale, speed=0.95, pitch=0.9)
            await player.update_filter(Vibrato, frequency=0.8, depth=0.4)
            
            # await player.update_filter(Equalizer, bands = [(0, 0.1),(1,0.1)])
            # await player.update_filter(Tremolo, frequency=1, depth=0.8)
        

            

