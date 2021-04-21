import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from datetime import datetime


logging_channel_id = 833184929122484254
guild_ids = [679923472561995801]

intents = discord.Intents.default()
intents.bans = True
intents.invites = True
intents.members = True
intents.guild_messages = True

client = discord.Client(intents=intents)
slash = SlashCommand(client, sync_commands=True)


async def send_to_logging_channel(embed_dict):
    log_embed = discord.Embed.from_dict(embed_dict)
    logging_channel = client.get_channel(logging_channel_id)
    await logging_channel.send(embed=log_embed)


@slash.slash(name='ban', description='Bans a specified member from the server.', guild_ids=guild_ids, options=[
    create_option(name="member", description="The member you want to ban.", option_type=6, required=True),
    create_option(name="reason", description="The reason for the ban.", option_type=3, required=False)])
async def ban(ctx, member: discord.Member, reason: discord.Message = None):
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await ctx.send(content=f'Successfully banned **{member}** for reason: {reason if reason else "None"}')
    else:
        await ctx.send(content='Sorry, but you do not have sufficient permissions to perform this action.')


@slash.slash(name='unban', description='Unbans a specified member from the server.', guild_ids=guild_ids, options=[
    create_option(name="member", description="The member you want to unban.", option_type=6, required=True),
    create_option(name="reason", description="The reason for the unban.", option_type=3, required=False)])
async def ban(ctx, member: discord.Member, reason: discord.Message = None):
    if ctx.author.guild_permissions.ban_members:
        await member.unban(reason=reason)
        await ctx.send(content=f'Successfully unbanned **{member}** for reason: {reason if reason else "None"}')
    else:
        await ctx.send(content='Sorry, but you do not have sufficient permissions to perform this action.')


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
