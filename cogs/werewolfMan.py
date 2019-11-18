import discord
from discord.ext import commands
import random

#currently supports a maximum of 10 players

class werewolfMan(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = 'Wstartup')
    async def Wstartup(self, ctx):
        await ctx.send('Initializing werewolf mod.')
        await ctx.send('Please input your name to join the game')
        await ctx.send('Join Syntax: !?join PlayerName')
        await ctx.send('Change roles Syntax: !?roleSetting')
        await ctx.send('Game Start Syntax: !?beginGame')
        await ctx.send('Ideally you should join in the order you are sitting')
        f = open("cogs/log/werewolfData.txt", "w")
        g = open("cogs/log/werewolfRoles.txt", "w")
        #f.write("Players:\n")
        f.close()
        g.close()

    @commands.command(name = 'roleSetting')
    async def roleSetting(self, ctx, arg1 : str, arg2 : int):
        g = open("cogs/log/werewolfRoles.txt", "a")
        #only including default setting for now
        if arg1 == "default" and arg2 < 16:
            g.write("Werewolf:2")
            g.write("Seer:1")
            g.write("Doctor:1")
            g.write("Villager:12")
        g.close()

    @commands.command(name = 'join')
    async def join(self, ctx, arg1):
        f = open("cogs/log/werewolfData.txt", "a")
        f.write(str(ctx.message.author.id) + ":" + arg1 + "\n")
        await ctx.send(arg1 + ' has joined the game')
        f.close()

    @commands.command(name = 'beginGame')
    async def beginGame(self, ctx):

        getID = []
        playerCount = 0
        await ctx.send("beginning game with players:")
        f = open("cogs/log/werewolfData.txt", "r")
        for line in f:
            if playerCount >= 0 and not line.split():
                getID = line.split(':')
                await ctx.send(getID[1])
                user = self.bot.get_user(int(getID[0]))
                await user.send("You are registered for the round") #works as reply
                await user.send("Use this chat to make actions each round")
            playerCount+=1
        #f.close() #commenting this out since werewolfData is used for assigning roles

        if(playerCount < 7): #forces one night rules if less than 7 players
            roles = open("cogs/werewolfRoles.txt", "w")
            roles.write("one night:default\n") #rule description
            roles.write("Werewolf:0\nWerewolf:0\nSeer:0\nRobber:0\nTroublemaker:0\nVillager:0\n") #total of 6 roles
            #number after colon in werewolfRoles determines if role is taken or not. 1 means claimed
        
        noWerewolf = True
        while(noWerewolf):
            g = open("cogs/log/werewolfRound.txt", "w") #used to store round by round info
            #will player information as "userID:PlayerName:Role:GameStatus" with GameStatus being alive or dead
            for line in f:
                openRoles = []
                for role in roles:
                    tempRoles = []
                    tempRoles = role.split(":")
                    print(tempRoles[0])
                    if tempRoles[1] == "0":
                        openRoles.append(tempRoles[0])
                    print("Werewolf Management: Role " + tempRoles[0] + " added to openRoles")
                chosenRole = random.choice(openRoles)
                if chosenRole == "Werewolf":
                    noWerewolf = False
                player = line[:-2]
                print("Werewolf Management: Chosen role for " + player + " is: " + chosenRole)
                g.write(player + ":" + chosenRole + ":Alive\n")

                
        roles.close()
        g.close()
        f.close()


def setup(bot):
    bot.add_cog(werewolfMan(bot))