import discord
from discord.ext import commands

import asyncio
import time
import os

import lavalink
from .LavalinkVoiceClient import LavalinkVoiceClient
from lavalink import Timescale, Equalizer, Tremolo, Vibrato


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # This ensures the client isn't overwritten during cog reloads.
        if not hasattr(bot, 'lavalink'):
            bot.lavalink = lavalink.Client(bot.user.id)
            # Host, Port, Password, Region, Name
            bot.lavalink.add_node(
                os.environ['lavalink_ip'], os.environ['lavalink_port'], os.environ['lavalink_pass'], 'ua', 'default-node')

        lavalink.add_event_hook(self.track_hook)

        self.live_player_dict: dict = {}
        self.command_list = {
            '⏪': self.rewind,
            '⏯️': self.pause_btn,
            '⏹️': self.stop_btn,
            '⏩': self.fast_forward,
            '⏭️': self.skip_btn,
            '🔁': self.repeat_btn,
            '🔀': self.shuffle_btn,
            '💜': self.nightcore_btn,
            '💙': self.slowed_and_reverb,
        }

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx: commands.Context):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None

        if guild_check:
            await self.ensure_voice(ctx)

        return guild_check

    async def cog_after_invoke(self, ctx: commands.Context):
        if ctx.guild.id not in self.live_player_dict:
            self.live_player_dict[ctx.guild.id] = {}
            await self.live_player(ctx)

    async def convert_millis(self, millis):
        seconds = int((millis/1000) % 60)
        minutes = int((millis/(1000*60)) % 60)
        hours = int((millis/(1000*60*60)) % 24)
        return {'seconds': seconds, 'minutes': minutes, 'hours': hours}

    async def cog_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandInvokeError):
            msg = await ctx.send(error.original)
            await asyncio.sleep(15)
            try:
                await msg.delete()
            except:
                pass

    async def ensure_voice(self, ctx: commands.Context):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id)
        should_connect = ctx.command.name in ('play', 'bump',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('Join a voicechannel first.')

        v_client = ctx.voice_client
        if not v_client:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError(
                    'I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await ctx.author.voice.channel.connect(cls=LavalinkVoiceClient)
        else:
            if v_client.channel.id != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError(
                    'You need to be in my voicechannel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = event.player.guild_id
            guild = self.bot.get_guild(guild_id)
            await guild.voice_client.disconnect(force=True)
            await self.end_play(guild_id)

    async def end_play(self, guild_id):
        player = self.bot.lavalink.player_manager.get(guild_id)
        player.queue.clear()
        player.set_shuffle(False)
        player.set_loop(0)
        await player.remove_filter(Timescale)
        try:
            await player.remove_filter(Vibrato)
        except: pass

        await self.live_player_dict[guild_id]['msg'].delete()
        del self.live_player_dict[guild_id]

    async def live_player(self, ctx: commands.Context):
        timeout = 0
        while True:
            player = self.bot.lavalink.player_manager.get(ctx.guild.id)
            try:
                duration = player.current.duration
                position = player.position
                track = player.current
                loop = player.loop
                shuffle = player.shuffle
            except:
                break
            
            """Disconnects if not users in vs"""
            users = []
            voice_channel = self.bot.get_channel(player.channel_id)
            members = voice_channel.members
            for item in members:
                if item.bot == False:
                    users.append(item)
            
            if not users:
                timeout += 1
                # print(f'{ctx.guild} - {timeout}')
                if  timeout == 30:
                    await self.disconnect(ctx, without_user=True)
                    await self.end_play(ctx.guild.id)
                    break
            else:
                timeout = 0

            """Creates live player embed"""
            progress_bar = '▶️'
            parts = duration/12
            for i in range(0, 12):
                if position > parts*(i) and position < parts*(i+1):
                    progress_bar += ('━'*i) + '🔘' + '━' * (12-i)

            dur_hs = await self.convert_millis(duration)

            if dur_hs['hours'] != 0:
                track_duration = time.strftime(
                    '%H:%M:%S', time.gmtime(duration/1000))
                track_current_position = time.strftime(
                    '%H:%M:%S', time.gmtime(position/1000))
            else:
                track_duration = time.strftime(
                    '%M:%S', time.gmtime(duration/1000))
                track_current_position = time.strftime(
                    '%M:%S', time.gmtime(position/1000))

            loop_status = {0: '❌', 1:'single ✅', 2:'queue ✅'}
            shuffle_status = {False:'❌', True:'✅'}
            progress_bar += f" `{track_current_position}`/`{track_duration}`\n\n"\
                        f"*Repeat: {loop_status[loop]}* | "\
                        f"*Shuffle:* {shuffle_status[shuffle]}"
            
            yt_thumbnail = f'https://img.youtube.com/vi/{track.identifier}/maxresdefault.jpg'
            title, description = await self.queue(ctx.guild.id)

            embed = discord.Embed(color=discord.Color.blurple())
            embed.title = '🎸🤘​ Playing now  ​​🔉​🎶​'
            embed.description = f'[{track.title}]({track.uri})\n\n{progress_bar}'
            embed.set_author(
                name=f'{os.environ["bot_name"]} Player', icon_url=os.environ["bot_avatar"])
            embed.set_thumbnail(url=yt_thumbnail)
            embed.add_field(name=title, value=description)

            if 'msg' not in locals():
                msg = await ctx.send(embed=embed)
                self.live_player_dict[ctx.guild.id] = {'msg': msg, 'ctx': ctx}
                for item in self.command_list.keys():
                    await asyncio.sleep(0.1)
                    await msg.add_reaction(item)
            else:
                try:
                    await msg.edit(embed=embed)
                except:
                    if not player.current:
                        break
                    msg = await ctx.send(embed=embed)
                    self.live_player_dict[ctx.guild.id] = {
                        'msg': msg, 'ctx': ctx}
                    for item in self.command_list.keys():
                        await asyncio.sleep(0.1)
                        try:
                            await msg.add_reaction(item)
                        except: pass
            await asyncio.sleep(3)
