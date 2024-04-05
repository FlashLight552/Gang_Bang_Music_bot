import re

import lavalink
from lavalink.server import LoadType
from discord.ext import commands

from ..core.setup import Setup


url_rx = re.compile(r'https?://(?:www\.)?.+')
yt_url_rx = re.compile('(https:\/\/)?(www.|music.|youtu.|m.)?(youtube.com|be)')

class Play(Setup):
    async def search(self,query, player: lavalink, radio=False):
        query = query.strip('<>')

        """Starts radio"""
        if radio:
            """in track name"""
            if not url_rx.match(query):
                query = f'ytsearch:{query}'
                track = await player.node.get_tracks(query)
                id = (track.tracks[0].identifier)
                query = f'https://music.youtube.com/watch?v={id}&list=RDAMVM{id}'
                return await player.node.get_tracks(query)

            """YOUTUBE URL"""
            if yt_url_rx.match(query):
                track = await player.node.get_tracks(query)
                id = (track.tracks[0].identifier)
                query = f'https://music.youtube.com/watch?v={id}&list=RDAMVM{id}'
                return await player.node.get_tracks(query)

            """in track URL"""
            track = await player.node.get_tracks(query)
            title = track.tracks[0].title
            query = f'ytsearch:{title}'
            track = await player.node.get_tracks(query)
            id = (track.tracks[0].identifier)
            query = f'https://music.youtube.com/watch?v={id}&list=RDAMVM{id}'
            return await player.node.get_tracks(query)

        """Starts player in track name"""
        if not url_rx.match(query):
            query = f'ytsearch:{query}'
            return await player.node.get_tracks(query)

        """Starts player in track Url"""
        return await player.node.get_tracks(query)


    @commands.command(aliases=['p','!'], description='Searches and plays a song from a given query')
    async def play(self, ctx: commands.Context, *, query: str, radio = False):
        """ Searches and plays a song from a given query. """
        await ctx.message.delete()
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        results = await self.search(query, player, radio=radio)

        # Valid load_types are:
        #   TRACK    - direct URL to a track
        #   PLAYLIST - direct URL to playlist
        #   SEARCH   - query prefixed with either "ytsearch:" or "scsearch:". This could possibly be expanded with plugins.
        #   EMPTY    - no results for the query (result.tracks will be empty)
        #   ERROR    - the track encountered an exception during loading

        if results.load_type == LoadType.EMPTY:
            await ctx.send("I couldn't find any tracks for that query or something went wrong", delete_after=15)
            if not player.is_playing and not player.queue:
                await self.disconnect(ctx)
                await self.end_play(ctx.guild.id)

        if results.load_type == LoadType.PLAYLIST:
            tracks = results.tracks
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)
        
        if results.load_type == LoadType.TRACK or results.load_type == LoadType.SEARCH:
            track = results.tracks[0]
            player.add(track=track, requester=ctx.author.id)

        if not player.is_playing:
            await player.play()


    @commands.command(aliases=['bp'], description='Adds a track to the front of the queue')
    async def bump(self, ctx:commands.Context, *, query:str):
        await ctx.message.delete()
        
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        results = await self.search(query, player, 1)

        if results.load_type == LoadType.EMPTY:
            await ctx.send("I couldn'\t find any tracks for that query.", delete_after=15)
            if not player.is_playing and not player.queue:
                await self.disconnect(ctx)
                await self.end_play(ctx.guild.id)
        
        queue = list(player.queue)
        queue.insert(0, results.tracks[0])
        
        player.queue.clear()

        for track in queue:
            player.add(requester=ctx.author.id, track=track)

        if not player.is_playing:
            await player.play()


    @commands.command(aliases=['r',], name='radio', description='Starts radio with similar tracks')
    async def radio(self, ctx: commands.Context, *, query: str):
        await self.play(ctx, radio=True, query=query)
