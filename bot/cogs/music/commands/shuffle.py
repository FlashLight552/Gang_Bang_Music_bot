from ..core.setup import Setup


class Shuffle(Setup):
    async def shuffle(self, guild_id):
        player = self.bot.lavalink.player_manager.get(guild_id)
        player.set_shuffle(not player.shuffle)
        

    async def shuffle_btn(self, guild_id):
        await self.shuffle(guild_id)