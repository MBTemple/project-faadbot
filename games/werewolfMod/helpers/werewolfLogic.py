import mysql.connector
from mysql.connector import Error
import math
import re # used for multi-delimiter tokenizing

class werewolfLogic:
    def __init__(self):
        self.dbPassLoc = "games/werewolfMod/localhostDBPW.txt"
        self.testUserList = "games/werewolfMod/testUserInfo.txt"
        self.dbName = "testDB" #name of sql database, change if necessary
    
    def WLstartup(self):
        #get localhost mysql password for root
        TOKEN = open(self.dbPassLoc, "r").read()

        try:
            connection = mysql.connector.connect(
                host = 'localhost', 
                database = self.dbName, #change db name if necessary
                user = 'root',
                password = TOKEN)

            if connection.is_connected():
                print("****************************************************\n")
                print("Connected to database for reset\n")
                cursor = connection.cursor()

                #drops tables needed for game if exists
                cursor.execute("DROP TABLE IF EXISTS players")
                cursor.execute("DROP TABLE IF EXISTS roles")
                cursor.execute("DROP TABLE IF EXISTS round")
                #all require tables should no longer exist now. 
                #Recreating tables

                #in table players, name is the player chosen name for the game instance
                #userID is the userID number tied to the discord user in the game
                makePlayers = "CREATE TABLE players (userID VARCHAR(50) PRIMARY KEY, \
                    name VARCHAR(255) NOT NULL)"
                #in table roles, rolename is the name for a player role. Only role names
                #from the official werewolf game are acceptable here
                #roleStatus is a binary int that indicates if the role has been assigned to a player
                makeRoles = "CREATE TABLE roles (roleName VARCHAR(255), roleStatus TINYINT, specialAction VARCHAR(50))"
                #in table round, name is the player chosen name for the game instance
                #userID is the userID number tied to the discord user in the game
                #rolename is the name for a player role associated to the player entry
                #status is a binary int indicating if the player is alive or not (1 for alive)
                makeRound = "CREATE TABLE round (id INT AUTO_INCREMENT PRIMARY KEY, \
                    name VARCHAR(255), userID VARCHAR(50), roleName VARCHAR(255), \
                    status INT(1), specialAction VARCHAR(50))"

                #execute above sql calls to create tables
                cursor.execute(makePlayers)
                cursor.execute(makeRoles)
                cursor.execute(makeRound)

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection for reset is closed\n")
                print("****************************************************\n")

    #def WLroleSetting(playerCount, roleSet):
     #   if roleSet == "justVillagers":
      #      print("Using justVillagers as role set")

       # elif roleSet == "allSpecials"

    #for populating database with saved test users
    def WLfillUsers(self):
        try:
            userListFile = open(self.testUserList, "r")
            print("****************************************************\n")
            print("Filling database with saved users\n")
            user = []
            TOKEN = open(self.dbPassLoc, "r").read()
            for line in userListFile:
                user = re.split('[:\n]', line)
                try:
                    connection = mysql.connector.connect(
                        host = 'localhost', 
                        database = self.dbName, #change db name if necessary
                        user = 'root',
                        password = TOKEN)

                    if connection.is_connected():
                        cursor = connection.cursor()
                        sql = "INSERT INTO players (userID, name) VALUES (%s, %s)"
                        values = (user[0], user[1])
                        cursor.execute(sql, values)
                        connection.commit()

                except Error as e:
                    print("Error while connecting to MySQL", e)
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()
                        print("Saved userID {} and user {} added to database\n".format(user[0], user[1]))
        except:
            print("File for test users does not exist\n")
        finally:
            userListFile.close()
            print("****************************************************\n")

    #for saving current test users in database
    #WARNING: will delete previously saved set of test users
    def WLsaveUsers(self):
        try:
            print("****************************************************\n")
            print("Loading users from database to save\n")
            userListFile = open(self.testUserList, "w")
            try:
                TOKEN = open(self.dbPassLoc, "r").read()
                connection = mysql.connector.connect(
                    host = 'localhost',
                    database = self.dbName,
                    user = 'root',
                    password = TOKEN)
                
                if connection.is_connected():
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM players")
                    userList = cursor.fetchall()
                    for user in userList:
                        userListFile.write("{}:{}\n".format(user[0], user[1]))
                        print("adding {} {} to file\n".format(user[0], user[1]))
            
            except Error as e:
                print("Error while connecting to MySQL", e)
            finally:
                cursor.close()
                connection.close()
        
        except:
            print("Failed to open user file for saving\n")
        finally:
            print("Completed saving test users from database")
            print("****************************************************\n")
            userListFile.close()