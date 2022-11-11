from discord.ext import commands


class Event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Event Extension Loaded')

    @commands.command(name="sayd")
    async def __sayd(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)


async def setup(bot):
    await bot.add_cog(Event(bot))