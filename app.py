import discord
from discord.ext import commands
from datetime import datetime

logging_channel_id = 833184929122484254

intents = discord.Intents.default()
intents.bans = True
intents.invites = True
intents.members = True
intents.guild_messages = True

client = commands.Bot(command_prefix='!', intents=intents)


async def send_to_logging_channel(embed_dict):
    log_embed = discord.Embed.from_dict(embed_dict)
    logging_channel = client.get_channel(logging_channel_id)
    await logging_channel.send(embed=log_embed)


@client.command()
async def ban(ctx):
    await ctx.send(content=ctx.message.content)


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
        await send_to_logging_channel(embed_dict)


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
            await send_to_logging_channel(embed_dict)


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
        await send_to_logging_channel(embed_dict)


client.run('NDMwNjA3NzQ0MTg2NDQ5OTIw.WsMYtg.NCUFIgQn3NtKgFa4IQ2zIYJuH8Y')
