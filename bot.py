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
async def on_message(message): #happens when a message is sent in any channel by any user
    commandPossible = False
    help_embed = commands.help_embed()
    rules_embed = commands.rules_embed()
    i = 0
    print (message.content)
    print ("sent by: " + str(message.author) + " in channel " + str(message.channel))    #placeholder
    role_names = [role.name for role in message.author.roles] #create list of roles of author
    if message.author == client.user:
        pass
    else:
        if str(message.content[0]) == str(conf.symbol):     #check for valid commands
            if ('Commander' in role_names):
                print (str(message.author) + ' is a commander, admin commands allowed') #can run more powerful commands
                if conf.DEBUG: print (role_names) #For debugging
                for command in commands.admin_commandlist:
                    if message.content.find(command) != -1: #make sure the command is valid
                        commandPossible = True
                        if conf.DEBUG: print(command)
                    else:
                        if commandPossible == True:
                            await client.send_message(message.channel, 'Recieved command from admin user')
                            if message.content.find('help') != -1:
                                await commands.server_embed(client, message, help_embed)
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


                        else:
                            pass
                else:
                    commandPossible = False
                    msg = '{0.author.mention}, that isn\'t a valid command. Try running !help.'.format(message)
                    await client.send_message(message.channel, msg)

            else:
                print (str(message.author) + " is not a commander, only user commands allowed") #can only run less powerful commands
                print (role_names) #For debugging
                for command in commands.user_commandlist:
                    if message.content.find(command) != -1: #make sure the command is valid
                        commandPossible = True
                    else:
                        if commandPossible == True:
                            await client.send_message(message.channel, 'Recieved command from non-admin user')
                            if message.content.find('help') != -1:
                              await commands.server_help(client, message, help_embed)
                            return
                        else:
                            i=i+1
                            print('Incremented i'+str(i))
                else:
                    commandPossible = False
                    msg = '{0.author.mention}, that isn\'t a valid command. Try running !help.'.format(message)
                    await client.send_message(message.channel, msg)
        else:
            pass


client.run(conf.key)
