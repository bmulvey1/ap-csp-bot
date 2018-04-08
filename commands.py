import discord # the discordpy library was created by https://github.com/Rapptz/; licenced under the MIT license
import conf # file for configuration
import time # stock Python module

user_commandlist = ['help', 'test', 'rules','poll', 'placeholder'] # List of commands that normal users can use
admin_commandlist = ['help', 'remove', 'rules', 'give_role', 'take_role', 'poll', 'placeholder'] # List of commands that admins can use


async def remove(client, message, num): # Removes specified number of messages from a specified channel
    if num > 100:
        msg =  '{0.author.mention}, that isn\'t a valid argument. You can\'t remove more than 100 messages at once.'.format(message) # Discord allows a maximum of 100 messages to be removed at once
        await client.send_message(message.channel, msg)
        return
    else:
        try:
            await client.purge_from(message.channel, limit=num) # removes messages from channel
        except:
            if conf.DEBUG:
                print ('Remove failed.')
                msg = "Failed to remove messages"
                await client.send_message(message.channel, msg)
                return
            else:
                print('Removed {} messages from {.channel}'.format(num, message))
                return


async def give_role(client, message): # Gives a specified role to a specified user
    user = message.content.split(' ', 3)[1] # Get desired username
    dest_role = message.content.split(' ', 3)[2] # Get desired role
    server_roles = message.server.roles # List of Role objects in a server
    server_members = message.server.members # List of Member objects in a server
    role_name = {}
    member_name = {}
    for role in server_roles:
        role_name[role.name] = role # Associate a role name with a Role object
    for member in server_members:
        member_name[member.display_name] = member # Associate a display name with a Member object
    if (user not in member_name) and (role not in role_name): # Check if neither member or role is valid
        msg = '{0.author.mention}, that isn\'t a valid username or role.'.format(message)
        await client.send_message(message.channel, msg)
    elif user not in member_name: # Check if only member is incorrect
        msg = '{0.author.mention}, that isn\'t a valid username.'.format(message)
        await client.send_message(message.channel, msg)
    elif dest_role not in role_name: # Check if only role is incorrect
        msg = '{0.author.mention}, that isn\'t a valid role.'.format(message)
        await client.send_message(message.channel, msg)
    else: # Give role to the user
        await client.add_roles(member_name[user], role_name[dest_role])
        msg = 'Gave role {0} to {1}'.format(dest_role, user)
        await client.send_message(message.channel, msg)
        msg1 = '{0.author} gave role {1} to {2}'.format(message, dest_role, user)
        print (msg1)
    if conf.DEBUG: # Print details if debugging is enabled
        print(role_name)
        print(member_name)
        print(role)
        print(user)
        print(message.content.split(' ', 3))
        print('Gave roles')

async def remove_role(client, message): # Take a specified role from a specified user
    user = message.content.split(' ', 3)[1] # Get desired username
    dest_role = message.content.split(' ', 3)[2] # Get desired role
    server_roles = message.server.roles #
    server_members = message.server.members
    role_name = {}
    member_name = {}
    for role in server_roles:
        role_name[role.name] = role
    for member in server_members:
        member_name[member.display_name] = member
    if (user not in member_name) and (role not in role_name): # Check if neither member or role is valid
        msg = '{0.author.mention}, that isn\'t a valid username or role.'.format(message)
        await client.send_message(message.channel, msg)
    elif user not in member_name: # Check if only member is incorrect
        msg = '{0.author.mention}, that isn\'t a valid username.'.format(message)
        await client.send_message(message.channel, msg)
    elif dest_role not in role_name: # Check if only role is incorrect
        msg = '{0.author.mention}, that isn\'t a valid role.'.format(message)
        await client.send_message(message.channel, msg)
    else: # Remove role from user
        try:
            await client.remove_roles(member_name[user], role_name[dest_role]) # Fails if user does not have the role specified
        except:
            msg = 'That user does not have the specified role'
            await client.send_message(message.channel, msg)
        msg = 'Removed role {0} from {1}'.format(dest_role, user)
        await client.send_message(message.channel, msg)
        msg1 = '{0.author} took role {1} from {2}'.format(message, dest_role, user)
        print(msg1)
    if conf.DEBUG: # Print details if debugging is enabled
        print(role_name)
        print(member_name)
        print(role)
        print(user)
        print(message.content.split(' ', 3))
        print('Took roles')


async def server_embed(client, message, embed): # Send embed, which is passed in bot.py
    await client.send_message(message.channel, embed=embed)

def create_embed(type): # Create embed based on option passed in bot.py
    if type == 'help':
        embed = discord.Embed(title='Help', type='rich', description='Help dialog', color=0x00ff00)
        embed.add_field(name='Help', value='!help: Shows this help embed', inline=False)
        embed.add_field(name='Test', value='!test: Does nothing', inline=False)
        embed.add_field(name="Poll", value='!poll~ *text*~ *emoji*~ *emoji*: Creates a poll with 2 emoji as vote options', inline=False)
        return embed
    elif type == 'rules':
        embed = discord.Embed(title='rules', type='rich', description='Server rules', color=0x00ff00)
        embed.add_field(name='Rule 1', value='rule 1', inline=False)
        embed.add_field(name='Rule 2', value='rule 2', inline=False)
        return embed
    elif type == 'admin_help':
        embed = discord.Embed(title='Help', type='rich', description='Help dialog', color=0x00ff00)
        embed.add_field(name='Help', value='!help: Shows this help embed', inline=False)
        embed.add_field(name='Test', value='!test: Does nothing', inline=False)
        embed.add_field(name='Remove', value='!remove *messages* : Removes specified number of messages, up to 100', inline=False)
        embed.add_field(name='Give role', value='!give_role *user* *role* : Gives specified role to specified user', inline=False)
        embed.add_field(name='Remove role', value='!remove_role *user* *role* : Removes specified role from specified user', inline=False)
        embed.add_field(name="Poll", value='!poll~ *text*~ *emoji*~ *emoji*: Creates a poll with 2 emoji as vote options', inline=False)
        return embed

async def poll(client, message): # Create poll in a poll channel
    server_channels = message.server.channels # Get all Channel objects in server
    channels = {}
    for channel in server_channels:
        channels[channel.name] = channel # Associate channel name with Channel object
    try: # Lines 131-148 check validity of data in message
        text = message.content.split('~ ', 4)[1]
    except:
        msg = "Please provide all fields necessary"
        await client.send_message(message.channel, msg)
        return
    try:
        emoji1 = message.content.split('~ ', 4)[2]
    except:
        msg = "Please provide all fields necessary"
        await client.send_message(message.channel, msg)
        return
    try:
        emoji2 = message.content.split('~ ', 4)[3]
    except:
        msg = "Please provide all fields necessary"
        await client.send_message(message.channel, msg)
        return
    try: # Check if another poll with the same text exists already
        bot_message1 = discord.utils.get(client.messages, content=text, author=client.user, channel=channels['polls'])
    except: # Previous line throws an exception if the channel does not exist
        msg = "{0.author.mention}, the `polls` channel may not exist, please contact a server admin or create the channel".format(message)
        await client.send_message(message.channel, msg)
        return
    if bot_message1 != None: # Tell user if a poll with the same text already exists
        print(bot_message1)
        msg = "A poll with that text already exists, try looking at that poll or word yours differently"
        await client.send_message(message.channel, msg)
        return
    if conf.DEBUG: print(channels)
    await client.send_message(channels['polls'], text)
    time.sleep(4) # Wait for message to be sent
    bot_message = discord.utils.get(client.messages, content=text, author=client.user, channel=channels['polls'])
    await client.add_reaction(bot_message, emoji1) # Add emoji to bot message
    await client.add_reaction(bot_message, emoji2) # Add other emoji to bot message
    return