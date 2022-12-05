import asyncio
import shutil

from discord.ext import commands


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.tack_inactive = None


    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        pass

    async def cog_before_invoke(self, ctx: commands.Context):
        """ Command before-invoke handler. """
        pass

    async def cog_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

    async def cog_after_invoke(self, ctx: commands.Context):
        if not self.tack_inactive:
            self.tack_inactive = asyncio.create_task(self.inactive_disconnect(ctx))
        else:
            self.tack_inactive.cancel()
            self.tack_inactive = asyncio.create_task(self.inactive_disconnect(ctx))

    async def inactive_disconnect(self ,ctx):
        await asyncio.sleep(60)
        await ctx.voice_client.disconnect()
        dir_path = f'cogs/tts/{ctx.guild.id}'
        shutil.rmtree(dir_path)


    async def ensure_voice(self, ctx: commands.Context):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        should_connect = ctx.command.name in ('say',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('Join a voicechannel first.')

        v_client = ctx.voice_client
        if not v_client:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

            self.voice = await ctx.author.voice.channel.connect()

        else:
            if v_client.channel.id != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voicechannel.')