from .commands.disconnect import Disconnect
from .commands.pause import Pause
from .commands.play import Play
from .commands.queue import Queue
from .commands.reactions import Reactions
from .commands.seek import Seek
from .commands.skip import Skip
from .commands.stop import Stop
from .commands.nightcore import Nightcore

class MusicPlayer(Disconnect, Pause, Play, Queue, Reactions, Seek, Skip, Stop, Nightcore):
    def __init__(self, bot):
        super().__init__(bot)

async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))