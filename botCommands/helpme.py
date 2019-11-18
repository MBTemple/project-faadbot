import discord
from discord.ext import commands


class HelpMe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['HELPME', 'helpME', 'HELPme', 'HELP', 'commands'])
    async def helpme(self, ctx):
        delim = []
        await ctx.send('List of bot commands: \n')
        CLfile = open("commandList.txt", "r")
        for line in CLfile:
            delim = line.split(".")
            await ctx.send('!' + delim[1] + '\n')
        CLfile.close()

        await ctx.send('\n-------------------------------\n')
        helpFile = open("help.txt", "r")
        await ctx.send(helpFile.read())


def setup(bot):
    bot.add_cog(HelpMe(bot))
