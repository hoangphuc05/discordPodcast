import xml.etree.ElementTree as ET
import requests
import discord
import html2markdown


ns = {'itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd'}

class PodcastEp:
    def __init__(self, item) -> None:
        global ns
        try:
            self.title = item.find('./title').text
        except Exception:
            self.title = "No title found"

        try:
            self.pubdate = item.find('./pubDate').text
        except Exception:
            self.pubdate = "No date found"

        try:
            self.duration = item.find('./itunes:duration', ns).text
        except Exception:
            self.duration = "No duration found"

        try:
            self.description = html2markdown.convert(item.find('./description').text)[:1023]
        except Exception:
            self.description = "No description found"

        try:
            self.artUrl = item.find('./itunes:image', ns).attrib['href']
        except Exception:
            self.artUrl = "https://www.example.com"

        try:
            self.url = item.find('./enclosure').attrib["url"]
        except Exception:
            self.url = ""
        
        
        
        
        
        self.root = item

    def getEmbed(self):
        embedVar = discord.Embed(title = self.title)
        embedVar.set_thumbnail(url = self.artUrl)
        embedVar.add_field(inline=True, name="Episode title", value= self.title)
        embedVar.add_field(inline=True, name="Duration", value= self.duration)
        embedVar.add_field(inline=False, name="Description", value= self.description)
        return embedVar

class PodcastSeries:
    def __init__(self, url:str) -> None:
        global ns

        r = requests.get(url)
        root = ET.fromstring(r.content)
        # print(list(root.find('./channel').iter())[0:5])
        try:
            self.title = root.find('./channel/title').text
        except Exception:
            self.title = "No title found"
            pass

        try:
            self.lastUpdate = root.find('./channel/lastBuildDate').text
        except Exception:
            self.lastUpdate = "No date found"
        try:
            self.description = root.find('./channel/description').text
        except Exception:
            self.description = "No description found"
        try:
            self.artUrl = root.find('./channel/itunes:image', ns).attrib['href']
        except Exception:
            self.artUrl = "https://www.example.com"
                
        
        self.root = root
        self.eps = []
        try:
            for item in root.findall('./channel/item'):
                self.eps.append(PodcastEp(item))
        except:
            pass
        #self.podcastList = podcastList
    def getEmbed(self):
        embedVar = discord.Embed(title = self.title)
        embedVar.set_thumbnail(url = self.artUrl)
        embedVar.add_field(inline=True, name="Title", value= self.title)
        embedVar.add_field(inline=True, name="Last update", value= self.lastUpdate)
        embedVar.add_field(inline=False, name="Description", value= self.description)
        return embedVar

# def parsePodcast(url: str):
#     pass
# r = requests.get("https://nosleeppodcast.libsyn.com/rss")



# # tree = ET.parse(r.content)
# # root = tree.getroot
# root = ET.fromstring(r.content)


# # title = root.find('./channel/title')
# # lastUpdate = root.find('./channel/lastbuilddate')
# # descripton = root.find('./channel/description')
# # imgUrl = root.find('./channel/itunes:image', ns)

# noSleep = PodcastSeries(root)

# print(noSleep.imgUrl.attrib['href'])

# items = {}
# for item in root.findall('./channel/item'):
#     for child in item:
#         if child.tag == 'enclosure':
#             pass
#             #print(child.attrib['url'])
# print(root.attrib['version'])

a = PodcastSeries("https://nosleeppodcast.libsyn.com/rss")
print(a.title)
print(a.eps[0].artUrl)