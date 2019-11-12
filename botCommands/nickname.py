import discord
from discord.ext import commands


class Nickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='nickname')
    async def nickname(self, ctx, name: str = None):
        """Change your nickname on a server. Leave empty to remove nick."""
        if name is None:
            # await ctx.message.delete()
            await ctx.message.author.edit(nick=name)
            await ctx.send('Reset nickname back to %s' % ctx.message.author.name)
        else:
            await ctx.message.author.edit(nick=name)
            await ctx.send('Changed nickname to %s' % name)


def setup(bot):
    bot.add_cog(Nickname(bot))
