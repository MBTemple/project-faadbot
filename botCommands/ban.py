import discord 
from discord.ext import commands

class ban(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = 'ban')
    async def ban(self,ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)

def setup(bot):
    bot.add_cog(ban(bot))
