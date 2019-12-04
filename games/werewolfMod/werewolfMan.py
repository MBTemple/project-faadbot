import discord
from discord.ext import commands
import random
import mysql.connector
from mysql.connector import Error
import math
from games.werewolfMod.helpers.werewolfLogic import werewolfLogic

#currently supports a maximum of 10 players

class werewolfMan(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.rolesAdded = False
        self.dbPassLoc = "games/werewolfMod/localhostDBPW.txt"
        self.lynchActive = False
        self.lynchSeconded = False
        self.lynchAttempt = 0
        self.isDay = True
        self.statusList = None
        self.statusRef = [] #reference to statusList message in chat for editing
        self.werewolfHelper = werewolfLogic()

    @commands.command(name = 'Wstartup')
    async def Wstartup(self, ctx):
        await ctx.send("Initializing werewolf mod. \n")
        self.rolesAdded = False
        self.statusList = None
        self.statusRef = None

        self.werewolfHelper.WLstartup() #handles all MySQL actions for startup

        await ctx.send("Please input your name to join the game \n \
Ideally you should join in the order you are sitting \n \
Join Syntax: ``!Wjoin Playername`` \n \
After all players have joined but before starting the game you have to establish a role-set \n \
Current role-sets: ``justVillagers``, ``basicSpecials``, ``allSpecials`` \n \
Change roles Syntax: ``!WroleSetting justVillagers`` \n \
Game Start Syntax: ``!WbeginGame``")

    @commands.command(name = 'Whelp')
    async def Whelp(self,ctx):
        await ctx.send("Please input your name to join the game \n \
Ideally you should join in the order you are sitting \n \
Join Syntax: ``!Wjoin Playername`` \n \
After all players have joined but before starting the game you have to establish a role-set \n \
Current role-sets: ``justVillagers``, ``basicSpecials`` \n \
Change roles Syntax: ``!WroleSetting justVillagers`` \n \
Game Start Syntax: ``!WbeginGame``")

    @commands.command(name = 'WroleSetting')
    async def WroleSetting(self, ctx, arg1):
        playerCount = self.werewolfHelper.getPlayerCount()
        numWerewolves = int(math.floor(int(playerCount[0])/5))
        if arg1 == "justVillagers":
            await ctx.send("all special roles are disabled\n\
There will be {} werewolves".format(numWerewolves))
            self.werewolfHelper.WLroleSetting(playerCount[0], numWerewolves, 1)
            self.rolesAdded = True

        elif arg1 == "allSpecials":
            await ctx.send("This feature is not yet implemented. Please choose another")
        
        elif arg1 == "basicSpecials":
            await ctx.send("only seer and doctor are enabled\n\
There will be {} werewolves".format(numWerewolves))
            self.werewolfHelper.WLroleSetting(playerCount[0], numWerewolves, 2)
            self.rolesAdded = True

        else:
            await ctx.send("Invalid input")

    @commands.command(name = 'Wjoin')
    async def Wjoin(self, ctx, arg1):
        userID = "%s" % int(ctx.message.author.id)
        statusCode = self.werewolfHelper.WLjoin(userID, arg1)
        if statusCode == 0: #except error code
            await ctx.send("An error has occurred")
        elif statusCode == 1: #pass code
            await ctx.send("{} has joined the game".format(arg1))
        elif statusCode == 2: # duplicate name code
            await ctx.send("Duplicate name detected. Player names must be unique, please choose another name")
        elif statusCode == 3: #duplicate id code
            await ctx.send("Player name updated to {}".format(arg1))

    @commands.command(name = 'WbeginGame')
    async def WbeginGame(self, ctx):
        if self.rolesAdded:
            self.werewolfHelper.WLcreateRound() #assigns roles to players
            playerList = self.werewolfHelper.getPlayerList() #gets list of userIDs
            for playerID in playerList:
                UIstring = self.werewolfHelper.makeUI(playerID) #gets UI string to send to player
                user = self.bot.get_user(int(playerID))
                await user.send(UIstring)
                #TODO : find a way to store msg references to edit
                #self.statusRef.append(msg)
        else:
            await ctx.send("roles not yet set. Please set roles first")
  

# Action commands #########################################
###########################################################                                                         
###########################################################                                                          
###########################################################                                                          
###########################################################                                                          
###########################################################                                                          
###########################################################                                                          
# Action commands #########################################

    @commands.command(name = 'Wlynch')
    async def Wlynch(self, ctx, arg1):
        TOKEN = open(self.dbPassLoc, "r").read()
        try:
            connection = mysql.connector.connect(host = 'localhost', 
                                                database = 'testDB',
                                                user = 'root',
                                                password = TOKEN)
            if connection.is_connected():
                cursor = connection.cursor()
                print("****************************************************")
                #there are two votes that can occur for lynching
                #each lynching notion that is initiated must have a second person backing it
                #If a lynching notion passes, it immediately goes to night
                if self.isDay and not self.lynchActive:
                    arg1Exists = False
                    cursor.execute("SELECT * FROM players")
                    playerList = cursor.fetchall()
                    
                    for player in playerList:
                        if player[1] == arg1:
                            arg1Exists = True
                    if arg1Exists:
                        initiator = ctx.message.author.id
                        cursor.execute("SELECT * FROM players WHERE userID = {}".format(initiator))
                        initiatorName = cursor.fetchone()
                        for player in playerList:
                            user = self.bot.get_user(int(player[0]))
                            msg = self.statusRef
                            msg = msg + "{} has started a lynch vote against {} but needs \
                                someone to second this notion! (User ``!Wlynch Second`` to second \
                                the notion)".format(initiatorName[1], arg1)
                            await message.edit(content = msg)
                            #await user.send("{} has started a lynch vote against {} but needs \
                            #    someone to second this notion! (User ``!Wlynch Second`` to second \
                            #    the notion)".format(initiatorName[1], arg1))
                        self.lynchActive = True

                #elif self.isDay and self.lynchActive and arg1 == "second": #someone seconds a lynch attempt


                else:
                    await ctx.send("You can't use this until the daytime!")

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                print("****************************************************")

# Dev commands ############################################
###########################################################                                                         
###########################################################                                                          
###########################################################                                                          
###########################################################                                                          
###########################################################                                                          
###########################################################                                                          
# Dev commands ############################################

    @commands.command(name = 'WsaveUsers')
    async def WsaveUsers(self, ctx):
        await ctx.send("Attempting to save users in database locally")
        self.werewolfHelper.WLsaveUsers()

    @commands.command(name = 'WfillUsers')
    async def WfillUsers(self, ctx):
        await ctx.send("Attempting to fill database with saved users")
        self.werewolfHelper.WLfillUsers()

def setup(bot):
    bot.add_cog(werewolfMan(bot))