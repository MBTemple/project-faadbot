import discord
from discord.ext import commands
import random
import mysql.connector
from mysql.connector import Error

#currently supports a maximum of 10 players

class werewolfMan(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.rolesAdded = False
        self.dbPassLoc = "games/werewolfMod/localhostDBPW.txt"

    @commands.command(name = 'Wstartup')
    async def Wstartup(self, ctx):
        await ctx.send("Initializing werewolf mod. \n")

        TOKEN = open(self.dbPassLoc, "r").read() #gets localhost database password
        self.rolesAdded = False

        try:
            connection = mysql.connector.connect(host = 'localhost',
                                                database = 'testDB',
                                                user = 'root',
                                                password = TOKEN)
            
            if connection.is_connected():
                print("****************************************************")
                print("Connected to database for reset")
            cursor = connection.cursor()

            #drops tables needed for game if exists
            sql = "DROP TABLE IF EXISTS players"
            cursor.execute(sql)
            sql = "DROP TABLE IF EXISTS roles"
            cursor.execute(sql)
            sql = "DROP TABLE IF EXISTS round"
            cursor.execute(sql)
            #all required tables should no longer exist now. Recreating tables

            #in table players, name is the player chosen name for the game instance
            #userID is the userID number tied to the discord user in the game
            makePlayers = "CREATE TABLE players (userID VARCHAR(50) PRIMARY KEY, \
                name VARCHAR(255) NOT NULL)"
            #in table roles, rolename is the name for a player role. Only role names
            #from the official werewolf game are acceptable here
            #roleStatus is a binary int that indicates if the role has been assigned to a player
            makeRoles = "CREATE TABLE roles (roleName VARCHAR(255), roleStatus TINYINT)"
            #in table round, name is the player chosen name for the game instance
            #userID is the userID number tied to the discord user in the game
            #rolename is the name for a player role associated to the player entry
            #status is a binary int indicating if the player is alive or not (1 for alive)
            makeRound = "CREATE TABLE round (id INT AUTO_INCREMENT PRIMARY KEY, \
                name VARCHAR(255), userID INT(100), roleName VARCHAR(255), \
                status INT(1))"

            cursor.execute(makePlayers)
            cursor.execute(makeRoles)
            cursor.execute(makeRound)
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection for reset is closed")
                print("****************************************************")

        await ctx.send("Please input your name to join the game \n \
Join Syntax: ``!join Playername`` \n \
Change roles Syntax: ``!roleSetting`` \n \
Game Start Syntax: ``!beginGame`` \n \
Ideally you should join in the order you are sitting")

    @commands.command(name = 'roleSetting')
    async def roleSetting(self, ctx):
        TOKEN = open(self.dbPassLoc, "r").read()
        try:
            connection = mysql.connector.connect(host = 'localhost', 
                                                database = 'testDB',
                                                user = 'root',
                                                password = TOKEN)
            if connection.is_connected():
                cursor = connection.cursor()
                print("****************************************************")
                playerCount = cursor.rowcount
                if playerCount == 0:
                    await ctx.send("no players in game")

                elif playerCount < 3:
                    await ctx.send("not enough players for a game. werewolf requires at least 3")
                
                elif playerCount == 3: #forces one night roles with single werewolf for 3 player group
                    await ctx.send("defaulting to one-night roles with single werewolf due to party size")
                    sql = "INSERT INTO roles (roleName, roleStatus) VALUES (%s, %s)"
                    inVal = [
                        ('werewolf', '0'),
                        ('seer', '0'),
                        ('robber', '0'), #need to decide later if robber and troublemaker should be kept
                        ('troublemaker', '0'),
                        ('villager', '0'),
                        ('villager', '0'),
                        ('villager', '0'),
                    ]

                    cursor.executemany(sql, inVal)
                    connection.commit()
                    print(cursor.rowcount, " roles were added")
                    self.rolesAdded = True

                elif playerCount <= 5: #forces one night roles with two werewolves for party between 7 and 3 players
                    await ctx.send("defaulting to one-night roles due to party size")
                    sql = "INSERT INTO roles (roleName, roleStatus) VALUES (%s, %s)"
                    inVal = [
                        ('werewolf', '0')
                        ('werewolf', '0'),
                        ('seer', '0'),
                        ('robber', '0'), #need to decide later if robber and troublemaker should be kept
                        ('troublemaker', '0'),
                        ('villager', '0'),
                        ('villager', '0'),
                        ('villager', '0'),
                    ]

                    cursor.executemany(sql, inVal)
                    connection.commit()
                    print(cursor.rowcount, " roles were added")
                    self.rolesAdded = True

                elif playerCount <= 16: #smaller default werewolf ruleset
                    ctx.send("using defualt werewolf roleset")
                    sql = "INSERT INTO roles (roleName, roleStatus) VALUES (%s, %s)"
                    inVal = [
                        ('werewolf', '0'),
                        ('werewolf', '0'),
                        ('werewolf', '0'),
                        ('werewolf', '0'),
                        ('seer', '0'),
                        ('seerInsane', '0'),
                        ('hunter', '0'),
                        ('fool', '0'),
                        ('mason', '0'),
                        ('mason', '0'),
                        ('mason', '0'),
                        ('bodyguard', '0'),
                        ('pacifist', '0'),
                        ('pacifist', '0'),
                        ('gunsmith', '0'),
                        ('villager', '0'),
                        ('villager', '0'),
                        ('villager', '0'),
                        ('villager', '0'),                        
                    ] #refer to: https://boardgamegeek.com/wiki/page/BGG_Werewolf_PBF_Role_List

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                print("****************************************************")

    @commands.command(name = 'join')
    async def join(self, ctx, arg1):
        TOKEN = open(self.dbPassLoc, "r").read()
        try:
            connection = mysql.connector.connect(host = 'localhost', 
                                                database = 'testDB',
                                                user = 'root',
                                                password = TOKEN)
            if connection.is_connected():
                nameUnique = True
                userUnique = True
                inputNameComp = "%s" % arg1
                userIDComp = "%s" % ctx.message.author.id

                cursor = connection.cursor()
                print("****************************************************")
                #first check for duplicates
                #if duplicate userID, update name
                #if duplicate name, deny insert and notify user
                cursor.execute("SELECT * FROM players")
                playerList = cursor.fetchall()
                for entry in playerList:
                    if entry[1] == inputNameComp:
                        await ctx.send("Duplicate name detected. Select new name")
                        nameUnique = False
                    elif entry[0] == userIDComp:
                        await ctx.send("Updating player name")
                        userUnique = False
                        sql = "UPDATE players SET name = %s WHERE userID = %s"
                        inVal = (arg1, entry[0])
                        cursor.execute(sql, inVal)
                        connection.commit()
                        print(cursor.rowcount, "record(s) affected")

                #actual insert if duplicate check passes
                if nameUnique and userUnique:
                    sql = "INSERT INTO players (userID, name) VALUES (%s, %s)"
                    print("Connected to database to add " + str(ctx.message.author.id) +":" + arg1)
                    inVal = (ctx.message.author.id, arg1)
                    cursor.execute(sql, inVal)
                    connection.commit()
                    print(cursor.rowcount, "record inserted.")
                    await ctx.send(arg1 + ' has joined the game')
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                print("****************************************************")

    @commands.command(name = 'beginGame')
    async def beginGame(self, ctx):

        getID = []
        playerCount = 0
        await ctx.send("beginning game with players:")
        with open("cogs/werewolfData.txt", "r") as f:
            for line in f:
                if playerCount >= 0:
                    getID = line.split(':')
                    await ctx.send(getID[1])
                    user = self.bot.get_user(int(getID[0]))
                    await user.send("You are registered for the round") #works as reply
                    await user.send("Use this chat to make actions each round")
                playerCount+=1

        if playerCount == 0:
            await ctx.send("no players in game")

        if(playerCount == 3 ): #forces one night rules with single werewolf for 3 player group
            await ctx.send("defaulting to one night rules with single werewolf due to party size")
            with open("cogs/werewolfRoles.txt", 'w') as roles:
                roles.write("one night:default\nWerewolf:0\n \
Seer:0\nRobber:0\nTroublemaker:0\nVillager:0\nVillager:0\nVillager\n \
") #rule description

        elif(playerCount <=7): # forces one night rules with two werewolves for 7 or less players but more than 3
            await ctx.send("defaulting to normal one night rules due to party size")
            with open("cogs/werewolfRoles.txt", 'w') as roles:
                roles.write("one night:default\nWerewolf:0\nWerewolf:0\n \
Seer:0\nRobber:0\nTroublemaker:0\nVillager:0\nVillager:0\nVillager\n \
") #rule description


            #roles.write("Werewolf:0\nWerewolf:0\nSeer:0\nRobber:0\nTroublemaker:0\nVillager:0\n") #total of 6 roles
            #number after colon in werewolfRoles determines if role is taken or not. 1 means claimed
        
        #await ctx.send("assigning roles, standby for messages")
        noWerewolf = True #false to skip over this temporarily for testing
        while(noWerewolf):
            g = open("cogs/werewolfRound.txt", "w") #used to store round by round info
            playerInfo = open("cogs/werewolfData.txt", "r")
            #will player information as "userID:PlayerName:Role:GameStatus" with GameStatus being alive or dead
            #await ctx.send("Assigning player roles")
            for line in playerInfo:   
                roles = open("cogs/werewolfRoles.txt", "r")            
                openRoles = []
                for role in roles:
                    tempRoles = []
                    tempRoles = role.split(":")
                    if tempRoles[1] == "0\n":
                        openRoles.append(tempRoles[0])
                        print("Werewolf Management: Role " + tempRoles[0] + " added to openRoles")
                roles.close()
                chosenRole = random.choice(openRoles)
                openRoles.remove(chosenRole)
                #await ctx.send(chosenRole) #here to test
                if chosenRole == "Werewolf":
                    noWerewolf = False
                player = line[:-1]
                print("Werewolf Management: Chosen role for " + player + " is: " + chosenRole)
                g.write(player + ":" + chosenRole + ":Alive\n")
                roles = open("cogs/werewolfRoles.txt", "w")
                for role in openRoles:
                    roles.write(role + ":0\n")

                
        roles.close()
        g.close()
        playerInfo.close()
        await ctx.send("role assignment complete")


def setup(bot):
    bot.add_cog(werewolfMan(bot))