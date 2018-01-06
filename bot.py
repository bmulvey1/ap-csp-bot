import discord
import re
import conf
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print ('Logged in as')
    print (client.user.name)
    print (client.user.id)
    print (conf.symbol + " is the command symbol")
    print('-----')

@client.event
async def on_message(message): #happens when a message is sent in any channel by any user
    print (message.content)
    print ("sent by: " + str(message.author) + " in channel " + str(message.channel))    #placeholder
    role_names = [role.name for role in message.author.roles] #create list of roles of author
    if str(message.content[0]) == str(conf.symbol):     #check for valid commands
        if ('Commander' in role_names):
            print (str(message.author) + " is a commander, admin commands allowed") #can run more powerful commands
            print (role_names)
        else:
            print (str(message.author) + " is not a commander, only user commands allowed") #can run more powerful commands
            print (role_names)
    else:
        pass
client.run(conf.key)
