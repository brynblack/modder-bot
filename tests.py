import discord

logging_channel_id = 833184929122484254

intents = discord.Intents.default()
intents.bans = True
intents.invites = True
intents.members = True
intents.guild_messages = True

client = discord.Client(intents=intents)


async def test_variables():
    try:
        await client.fetch_channel(logging_channel_id)
    except:
        raise AssertionError


@client.event
async def on_ready():
    await test_variables()


client.run('NDMwNjA3NzQ0MTg2NDQ5OTIw.WsMYtg.NCUFIgQn3NtKgFa4IQ2zIYJuH8Y')
