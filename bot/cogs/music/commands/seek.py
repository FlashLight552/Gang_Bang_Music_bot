from ..core.setup import Setup


class Seek(Setup):
    async def seek(self, guild_id, time:int):
        player = self.bot.lavalink.player_manager.get(guild_id)
        await player.seek(player.position + time*1000)

    async def fast_forward(self, guild_id, *args):
        await self.seek(guild_id, 15)

    async def rewind(self, guild_id, *args):
        await self.seek(guild_id, -15)