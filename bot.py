import os
import time
import discord
from dotenv import load_dotenv
from message_handler import RequestMessageHandler

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):

    user_message_lower = message.content.lower()
    message_handler = RequestMessageHandler(message)
    await message.channel.send(message_handler.response)

client.run(TOKEN)


