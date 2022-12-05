from .my_help import MyHelpCommand

async def setup(bot):
    # await bot.add_cog(MyHelpCommand(bot))
    bot.help_command = MyHelpCommand()

