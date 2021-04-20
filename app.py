import discord
from datetime import datetime

channel_id = 833184929122484254
join_leave_channel_id = 679927580358344762

intents = discord.Intents.default()
intents.bans = True
intents.invites = True
intents.members = True
intents.guild_messages = True

client = discord.Client(intents=intents)


@client.event
async def on_invite_create(invite):
    await client.wait_until_ready()
    embed_dict = {
        'title': f'Created Invite {invite.id}',
        'timestamp': str(datetime.utcnow()),
        'color': discord.Colour.orange().value,
        'author': {
            'name': f'{invite.inviter} ({invite.inviter.id})',
            'icon_url': str(invite.inviter.avatar_url)
        }
    }
    log_embed = discord.Embed.from_dict(embed_dict)
    logging_channel = client.get_channel(channel_id)
    await logging_channel.send(embed=log_embed)


@client.event
async def on_invite_delete(invite):
    await client.wait_until_ready()
    async for event in invite.guild.audit_logs(limit=1, action=discord.AuditLogAction.invite_delete):
        embed_dict = {
            'title': f'Deleted Invite {invite.id}',
            'timestamp': str(datetime.utcnow()),
            'color': discord.Colour.orange().value,
            'author': {
                'name': f'{event.user.name}#{event.user.discriminator} ({event.user.id})',
                'icon_url': str(event.user.avatar_url)
            }
        }
        log_embed = discord.Embed.from_dict(embed_dict)
        logging_channel = client.get_channel(channel_id)
        await logging_channel.send(embed=log_embed)


@client.event
async def on_member_ban(guild, user):
    await client.wait_until_ready()
    async for event in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
        embed_dict = {
            'title': f'Banned {user} ({user.id})',
            'description': f'**Reason:** {event.reason if event.reason else "Unspecified"}',
            'timestamp': str(datetime.utcnow()),
            'color': discord.Colour.orange().value,
            'footer': {
                'text': event.id
            },
            'thumbnail': {
                'url': str(user.avatar_url)
            },
            'author': {
                'name': f'{event.user.name}#{event.user.discriminator} ({event.user.id})',
                'icon_url': str(event.user.avatar_url)
            }
        }
        log_embed = discord.Embed.from_dict(embed_dict)
        logging_channel = client.get_channel(channel_id)
        await logging_channel.send(embed=log_embed)


@client.event
async def on_member_join(member):
    await client.wait_until_ready()
    embed_dict = {
            'title': f'Joined Server',
            'timestamp': str(datetime.utcnow()),
            'color': discord.Colour.orange().value,
            'author': {
                'name': f'{member} ({member.id})',
                'icon_url': str(member.avatar_url)
            }
        }
    log_embed = discord.Embed.from_dict(embed_dict)
    logging_channel = client.get_channel(join_leave_channel_id)
    await logging_channel.send(embed=log_embed)


@client.event
async def on_member_remove(member):
    await client.wait_until_ready()
    async for event in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
        delta = datetime.utcnow().second - event.created_at.second
        if delta == 0:
            embed_dict = {
                'title': f'Kicked {member} ({member.id})',
                'description': f'**Reason:** {event.reason if event.reason else "Unspecified"}',
                'timestamp': str(datetime.utcnow()),
                'color': discord.Colour.orange().value,
                'footer': {
                    'text': event.id
                },
                'thumbnail': {
                    'url': str(member.avatar_url)
                },
                'author': {
                    'name': f'{event.user.name}#{event.user.discriminator} ({event.user.id})',
                    'icon_url': str(event.user.avatar_url)
                }
            }
            log_embed = discord.Embed.from_dict(embed_dict)
            logging_channel = client.get_channel(channel_id)
            await logging_channel.send(embed=log_embed)
        embed_dict = {
            'title': f'Left Server',
            'timestamp': str(datetime.utcnow()),
            'color': discord.Colour.orange().value,
            'author': {
                'name': f'{member} ({member.id})',
                'icon_url': str(member.avatar_url)
            }
        }
        log_embed = discord.Embed.from_dict(embed_dict)
        logging_channel = client.get_channel(join_leave_channel_id)
        await logging_channel.send(embed=log_embed)


@client.event
async def on_member_unban(guild, user):
    await client.wait_until_ready()
    async for event in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
        embed_dict = {
            'title': f'Unbanned {user} ({user.id})',
            'description': f'**Reason:** {event.reason if event.reason else "Unspecified"}',
            'timestamp': str(datetime.utcnow()),
            'color': discord.Colour.orange().value,
            'footer': {
                'text': event.id
            },
            'thumbnail': {
                'url': str(user.avatar_url)
            },
            'author': {
                'name': f'{event.user.name}#{event.user.discriminator} ({event.user.id})',
                'icon_url': str(event.user.avatar_url)
            }
        }
        log_embed = discord.Embed.from_dict(embed_dict)
        logging_channel = client.get_channel(channel_id)
        await logging_channel.send(embed=log_embed)


@client.event
async def on_message_edit(message_before, message_after):
    await client.wait_until_ready()
    if message_after.author == client.user:
        return
    embed_dict = {
        'title': f'Edited Message ({message_after.id})',
        'timestamp': str(datetime.utcnow()),
        'color': discord.Colour.orange().value,
        'author': {
            'name': f'{message_after.author} ({message_after.author.id})',
            'icon_url': str(message_after.author.avatar_url)
        },
        'fields': [
            {
                'name': 'Before',
                'value': message_before.content,
                'inline': True
            },
            {
                'name': 'After',
                'value': message_after.content,
                'inline': True
            }
        ]
    }
    log_embed = discord.Embed.from_dict(embed_dict)
    logging_channel = client.get_channel(channel_id)
    await logging_channel.send(embed=log_embed)


client.run('NDMwNjA3NzQ0MTg2NDQ5OTIw.WsMYtg.NCUFIgQn3NtKgFa4IQ2zIYJuH8Y')
