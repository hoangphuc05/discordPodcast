import discord
from dotenv import load_dotenv
import os
import searchItune
import asyncio
import importlib

import podcastHandler

load_dotenv()
token = os.getenv("DISCORD_TOKEN")


client = discord.Client()

podcastClient = podcastHandler.PodcastBot(client)

class PodcastBot(discord.Client):
    @client.event
    async def on_ready(self):
        print("This bot is read?")

    @client.event
    async def on_message(self, message):
        if message.author == client.user:
            return
        await podcastClient.messageHandler(message)

clients = PodcastBot()
importlib.reload(podcastHandler)
podcastClient = podcastHandler.PodcastBot(clients)


clients.run(token)