from discord.ext import commands
import re
import os
import asyncio

from ..core.setup import Setup
from ..core.spotify_api import Spotify_api


url_rx = re.compile(r'https?://(?:www\.)?.+')
sp_url_rx = re.compile("(https?:\/\/)?(www.)?(open.spotify.com\/)?(playlist\/|track\/)")

class Play(Setup):
    async def search(self,query, player, limit=10):
        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'
        
        if sp_url_rx.match(query):
            sp = Spotify_api(os.environ['sp_cli'], os.environ['sp_cls'])
            query = sp.get_tracks(query,limit)
            list = []
            for item in query:
                list.append(await player.node.get_tracks(f'ytsearch:{item}'))
            return list
        
        
        return [await player.node.get_tracks(query)]


    @commands.command(aliases=['p', '!'], description='Searches and plays a song from a given query')
    async def play(self, ctx: commands.Context, *, query: str):
        """ Searches and plays a song from a given query. """
        await ctx.message.delete()
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        results = await self.search(query, player)
        
        if not results or not results[0].tracks:
            nf_msg = await ctx.send('Nothing found!')
            if not player.is_playing and not player.queue:
                await self.disconnect(ctx)

            await asyncio.sleep(15)
            return await nf_msg.delete()

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL)
        #   PLAYLIST_LOADED - direct URL to playlist)
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
        

        if results[0].load_type == 'PLAYLIST_LOADED':
            tracks = results[0].tracks
            
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)
        else:
            for i in range(len(results)):
                result = results[i]
                player.add(requester=ctx.author.id, track=result.tracks[0])

        if not player.is_playing:
            await player.play()


    @commands.command(aliases=['bp'], description='Adds a track to the front of the queue')
    async def bump(self, ctx:commands.Context, *, query:str):
        await ctx.message.delete()
        
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        results = await self.search(query, player, 1)

        if not results or not results[0].tracks:
            nf_msg = await ctx.send('Nothing found!')
            await asyncio.sleep(15)
            return await nf_msg.delete()
        
        queue = list(player.queue)
        queue.insert(0, results[0].tracks[0])
        
        player.queue.clear()

        for track in queue:
            player.add(requester=ctx.author.id, track=track)

        if not player.is_playing:
            await player.play()
