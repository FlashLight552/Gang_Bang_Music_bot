from discord.ext import commands
import re
import os
import asyncio
from lavalink.server import LoadType
import lavalink


from ..core.setup import Setup
from ..core.spotify_api import Spotify_api


url_rx = re.compile(r'https?://(?:www\.)?.+')
sp_url_rx = re.compile("(https?:\/\/)?(www.)?(open.spotify.com\/)?(playlist\/|track\/)")
yt_url_rx = re.compile('(https:\/\/)?(www.|music.|youtu.|m.)?(youtube.com|be)')

class Play(Setup):
    async def search(self,query, player, limit=10, radio=False):
        query = query.strip('<>')
        
        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        if sp_url_rx.match(query):
            sp = Spotify_api(os.environ['sp_cli'], os.environ['sp_cls'])
            query = sp.get_tracks(query,limit)
            if radio:
                await asyncio.sleep(0.5)
                track = await player.node.get_tracks(f'ytsearch:{query[0]}')
                id = (track.tracks[0].identifier)
                query = f'https://music.youtube.com/watch?v={id}&list=RDAMVM{id}'
                return [await player.node.get_tracks(query)]
            else:
                list = []
                for item in query:
                    list.append(await player.node.get_tracks(f'ytsearch:{item}'))
                return list
        
        if radio: 
            if yt_url_rx.match(query):
                id = query.split('watch?v=')[1].split('&')[0]
                query = f'https://music.youtube.com/watch?v={id}&list=RDAMVM{id}'

            
            if not url_rx.match(query):
                track = await player.node.get_tracks(query)
                id= (track.tracks[0].identifier)
                query = f'https://music.youtube.com/watch?v={id}&list=RDAMVM{id}'
        
        
        return await player.node.get_tracks(query)


    @commands.command(aliases=['p','!'], description='Searches and plays a song from a given query')
    async def play(self, ctx: commands.Context, *, query: str, radio = False):
        """ Searches and plays a song from a given query. """
        await ctx.message.delete()
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        results = await self.search(query, player, radio=radio)

        # if not results or not results[0].tracks:
        #     nf_msg = await ctx.send('Nothing found!')
        #     if not player.is_playing and not player.queue:
        #         await self.disconnect(ctx)
        #         # await self.end_play(ctx.guild.id)

        #     return await nf_msg.delete(delay=15)

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL)
        #   PLAYLIST_LOADED - direct URL to playlist)
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.

        if results.load_type == LoadType.EMPTY:
            await ctx.send("I couldn'\t find any tracks for that query.", delete_after=15)
            if not player.is_playing and not player.queue:
                await self.disconnect(ctx)
                await self.end_play(ctx.guild.id)

        if results.load_type == LoadType.PLAYLIST:
            tracks = results.tracks
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)
        
        if results.load_type == LoadType.TRACK:
            track = results.tracks[0]
            player.add(track=track, requester=ctx.author.id)

        if not player.is_playing:
            await player.play()


    @commands.command(aliases=['bp'], description='Adds a track to the front of the queue')
    async def bump(self, ctx:commands.Context, *, query:str):
        await ctx.message.delete()
        
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        results = await self.search(query, player, 1)

        if not results or not results[0].tracks:
            nf_msg = await ctx.send('Nothing found!')
            return await nf_msg.delete(delay=15)
        
        queue = list(player.queue)
        queue.insert(0, results[0].tracks[0])
        
        player.queue.clear()

        for track in queue:
            player.add(requester=ctx.author.id, track=track)

        if not player.is_playing:
            await player.play()


    @commands.command(aliases=['r',], name='radio', description='Starts radio with similar tracks')
    async def radio(self, ctx: commands.Context, *, query: str):
        await self.play(ctx, radio=True, query=query)
