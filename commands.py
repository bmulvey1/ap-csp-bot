import discord
import conf

user_commandlist = ['help', 'test', 'rules', 'placeholder']
admin_commandlist = ['help', 'remove', 'rules', 'give_role', 'remove_role', 'placeholder']


async def remove(client, message, num):
    if num > 100:
        msg =  '{0.author.mention}, that isn\'t a valid argument. You can\'t remove more than 100 messages at once.'.format(message)
        await client.send_message(message.channel, msg)
        return
    else:
        try:
            await client.purge_from(message.channel, limit=num)
        except:
            if conf.DEBUG: print ('Remove failed.')
            else:
                pass
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
    if conf.DEBUG:
        print(role_name)
        print(member_name)
        print(role)
        print(user)
        print(message.content.split(' ', 3))


async def server_embed(client, message, embed):
    await client.send_message(message.channel, embed=embed)

def create_embed(type):
    if type == 'help':
        embed = discord.Embed(title='Help', type='rich', description='Help dialog', color=0x00ff00)
        embed.add_field(name='Help', value='!help: Shows this help embed', inline=False)
        embed.add_field(name='Test', value='!test: Does nothing', inline=False)
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
        embed.add_field(name='Give role', value='!give_role *user* *role* : Gives specified role to specified user',inline=False)
        return embed