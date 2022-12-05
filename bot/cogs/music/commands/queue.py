from ..core.setup import Setup


class Queue(Setup):
    async def queue(self, guild_id):
        player = self.bot.lavalink.player_manager.get(guild_id)
        queue = player.queue
        msg = ''

        for i in range(len(queue)):
            if len(msg) <= 800:
                msg += f'**{i+1}.** [{queue[i].title}]({queue[i].uri})\n'
                embed_queue = i + 1
            else: 
                break
            
        if not msg:
            msg = "*It's empty now*"
        
        if 'embed_queue' in locals():
            title = f'Playlist {embed_queue}/{len(queue)}\n'
        else:
            title = f'Playlist \n'

        return title, msg