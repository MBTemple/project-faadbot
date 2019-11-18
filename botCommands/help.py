import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.remove_command('help')

    @commands.command(aliases=['helpme', 'HELPME', 'helpME', 'HELPme', 'HELP', 'commands', 'COMMANDS'])
    async def help(self, ctx):
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
    bot.add_cog(Help(bot))
