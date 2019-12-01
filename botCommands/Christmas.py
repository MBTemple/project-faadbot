import datetime
import discord
from discord.ext import commands
from datetime import datetime


class Christmas(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.command(name='countdown')
    async def cc(self, ctx):
        futuredate = datetime.strptime('Dec 25 2019  0:00', '%b %d %Y %H:%M')
        nowdate = datetime.now()
        count = int((futuredate-nowdate).total_seconds())
        days = count//86400
        hours = (count-days*86400)//3600
        minutes = (count-days*86400-hours*3600)//60
        seconds = count-days*86400-hours*3600-minutes*60
        embed = discord.Embed(colour=0x9c0101, description=f"There are...\n**{days}** days\n**{hours}** hours\n**{minutes}** minutes\n**{seconds}** seconds\n... until Christmas!")
        embed.set_author(icon_url=ctx.me.avatar_url_as(format='png'), name="Countdown to Christmas")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Christmas(bot))