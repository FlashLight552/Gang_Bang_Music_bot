from discord.ext import commands
from ..core.setup import Setup



class Disconnect(Setup):
    @commands.command(aliases=['dc'], description='Disconnects the player from the voice channel')
    async def disconnect(self, ctx: commands.Context):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not ctx.voice_client:
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voicechannel!')

        player.queue.clear()
        player.set_shuffle(False)
        player.set_loop(0)

        await player.stop()
        await ctx.voice_client.disconnect(force=True)