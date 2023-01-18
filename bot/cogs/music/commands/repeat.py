from ..core.setup import Setup


class Repeat(Setup):
    async def repeat(self, guild_id):
        player = self.bot.lavalink.player_manager.get(guild_id)
        if player.loop < 2:
            player.set_loop(player.loop + 1)
        
        else:
            player.set_loop(0)
        

    async def repeat_btn(self, guild_id):
        await self.repeat(guild_id)

