from discord.ext import commands


class Event(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        print('Event')


    @commands.command()
    async def _sayd(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Event(bot))