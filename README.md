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

## Project Relevance
    
    The greatest advantage of a discord bot project is that there are a nearly infinite number of utilities 
    that can be added to it. Should a project be too big or too small, features can quickly be added or dropped.
    The project itself is relevant to the course as each of these features would be implemented in a modular
    way. By doing this, it easily provides small modules for each team member to work on. By splitting features 
    up into these modules, not only does it allow team members to work on code that doesn't interfere with another
    team members', it also provides a great environment to implement TDD principles. Also, while this isn't 
    necessary, the modularity also provides the opportunity for team members with different coding backgrounds
    to work in their own familiar language, so long as a group effort is made to properly integrate all the modules
    back together.
    
## Conceptual Design

    The most critical thing for this project is setting up an environment to test it, so I will first create 
    a private discord server to run testing modules. From here, I would research the discord api to determine 
    how best to keep features modular. I plan on quickly setting up the base module that reads inputs from 
    the discord chat, then having myself and team members work on each of the feature modules based on that 
    first module.

## Background
    
    [https://github.com/CAPark/01-Park-FAADBot]
    
    Regarding the name of the project: the main function of the bot is to work as a ModeratorBot, which
    could simplify into ModBot. The problem with that name is that it is incredibly common and not
    distinguishable from the thousands of other ModBots. So to create the new name, I took the "Mod"
    section and converted the ascii values of letters into binary and then into hex. The final hex 
    number had 4 numbers in it and the letters "F" and "D". I just added the numbers up to get 20, 
    and chose "A" for the remaining to letters since "A" has a hex value of 10, having two adding 
    up to 20. As a result, I mashed together the letters "F", "A", "A", and "D" to get FAADBot.
    

## Group Members

- Christopher Park

- Sungji Kim

- Maamar Bousseloub

- Dawud Baig
