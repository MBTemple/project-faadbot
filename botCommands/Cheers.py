import discord
from discord.ext import commands
import random as r


class Cheers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix="")

    @bot.event
    async def on_message(self, message):
        cheer_text = (
            'yay',
            'Yay',
            'YAY',
            'YAY!'
        )
        if message.content.startswith(cheer_text):

            cheers = [
                "HOORAH!",
                "HURRAY!",
                "OORAH!",
                "YAY!",
                "HOOHAH!",
                "HOOYAH!",
                'HUAH!',
                '♪ ┏(°.°)┛CHEERS!┗(°.°)┓ ♬'
            ]

            cheer = r.choice(cheers)
            await message.channel.send(cheer)


def setup(bot):
    bot.add_cog(Cheers(bot))