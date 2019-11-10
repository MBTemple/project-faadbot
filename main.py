import discord
import os #gives access to listdir()
import importlib
import sys
from discord.ext import commands

discordCommandDir = 'discordCommands' #storage for discord affecting modules
botCommandDir = 'botCommands' #storage for bot related modules
commandList = []
buffer = []
TOKEN = open("faadbotToken.txt", "r").read() #Gets OAuth2 Token for bot


def get_prefix(bot, message):

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['!']

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix= get_prefix, description = 'bot')

cogs = ['cogs.startup']
#populate list of cogs
try: #parses and adds botCommand modules
    for commandFile in os.listdir(botCommandDir):
        if commandFile != '__init__.py' and commandFile.endswith(".py"): #dont want to add init file
            buffer = commandFile.split('.')
            foundCommand = botCommandDir + "." + buffer[0]
            #print(foundCommand + "\n") #testing
            commandList.append(foundCommand)
except FileNotFoundError:
    print('No command files found')

try: #parses and adds discordCommand modules
    for commandFile in os.listdir(discordCommandDir):
        if commandFile != '__init__.py' and commandFile.endswith(".py"): #dont want to add init file
            buffer = commandFile.split('.')
            foundCommand = discordCommandDir + "." + buffer[0]
            #print(foundCommand + "\n") #testing
            commandList.append(foundCommand)
except FileNotFoundError:
    print('No command files found')

if __name__ == '__main__':
    for extension in commandList:
        #print(extension + "\n")
        bot.load_extension(extension)

@bot.event #bootup event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')

    #verify inputs in terminal
    print('Commands that have been imported:\n')
    for com in commandList:
        if com not in sys.modules:
            print('You have not imported the {} module'.format(com))
        else:
            print(com + ' ')
    print('\n')

#client.run(TOKEN) #runs bot, should be last line
bot.run(TOKEN, bot=True, reconnect=True)