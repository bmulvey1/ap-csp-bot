user_commandlist = ['help', 'test']
admin_commandlist = ['help', 'remove', 'give_role', 'remove_role']

async def server_help(client, message, help_embed):
    await client.send_message(message.channel, embed=help_embed)

async def remove(client, message, num):
    if num > 100:
        msg =  '{0.author.mention}, that isn\'t a valid argument. You can\'t remove more than 100 messages at once.'.format(message)
        await client.send_message(message.channel, msg)
        return
    else:
        try:
            await client.purge_from(message.channel, limit=num)
        except:
            print ('Remove failed.')
        print('Removed {} messages from {.channel}'.format(num, message))
