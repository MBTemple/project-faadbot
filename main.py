import discord
import os #gives access to listdir()
import importlib

discordCommandDir = 'discordCommands' #storage for discord affecting modules
botCommandDir = 'botCommands' #storage for bot related modules
commandList = []
buffer = []
TOKEN = open("faadbotToken.txt", "r").read() #Gets OAuth2 Token for bot

client = discord.Client()

@client.event #bootup event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

    try: #parses and imports botCommand modules
        for commandFile in os.listdir(botCommandDir):
            if commandFile != '__init__.py' and commandFile.endswith(".py"): #make sure not to import init file
                buffer = commandFile.split('.')
                #print(buffer[0])
                foundCommand = importlib.import_module(botCommandDir + "." + buffer[0])
                print(foundCommand)
                commandList.append(buffer[0]) #adds module command to list of commands
    except FileNotFoundError:
        print('No command files found')
    try: #parses and imports discordCommand modules
        for commandFile in os.listdir(discordCommandDir):
            if commandFile != '__init__.py' and commandFile.endswith(".py"): #make sure not to import init file
                buffer = commandFile.split('.')
                #print(buffer[0])
                foundCommand = importlib.import_module(discordCommandDir + "." + buffer[0])
                print(foundCommand)
                commandList.append(buffer[0]) #adds module command to list of commands
    except FileNotFoundError:
        print('No command files found')

    #verify inputs in terminal
    print('Commands that have been imported:\n')
    for com in commandList:
        print(com + ' ')
    print('\n')

client.run(TOKEN) #runs bot, should be last line