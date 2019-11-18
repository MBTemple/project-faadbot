import discord 
from discord.ext import commands
from discord.ext.commands import has_permissions

class kick(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = 'kick')
    @has_permissions(manage_roles=True, kick_members=True)
    async def kick(self,ctx, member:discord.Member, *, reason=None ):
        await member.kick(reason=reason)

def setup(bot):
    bot.add_cog(kick(bot))