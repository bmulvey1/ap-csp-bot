import discord
import conf

user_commandlist = ['help', 'test', 'rules', 'placeholder']
admin_commandlist = ['help', 'remove', 'rules', 'give_role', 'remove_role', 'placeholder']

async def server_embed(client, message, embed):
    await client.send_message(message.channel, embed=embed)

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


def help_embed():
    help_embed = discord.Embed(title='Help', type='rich', description='Help dialog', color=0x00ff00)
    help_embed.add_field(name='Help', value='!help: Shows this help embed', inline=False)
    help_embed.add_field(name='Test', value='!test: Does nothing', inline=False)
    return help_embed

def rules_embed():
    rules_embed = discord.Embed(title='rules', type='rich', description='Server rules', color=0x00ff00)
    rules_embed.add_field(name='Rule 1', value='rule 1', inline=False)
    rules_embed.add_field(name='Rule 2', value='rule 2', inline=False)
    return rules_embed