from discord.ext import commands

from ..core.setup import Setup


class Pause(Setup):
    @commands.command(name='pause', description='Play/Pause', aliases=['pp'])
    async def pause(self,ctx: commands.Context):
        await self.pause_btn(ctx.guild.id)
        await ctx.message.delete()
    
    async def pause_btn(self, guild_id, *args):
        player = self.bot.lavalink.player_manager.get(guild_id)
        status = player.paused
        await player.set_pause(not status)