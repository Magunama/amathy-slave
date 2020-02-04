from discord.ext import commands
from utils.checks import check_create_logging


class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["logs"])
    async def log(self, ctx):
        """Follow logging of certain events"""
        check_create_logging(ctx.guild.id, ctx.channel.id)
        await ctx.send("Logging enabled!")


def setup(bot):
    bot.add_cog(Log(bot))
