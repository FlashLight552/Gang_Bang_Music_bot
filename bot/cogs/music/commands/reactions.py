import discord
from discord.ext import commands

import asyncio
from ..core.setup import Setup


class Reactions(Setup):
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if self.live_player_dict and payload.message_id == self.live_player_dict[payload.guild_id]['msg'].id:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = self.bot.get_user(payload.user_id)
            emoji = payload.emoji


            if not user.bot:
                player = self.bot.lavalink.player_manager.get(payload.guild_id)
                voice_channel = self.bot.get_channel(player.channel_id)
                members = voice_channel.members
                members_id = [] #(list)
                for member in members:
                    members_id.append(member.id)
                
                if payload.user_id in members_id:
                    try:
                        await self.command_list[emoji.name](payload.guild_id)
                        await message.remove_reaction(emoji, user)
                    except:
                        pass
                else: 
                    await message.remove_reaction(emoji, user)

                    msg = await channel.send("You're not in my voicechannel!")
                    await asyncio.sleep(10)
                    await msg.delete()