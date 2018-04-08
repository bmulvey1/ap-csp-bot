import discord # the discordpy library was created by https://github.com/Rapptz/; licenced under the MIT license
import conf # file for configuration
import time # stock Python module

user_commandlist = ['help', 'test', 'rules','poll', 'placeholder']
admin_commandlist = ['help', 'remove', 'rules', 'give_role', 'take_role', 'poll', 'placeholder']


async def remove(client, message, num):
    if num > 100:
        msg =  '{0.author.mention}, that isn\'t a valid argument. You can\'t remove more than 100 messages at once.'.format(message)
        await client.send_message(message.channel, msg)
        return
    else:
        try:
            await client.purge_from(message.channel, limit=num)
        except:
            if conf.DEBUG:
                print ('Remove failed.')
                msg = "Failed to remove messages"
                await client.send_message(message.channel, msg)
            else:
                return
        print('Removed {} messages from {.channel}'.format(num, message))

async def give_role(client, message):
    user = message.content.split(' ', 3)[1]
    dest_role = message.content.split(' ', 3)[2]
    server_roles = message.server.roles
    server_members = message.server.members
    role_name = {}
    member_name = {}
    for role in server_roles:
        role_name[role.name] = role
    for member in server_members:
        member_name[member.display_name] = member
    if (user not in member_name) and (role not in role_name):
        msg = '{0.author.mention}, that isn\'t a valid username or role.'.format(message)
        await client.send_message(message.channel, msg)
    elif user not in member_name:
        msg = '{0.author.mention}, that isn\'t a valid username.'.format(message)
        await client.send_message(message.channel, msg)
    elif dest_role not in role_name:
        msg = '{0.author.mention}, that isn\'t a valid role.'.format(message)
        await client.send_message(message.channel, msg)
    else:
        await client.add_roles(member_name[user], role_name[dest_role])
        msg = 'Gave role {0} to {1}'.format(dest_role, user)
        await client.send_message(message.channel, msg)
        msg1 = '{0.author} gave role {1} to {2}'.format(message, dest_role, user)
        print (msg1)
    if conf.DEBUG:
        print(role_name)
        print(member_name)
        print(role)
        print(user)
        print(message.content.split(' ', 3))
        print('Gave roles')

async def remove_role(client, message):
    user = message.content.split(' ', 3)[1]
    dest_role = message.content.split(' ', 3)[2]
    user_roles = message.author.roles
    server_members = message.server.members
    role_name = {}
    member_name = {}
    for role in user_roles:
        role_name[role.name] = role
    for member in server_members:
        member_name[member.display_name] = member
    if (user not in member_name) and (role not in role_name):
        msg = '{0.author.mention}, that isn\'t a valid username or role.'.format(message)
        await client.send_message(message.channel, msg)
    elif user not in member_name:
        msg = '{0.author.mention}, that isn\'t a valid username.'.format(message)
        await client.send_message(message.channel, msg)
    elif dest_role not in role_name:
        msg = '{0.author.mention}, that isn\'t a valid role.'.format(message)
        await client.send_message(message.channel, msg)
    else:
        await client.remove_roles(member_name[user], role_name[dest_role])
        msg = 'Removed role {0} from {1}'.format(dest_role, user)
        await client.send_message(message.channel, msg)
        msg1 = '{0.author} took role {1} from {2}'.format(message, dest_role, user)
        print(msg1)
    if conf.DEBUG:
        print(role_name)
        print(member_name)
        print(role)
        print(user)
        print(message.content.split(' ', 3))
        print('Took roles')


async def server_embed(client, message, embed):
    await client.send_message(message.channel, embed=embed)

def create_embed(type):
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

async def poll(client, message):
    server_channels = message.server.channels
    channels = {}
    for channel in server_channels:
        channels[channel.name] = channel
    try:
        text = message.content.split('~ ', 4)[1]
    except:
        msg = "Please provide all fields necessary"
        await client.send_message(message.channel, msg)
        return
    try:
        bot_message1 = discord.utils.get(client.messages, content=text, author=client.user, channel=channels['polls'])
    except:
        msg = "{0.author.mention}, the `polls` channel may not exist, please contact a server admin or create the channel".format(message)
        await client.send_message(message.channel, msg)
        return
    if bot_message1 != None:
        print(bot_message1)
        msg = "A poll with that text already exists, try looking at that poll or word yours differently"
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
    server_emoji = message.server.emojis
    emojis = {}
    for emoji in server_emoji:
        emojis[emoji.name] = emoji
    print(channels)
    print(emojis)
    await client.send_message(channels['polls'], text)
    time.sleep(4)
    bot_message = discord.utils.get(client.messages, content=text, author=client.user, channel=channels['polls'])
    await client.add_reaction(bot_message, emoji1)
    await client.add_reaction(bot_message, emoji2)
    return