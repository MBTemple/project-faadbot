import discord
from discord.ext import commands
import random

#currently supports a maximum of 10 players

class werewolfMan(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = 'Wstartup')
    async def Wstartup(self, ctx):
        await ctx.send("Initializing werewolf mod. \n \
Please input your name to join the game \n \
Join Syntax: ``!join Playername`` \n \
Change roles Syntax: ``!roleSetting`` \n \
Game Start Syntax: ``!beginGame`` \n \
Ideally you should join in the order you are sitting")
        
        f = open("cogs/werewolfData.txt", "w")
        g = open("cogs/werewolfRoles.txt", "w")
        #f.write("Players:\n")
        f.close()
        g.close()

    @commands.command(name = 'roleSetting')
    async def roleSetting(self, ctx, arg1 : str, arg2 : int):
        g = open("cogs/werewolfRoles.txt", "a")
        #only including default setting for now
        if arg1 == "default" and arg2 < 16:
            g.write("Werewolf:2")
            g.write("Seer:1")
            g.write("Doctor:1")
            g.write("Villager:12")
        g.close()

    @commands.command(name = 'join')
    async def join(self, ctx, arg1):
        f = open("cogs/werewolfData.txt", "a")
        f.write(str(ctx.message.author.id) + ":" + arg1 + "\n")
        await ctx.send(arg1 + ' has joined the game')
        f.close()

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

        if(playerCount < 7): #forces one night rules if less than 7 players
            await ctx.send("defaulting to one night rules due to party size")
            with open("cogs/werewolfRoles.txt", 'w') as roles:
                roles.write("one night:default\nWerewolf:0\nWerewolf:0\nSeer:0\nRobber:0\nTroublemaker:0\nVillager:0\n") #rule description

            #roles.write("Werewolf:0\nWerewolf:0\nSeer:0\nRobber:0\nTroublemaker:0\nVillager:0\n") #total of 6 roles
            #number after colon in werewolfRoles determines if role is taken or not. 1 means claimed
        
        #await ctx.send("assigning roles, standby for messages")
        noWerewolf = True #false to skip over this temporarily for testing
        while(noWerewolf):
            g = open("cogs/werewolfRound.txt", "w") #used to store round by round info
            f = open("cogs/werewolfData.txt", "r")
            #will player information as "userID:PlayerName:Role:GameStatus" with GameStatus being alive or dead
            #await ctx.send("Assigning player roles")
            for line in f:   
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
        f.close()
        await ctx.send("role assignment complete")


def setup(bot):
    bot.add_cog(werewolfMan(bot))