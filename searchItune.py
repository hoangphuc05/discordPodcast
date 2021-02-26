from typing import List
import requests
import json
import discord
import podcastrss


class SearchResult:
    def __init__(self, artistName, collectionName, trackName, feedUrl, artWork, trackCount, collectionID) -> None:
        self.artistName = artistName
        self.collectionName = collectionName
        self.trackName = trackName
        self.feedUrl = feedUrl
        self.artWork = artWork
        self.trackCount = trackCount
        self.collectionID = collectionID
        self.podcastSeries = podcastrss.PodcastSeries(self.feedUrl)

    def getEmbed(self):
        # embedVar = discord.Embed(title = self.collectionName)
        # embedVar.set_thumbnail(url = self.artWork)
        # embedVar.add_field(inline=False, name="Podcast name", value= self.collectionName)
        # embedVar.add_field(inline=False, name="Number of episode", value= self.trackCount)

        
        embedVar = self.podcastSeries.getEmbed()
        embedVar.add_field(inline=True, name="Number of episode", value= self.trackCount)

        return embedVar


def searchPodcast(term: str) -> list:
    baseUrl = "https://itunes.apple.com/search"
    

    params = {'term':term,
            'media': 'podcast',
            'entity': 'podcast',
            'attribute': 'titleTerm'}

    r = requests.get(baseUrl, params= params)
    data = r.json()

    print(data['resultCount'])
    podcastList = []
    #parse the result to usable form
    for podcast in data['results']:
        try:
            podcastList.append(SearchResult(podcast['artistName'], podcast['collectionName'], podcast['trackName'], podcast['feedUrl'],podcast['artworkUrl100'], podcast['trackCount'], podcast['collectionId']))
            print(podcast["trackName"])
        except:
            pass

    return podcastList

def searchID(id:str) -> list:
    baseUrl = "https://itunes.apple.com/search"

    params = {
        'term' : id,
        'media': 'podcast'
    }
    r = requests.get(baseUrl, params= params)
    data = r.json()
    podcastList = []
    #parse the result to usable form
    for podcast in data['results']:
        try:
            podcastList.append(SearchResult(podcast['artistName'], podcast['collectionName'], podcast['trackName'], podcast['feedUrl'],podcast['artworkUrl100'], podcast['trackCount'], podcast['collectionId']))
            print(podcast["trackName"])
        except:
            pass