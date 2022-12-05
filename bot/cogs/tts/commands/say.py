import asyncio
import os

import discord
from discord.ext import commands

from ..core.setup import Setup
from ..core.tts_amazon import TTSVoiceAmazon

class TextToSpeech(Setup):
    def __init__(self, bot):
        super().__init__(bot)


    @commands.command(name='say')
    async def say(self, ctx:commands.Context, *, text:str):
        await ctx.message.delete()
        
        dir_path = f'cogs/tts/{ctx.guild.id}' # create dir for mp3 
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        await self.ensure_voice(ctx) # join to vc

        tts = TTSVoiceAmazon() # TTS
        await tts.text_to_voice(text)
        mp3 = await tts.save(dir_path)

        while self.voice.is_playing(): # if true, waiting for queue
            await asyncio.sleep(1)
        
        source = discord.FFmpegPCMAudio(mp3['path']+ mp3['name'])
        self.voice.play(source) # playing sinteze text
        





    

    