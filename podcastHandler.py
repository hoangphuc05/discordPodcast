import discord
import asyncio

from discord import channel
import searchItune
import podcastrss
import requests


class PodcastBot:
    def __init__(self, client: discord.client.Client) -> None:
        self.client = client
        self.prefix = "pd!"

    

    async def messageHandler(self, message):
        
        args = message.content.lower().strip().split()
        #if there is no content in the call
        if len(args) < 1 or message.author.bot or (not args[0].lower().startswith(self.prefix)) or (not hasattr(self, args[0][len(self.prefix):])):
            return

        await getattr(self, args[0][len(self.prefix):])(message, args)

    async def _joinVoice(self, message, user: discord.Member):
        voiceState = user.voice
        if voiceState == None:
            await message.channel.send("You need to be in a voice channel to use this.")    
            return 
        vc = await voiceState.channel.connect()


    async def _selectseries(self, message, podcastList: list):
        '''
        args[1] contains the list of all the podcast
        '''
        index = 0
        response = ""

        if len(podcastList) < 1:
            message.channel.send("Something went wrong, no podcast found!")
            return
        
        msg = await message.channel.send(embed = podcastList[index].getEmbed())
        #msg = await message.channel.send(podcastList[index].title)
        await msg.add_reaction("⬅️")
        await msg.add_reaction("✔️")
        await msg.add_reaction("➡️")

        def reactCheck(reaction: discord.Reaction, user):
            '''
            Check if reaction of a message on a normal channel is belong to that specific message.
            This does not triggered on DM channel
            '''
            if not user.bot and reaction.message.id == msg.id:
                return True
            else:
                return False

        while True:
            try:
                reaction, user = await self.client.wait_for('reaction_add',timeout=60, check= reactCheck)
            except asyncio.TimeoutError:
                break

            try:
                await reaction.remove(user)
            except:
                pass
            if str(reaction) == '➡️':
                index += 1
            elif str(reaction) == "⬅️":
                index -= 1
            if index < 0:
                index = len(podcastList) -1
            elif index > len(podcastList) -1:
                index = 0

            #check for select emo
            if str(reaction) == '✔️':
                await self._joinVoice(message, user)
                pass


            await msg.edit(embed = podcastList[index].getEmbed())

    async def search(self, message, args):
        '''
        search a podcast using name/anything? as the parameter
        '''
        index = 0
        searchResult = searchItune.searchPodcast(str(message.content[len(args[0])+1:]))
        response = ""
        if len(searchResult) < 1:
            message.channel.send("No podcast found!")
            return

        for i in range(len(searchResult)):
            response+=f"{i+1}. {searchResult[i].collectionName}\n"
        
        msg = await message.channel.send(f"Search result:```{response}```", embed = searchResult[index].getEmbed())
        await msg.add_reaction("⬅️")
        await msg.add_reaction("✔️")
        await msg.add_reaction("➡️")

        def reactCheck(reaction: discord.Reaction, user):
            '''
            Check if reaction of a message on a normal channel is belong to that specific message.
            This does not triggered on DM channel
            '''
            if not user.bot and reaction.message.id == msg.id:
                return True
            else:
                return False
            
        while True:
            try:
                reaction, user = await self.client.wait_for('reaction_add',timeout=60, check= reactCheck)
            except asyncio.TimeoutError:
                break

            try:
                await reaction.remove(user)
            except:
                pass
            if str(reaction) == '➡️':
                index += 1
            elif str(reaction) == "⬅️":
                index -= 1
            if index < 0:
                index = len(searchResult) -1
            elif index > len(searchResult) -1:
                index = 0
            
            #check for select emo
            if str(reaction) == '✔️':
                await self._selectseries(message,searchResult[index].podcastSeries.eps)
                pass


            await msg.edit(embed = searchResult[index].getEmbed())
        pass