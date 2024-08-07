import discord
from discord.ext import commands

import asyncio
import time
import os

import lavalink

from .LavalinkVoiceClient import LavalinkVoiceClient
from lavalink.events import QueueEndEvent
from .lavalink_server_parser import lavalink_server_parser

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_list = lavalink_server_parser()

        # This ensures the client isn't overwritten during cog reloads.
        if not hasattr(bot, 'lavalink'):
            bot.lavalink = lavalink.Client(bot.user.id)
            
            # Host, Port, Password, Region, Name
            
            # for item in (self.server_list):
            #     bot.lavalink.add_node(
            #         self.server_list[item]['host'],
            #         self.server_list[item]['port'],
            #         self.server_list[item]['password'],
            #         'Ukraine',
            #         self.server_list[item]['host'])

        
            bot.lavalink.add_node(
                os.environ['lavalink_ip'],
                os.environ['lavalink_port'], 
                os.environ['lavalink_pass'], 
                'Ukraine',
                'Main-Node')
    
        self.lavalink: lavalink.Client = bot.lavalink
        self.lavalink.add_event_hooks(self)

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
            player = self.bot.lavalink.player_manager.get(ctx.guild.id)
            if player.is_playing or player.queue:
                try:
                    self.live_player_dict[ctx.guild.id]
                except KeyError:
                    self.live_player_dict[ctx.guild.id] = {}
                    await self.live_player(ctx)
                    

    async def convert_millis(self, millis):
        seconds = int((millis/1000) % 60)
        minutes = int((millis/(1000*60)) % 60)
        hours = int((millis/(1000*60*60)) % 24)
        return {'seconds': seconds, 'minutes': minutes, 'hours': hours}

    async def cog_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original, delete_after= 15)

            player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id) 
            if not player.is_playing and not player.queue:
                
                    await self.disconnect(ctx, without_user=True)
                    await self.end_play(ctx.guild.id)
            
    async def ensure_voice(self, ctx: commands.Context):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = ctx.bot.lavalink.player_manager.create(ctx.guild.id)
        should_connect = ctx.command.name in ('play', 'bump', 'radio', )

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

    @lavalink.listener(QueueEndEvent)
    async def track_hook(self, event: QueueEndEvent):
        guild_id = event.player.guild_id
        guild = self.bot.get_guild(guild_id)

        if guild is not None:
            await guild.voice_client.disconnect(force=True)
            await self.end_play(guild_id)

    async def end_play(self, guild_id):
        await self.lavalink.player_manager.destroy(guild_id)
        """Deletes live player message"""   
        try:
            await self.live_player_dict[guild_id]['msg'].delete() 
        except: pass
        """Deletes live player data from list"""
        try:
            del self.live_player_dict[guild_id]
        except: pass

    async def live_player(self, ctx: commands.Context):
        while True:
            player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
            
            try:
                duration = player.current.duration
                position = player.position
                track = player.current
                loop = player.loop
                shuffle = player.shuffle
            except:
                await self.disconnect(ctx, without_user=True)
                await self.end_play(ctx.guild.id)
                break
            
            """Disconnects if not users in vc"""
            if await self.dc_if_not_users(ctx, player):
                break

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

            """Creates or edits live player message"""
            if 'msg' not in locals():
                msg = await ctx.send(embed=embed)
                self.live_player_dict[ctx.guild.id] = {'msg': msg, 'ctx': ctx}
                
                for item in self.command_list.keys():
                    try:
                        await asyncio.sleep(0.15)
                        await msg.add_reaction(item)
                    except discord.errors.NotFound:
                        break
            else:
                try:
                    if self.live_player_dict[ctx.guild.id]['msg'] == msg:
                        await msg.edit(embed=embed) 
                except:
                    if not player.current:
                        break
                    msg = await ctx.send(embed=embed)
                    self.live_player_dict[ctx.guild.id] = {
                        'msg': msg, 'ctx': ctx}
                    for item in self.command_list.keys():
                        try:
                            await asyncio.sleep(0.15)
                            await msg.add_reaction(item)
                        except discord.errors.NotFound:
                            break
            
            await asyncio.sleep(3)

    async def dc_if_not_users(self, ctx: commands.Context, player):
            try:
                users = []
                voice_channel = self.bot.get_channel(player.channel_id)
                members = voice_channel.members
                for item in members:
                    if item.bot == False:
                        users.append(item)
                
                if not users:
                        await self.disconnect(ctx, without_user=True)
                        await self.end_play(ctx.guild.id)
                        return True
            except:
                await self.disconnect(ctx, without_user=True)
                await self.end_play(ctx.guild.id)
                return True