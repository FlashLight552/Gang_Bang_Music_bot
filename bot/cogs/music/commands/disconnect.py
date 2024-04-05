import discord
from discord.ext import commands
from ..core.setup import Setup



class Disconnect(Setup):
    @commands.command(aliases=['dc'], description='Disconnects the player from the voice channel')
    async def disconnect(self, ctx: commands.Context, without_user = False):

        try:
            await ctx.message.delete()
        except discord.errors.NotFound:
            pass

        if without_user == False:
            if not ctx.voice_client:
                return await ctx.send('Not connected.')

        try:
            await ctx.voice_client.disconnect(force=True)
        except:pass
