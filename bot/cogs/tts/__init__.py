from .commands.say import TextToSpeech

async def setup(bot):
    await bot.add_cog(TextToSpeech(bot))