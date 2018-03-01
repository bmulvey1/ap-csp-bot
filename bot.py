import discord
import re
import conf
import asyncio
import commands

client = discord.Client()

@client.event
async def on_ready():
    print ('Logged in as')
    print (client.user.name)
    print (client.user.id)
    print (conf.symbol + " is the command symbol")
    print('-----')

@client.event
async def on_message(message): #runs when a message is sent in any channel by any user
    commandPossible = False
    help_embed = commands.create_embed('help')
    rules_embed = commands.create_embed('rules')
    admin_help = commands.create_embed('admin_help')
    role_names = [role.name for role in message.author.roles] #create list of roles of author
    if message.author == client.user: #ignore messages from bot
        pass
    else:
        print(message.content)
        print("sent by: " + str(message.author) + " in channel " + str(message.channel))
        if str(message.content[0]) == str(conf.symbol):     #check for valid commands
            if ('Commander' in role_names):
                if conf.DEBUG: print (str(message.author)+ ' is a commander, admin commands allowed') #can run more powerful commands
                if conf.DEBUG: print (role_names) #For debugging
                for command in commands.admin_commandlist:
                    if message.content.find(command) != -1: #make sure the command is valid
                        commandPossible = True
                        if conf.DEBUG: print(command)
                    else:
                        if commandPossible == True:
                            if message.content.find('help') != -1:
                                await commands.server_embed(client, message, admin_help)
                                return

                            elif message.content.find('rules') != -1:
                                await commands.server_embed(client, message, rules_embed)
                                return

                            elif message.content.find('remove') != -1:
                                if message.content.find('-') != -1:
                                    msg = '{0.author.mention}, you can\'t remove negative messages.'.format(message)
                                    await client.send_message(message.channel, msg)
                                else:
                                    try:
                                        num = int(re.search('-?\d+', message.content).group())
                                    except:
                                        msg = '{0.author.mention}, that isn\'t a valid number of messages.'.format(message)
                                        await client.send_message(message.channel, msg)
                                        return
                                    await commands.remove(client, message, num)
                                return

                            elif message.content.find('give_role') != -1:
                                await commands.give_role(client, message)
                                return

                            elif message.content.find('take_role') != -1:
                                await commands.remove_role(client, message)
                                return

                        else:
                            pass
                else:
                    commandPossible = False
                    msg = '{0.author.mention}, that isn\'t a valid command. Try running !help.'.format(message) #tell message author that the command is invalid
                    await client.send_message(message.channel, msg)

            else:
                print (str(message.author) + " is not a commander, only user commands allowed") #can only run less powerful commands
                if conf.DEBUG: print (role_names) #For debugging
                if conf.DEBUG: print (commands.user_commandlist)
                for command in commands.user_commandlist:
                    if message.content.find(command) != -1: #make sure the command is valid
                        commandPossible = True
                    else:
                        if commandPossible == True:
                            if message.content.find('help') != -1:
                              await commands.server_embed(client, message, help_embed)
                              return

                            elif message.content.find('rules') != -1:
                                await commands.server_embed(client, message, rules_embed)
                                return

                        else:
                           pass
                else:
                    commandPossible = False
                    msg = '{0.author.mention}, that isn\'t a valid command. Try running !help.'.format(message)  #tell message author that the command is invalid
                    await client.send_message(message.channel, msg)
        else:
            pass


client.run(conf.key)
