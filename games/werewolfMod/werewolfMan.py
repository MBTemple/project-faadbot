import discord
from discord.ext import commands
import random
import mysql.connector
from mysql.connector import Error
import math

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
Ideally you should join in the order you are sitting \n \
Join Syntax: ``!join Playername`` \n \
After all players have joined but before starting the game you have to establish a role-set \n \
Current role-sets: ``justVillagers``, ``basicSpecials``, ``allSpecials`` \n \
Change roles Syntax: ``!roleSetting justVillagers`` \n \
Game Start Syntax: ``!beginGame``")

    @commands.command(name = 'Whelp')
    async def Whelp(self,ctx):
        await ctx.send("Please input your name to join the game \n \
Ideally you should join in the order you are sitting \n \
Join Syntax: ``!join Playername`` \n \
After all players have joined but before starting the game you have to establish a role-set \n \
Current role-sets: ``justVillagers``, ``basicSpecials``, ``allSpecials`` \n \
Change roles Syntax: ``!roleSetting justVillagers`` \n \
Game Start Syntax: ``!beginGame``")

    @commands.command(name = 'roleSetting')
    async def roleSetting(self, ctx, arg1):
        if arg1 == "justVillagers":
            specialRoles = False
            basicRoles = False
            await ctx.send("special roles are disabled")
        elif arg1 == "allSpecials":
            specialRoles = True
            basicRoles = False
            await ctx.send("special roles are enabled")
        elif arg1 == "basicSpecials":
            specialRoles = False
            basicRoles = True
            await ctx.send("only seer and doctor are enabled")
        else:
            specialRoles = False
            basicRoles = False
            await ctx.send("Invalid input, defaulting to justVillagers")

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
                
                elif playerCount == 3 and specialRoles: #forces one night roles with single werewolf for 3 player group
                    await ctx.send("defaulting to one-night roles with single werewolf due to party size")
                    sql = "INSERT INTO roles (roleName, roleStatus) VALUES (%s, %s)"
                    inVal = [
                        ('werewolf', '0'),                            ('seer', '0'),
                        ('robber', '0'), #need to decide later if robber and troublemaker should be kept
                        ('troublemaker', '0'),
                        ('villager', '0'),
                        ('villager', '0'),
                        ('villager', '0')
                    ]

                    cursor.executemany(sql, inVal)
                    connection.commit()
                    print(cursor.rowcount, " roles were added")
                    self.rolesAdded = True

                elif playerCount <= 5 and specialRoles: #forces one night roles with two werewolves for party between 7 and 3 players
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
                        ('villager', '0')
                    ]

                    cursor.executemany(sql, inVal)
                    connection.commit()
                    print(cursor.rowcount, " roles were added")
                    self.rolesAdded = True

                elif playerCount <= 16 and specialRoles: #smaller default werewolf ruleset
                    await ctx.send("using defualt werewolf roleset")
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
                        ('villager', '0')                       
                    ] #refer to: https://boardgamegeek.com/wiki/page/BGG_Werewolf_PBF_Role_List

                elif playerCount < 5 and basicRoles:
                    await ctx.send("not enough players for game with seer and doctor. Need at least 5")

                elif playerCount >= 5 and basicRoles:
                    numWerewolves = math.floor(playerCount/5)
                    await ctx.send("there will be " + numWerewolves + " werewolves")
                    sql = "INSERT INTO roles (roleName, roleStatus) VALUES (%s, %s)"
                    wwinVal = [
                        ('werewolf', '0')
                    ]

                    vilinVal = [
                        ('villager', '0')
                    ]

                    otherinVal = [
                        ('seer', '0'),
                        ('doctor', '0')
                    ]
                    #adding just seer and doctor
                    cursor.executemany(sql, otherinVal)
                    connection.commit()
                    print(cursor.rowcount, " roles were added")

                    for _ in range(numWerewolves):
                        cursor.execute(sql, wwinVal)
                        connection.commit()
                        print(cursor.rowcount, " werewolf added")

                    numVillagers = playerCount - numWerewolves - 2
                    for _ in range(numVillagers):
                        cursor.execute(sql, vilinVal)
                        connection.commit()
                        print(cursor.rowcount, " villager added")
                    self.rolesAdded = True

                elif playerCount >= 5:
                    numWerewolves = math.floor(playerCount/5)
                    await ctx.send("there will be " + numWerewolves + " werewolves")
                    sql = "INSERT INTO roles (roleName, roleStatus) VALUES (%s, %s)"
                    wwinVal = [
                        ('werewolf', '0')
                    ]

                    vilinVal = [
                        ('villager', '0')
                    ]

                    for _ in range(numWerewolves):
                        cursor.execute(sql, wwinVal)
                        connection.commit()
                        print(cursor.rowcount, " werewolf added")

                    numVillagers = playerCount - numWerewolves
                    for _ in range(numVillagers):
                        cursor.execute(sql, vilinVal)
                        connection.commit()
                        print(cursor.rowcount, " villager added")
                    self.rolesAdded = True

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
        TOKEN = open(self.dbPassLoc, "r").read()
        try:
            connection = mysql.connector.connect(host = 'lolcalhost',
                                                database = 'testDB',
                                                user = 'root',
                                                password = TOKEN)

            if connection.is_connected():
                cursor = connection.cursor()
                print("****************************************************")
                cursor.execute("SELECT * FROM players")
                playerList = cursor.fetchall()
                if self.rolesAdded:
                    for entry in playerList: #format (userID, name)
                        user = self.bot.get_user(int(entry[0]))
                        await user.send("You are registered for the game")
                        await user.send("Use this chat to make actions for each round")
                        await user.send("Standby for role assignment")
                        sql = "INSERT INTO round (name, userID, status) VALUES (%s, %s, %s)"
                        roundVal = (entry[1], entry[0], "1")
                        cursor.execute(sql, roundVal)
                        connection.commit()
                    #actually assigning roles now
                    cursor.execute("SELECT * FROM round")
                    roundList = cursor.fetchall()
                    for entry in roundList: #format (id, name, userID, roleName, status)
                        cursor.execute("SELECT * FROM roles WHERE roleStatus = '0'")
                        openRolesList = cursor.fetchall()
                        openRoles = []
                        for role in openRolesList:
                            openRoles.append(role[0])
                        chosenRole = random.choice(openRoles)
                        sql = "UPDATE round SET roleName = %s WHERE userID = %s"
                        inputVal = (chosenRole, entry[2])
                        cursor.execute(sql, inputVal)
                        connection.commit()
                        print("Player: " + entry[1] + ":" + entry[2] + "is role: " + chosenRole +"\n")
                        user = self.bot.get_user(int(entry[2]))
                        await user.send("Your player name is : " + entry[1])
                        await user.send("You are assigned role: " + chosenRole)
                        #now to remove chosenRole from openRole db
                        sql = "UPDATE roles SET roleStatus = %s WHERE roleName = %s limit 1"
                        roleUpdate = ("1", chosenRole)
                        cursor.execute(sql, roleUpdate)
                        connection.commit()
                    await ctx.send("roles have been assigned")


                else:
                    await ctx.send("roles not yet set. Please set roles first")
        except Error as e:
            print("Error while conecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                print("****************************************************")

# old code ################################################
#                                                         #
#                                                         #
#                                                         #
#                                                         #
#                                                         #
#                                                         #
# old code ################################################


def setup(bot):
    bot.add_cog(werewolfMan(bot))