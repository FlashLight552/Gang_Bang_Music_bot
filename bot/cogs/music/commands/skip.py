from discord.ext import commands

from ..core.setup import Setup


class Skip(Setup):
    @commands.command(name='skip', aliases=['s'], description='Skips current track')
    async def skip(self, ctx: commands.Context):
        await self.skip_btn(ctx.guild.id)
        await ctx.message.delete()

    async def skip_btn(self, guild_id, *args):
        player = self.bot.lavalink.player_manager.get(guild_id)
        await player.skip()