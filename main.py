import discord
import os #gives access to listdir()
import importlib

commandDir = 'commands' #where modules are stored
commandList = []
buffer = []
TOKEN = open("faadbotToken.txt", "r").read() #Gets OAuth2 Token for bot

client = discord.Client()

@client.event #bootup event
async def on_ready():
    print('Logged in as ' + client.user.name + ' ' + client.user.id)
    print('-----')

    try:
        for commandFile in os.listdir(commandDir):
            if commandFile != '__init__.py' and commandFile.endswith(".py"): #make sure not to import init file
                buffer = commandFile.split('.')
                #print(buffer[0])
                foundCommand = importlib.import_module(commandDir + "." + buffer[0])
                print(foundCommand)
                commandList.append(buffer[0]) #adds module command to list of commands
    except FileNotFoundError:
        print('No command files found')

client.run(TOKEN) #runs bot, should be last line