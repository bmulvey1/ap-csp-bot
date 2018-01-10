user_commandlist = ['help', 'test']
admin_commandlist = ['help', 'remove', 'give_role', 'remove_role']

async def server_help(client, message, help_embed):
    await client.send_message(message.channel, embed=help_embed)