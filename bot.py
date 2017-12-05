import discord
import re
import conf
import asycio

client = Discord.client()

@client.event
    async def on_ready():
        print ('Logged in as')
        print (client.user.name)
        print (client.user.id)
        print('-----')

@client.event
async def on_message(message): #happens when a message is sent in any channel by any user
    print (message.content)
    print ("sent by: " + message.author)    #placeholder
