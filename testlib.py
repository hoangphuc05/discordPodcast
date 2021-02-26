import podcastparser
import urllib

feedurl ="https://nosleeppodcast.libsyn.com/rss"

parsed = podcastparser.parse(feedurl, urllib.urlopen(feedurl))

# parsed is a dict
import pprint
pprint.pprint(parsed)