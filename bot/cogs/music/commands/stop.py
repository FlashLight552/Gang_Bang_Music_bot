from discord.ext import commands

from ..core.setup import Setup


class Stop(Setup):
    # @commands.command(name='stop', description='Stops and disconnects a player from the voice channel' , aliases=['st'])
    # async def stop(self, ctx: commands.Context):
    #     await self.stop_btn()
    #     await ctx.message.delete()

    async def stop_btn(self, guild_id):
        # player = self.bot.lavalink.player_manager.get(guild_id)
        # await player.remove_filter(Timescale)
        await self.disconnect(self.live_player_dict[guild_id]['ctx'])
        await self.end_play(guild_id)