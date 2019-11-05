# project-faadbot

## Project Abstract

    Discord is a popular application that works in a similar manner to slack. Discord provides users the
    ability to create servers that other users can join to communicate with one another. Regardless of the
    focus of the server, there are often a number of features that can be troublesome to handle on larger
    sized servers. To fix this, discord bots can be made to handle common items like moderating chats, 
    assigning priviledges to particular users, or working with user management. This bot can also have 
    entertainment focused features like custom image posting or hosting of mini chat-based games. 
    For the purpose of this project, I plan on creating a discord bot that features several moderation 
    functions. All of these features will be implemented modularly using the discord api, and should 
    the project be too small, other entertainment focused modules can be implemented as well.
    
    For the complete project, interaction with the bot will be handled using the actual discord
    application. Since discord has a lot of bot friendly functionality, the bot would actually be
    added to a particular server as a bot, and interaction occurs in the text chat using a chosen
    special character. For example, if I have a help function with my bot, and use "!" as my 
    special character, I can invoke the help function by typing "!help" in chat.

## Background
    
    [https://github.com/CAPark/01-Park-FAADBot]
    
    Regarding the name of the project: the main function of the bot is to work as a ModeratorBot, which
    could simplify into ModBot. The problem with that name is that it is incredibly common and not
    distinguishable from the thousands of other ModBots. So to create the new name, I took the "Mod"
    section and converted the ascii values of letters into binary and then into hex. The final hex 
    number had 4 numbers in it and the letters "F" and "D". I just added the numbers up to get 20, 
    and chose "A" for the remaining to letters since "A" has a hex value of 10, having two adding 
    up to 20. As a result, I mashed together the letters "F", "A", "A", and "D" to get FAADBot.
    
## Vision

*FOR* discord users *WHO* have user requests that require moderator approval, the FAADBot 
is a discord bot *THAT* automates handling of these mundane tasks to reduce workload on moderators
*UNLIKE* most other discord bots, *OUR PRODUCT* will be created modularly to promote open-source additon 
of additional functionalities.

## Personas
#### Alex - Streamer

Alex, age 23, is a college student at XYZ university in Vermont. He is in his third year for an accounting degree.
When Alex isn't busy with his academics, he spends a significant amount of his time playing video games. TAlex
frequently uses discord to coordinate and communicate with his friends while playing games with them. Recently, 
with the increasing popularity of video game streaming in the past year, Alex wanted to attempt it himself. 
Since a majority of the starting difficulty of a streamer stems from advertising your channel, Alex takes to
discord as a means of putting out awareness of his streams. 

#### Jimmy - New Member

Jimmy, age 20, is a criminal justice major at a university in New York. Jimmy likes to spend his free time reading or watching documentaries. Jimmy has joined a club for other law majors to network, socialize and share resources. Jimmy wants to form new connections and make friends with other undergraduates in his field. This club’s members use Discord to communicate. Jimmy isn’t tech-illiterate but is not necessarily tech-savvy either. The only messaging app he’s familiar with is Facebook Messenger, so Discord is a new experience for him. Jimmy downloads the app and joins the server linked on the club’s webpage. He is initially overwhelmed by the options and settings available. Jimmy doesn’t want to join any large group discussions and is more so seeking to get to know some people individually. 


## Initially Planned Features

- Adding and removing roles (normal user)
- Change nicknames (normal user)
- Text to speech (normal user)
- Ban users (moderator/super user)
- Create or Delete roles (moderator/super user)

## Resources

[Link to Trello Board](https://trello.com/b/GrKoPabm/faadbot)

[Link to the discord server for testing](https://discord.gg/gv97GxT)

[Link to discord's python API](https://discordpy.readthedocs.io/en/latest/api.html)


## Group Members

- Christopher Park
- Sungji Kim
- Maamar Bousseloub
- Dawud Baig
