import discord
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('discord')

class ModderBot(discord.Client):
    async def on_ready(self):
        logger.info(f'authenticated as {self.user}')

intents = discord.Intents.default()
client = ModderBot(intents=intents)

client.run(os.getenv('BOT_TOKEN'))
