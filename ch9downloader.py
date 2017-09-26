#!/usr/bin/python

import os, urllib, feedparser, math, sys


BASE_FEED = "https://s.ch9.ms/{type}/{name}/RSS/{quality}"

# There are mutliple types of feeds, "Events" or "Shows"
# Event example - http://channel9.msdn.com/Shows/Azure-Friday/RSS/mp4high
# Show example - https://s.ch9.ms/Events/dotnetconf/2017/RSS/mp4high
TYPE = "Events"
NAME = "dotnetconf/2017" # "Azure-Friday" or "dotnetconf/2017"
QUALITY = "mp3" # "mp4high" / "mp4" / "mp3", didn't ssucceded to get mp4mid
FEED = BASE_FEED.format(type=TYPE, name=NAME, quality=QUALITY)
print(FEED)

def handleunicode(title):
    return title.encode(encoding='ascii',errors='replace')

def tofile(title):
    title = title.replace("?", "-").replace("$", "-").replace("/", "-").replace(":", "-").replace(",", "-").replace("<", "").replace(">","")
    return title + ".mp4"

def getsessions():
    '''
    This requires feedparser to be loaded. E.g (pip install feedparser)
    '''
    try:	
        url = FEED
        rss = feedparser.parse(url)
        
        if not os.path.exists(NAME):
            os.makedirs(NAME)

        return [(os.path.join(NAME, tofile(handleunicode(e.title))), e.enclosures[0].href) for e in rss.entries]
    except Exception as ex:
        print("Error reading Session RSS feed")
        raise

def reportprogress(blocksRead, blockSize, totalSize):
    downloaded = blocksRead * blockSize
    complete = math.ceil((downloaded / (totalSize * 1.0)) * 100)

    sys.stdout.write("{0:.0f}%".format(complete))
    sys.stdout.write("\r")
    sys.stdout.write("")
    sys.stdout.flush()


def download(sessions):
    sessions.sort()
    for s in sessions:
        fname = s[0]
        url = s[1]
        if not os.path.exists(fname):
            try:
                print(fname)
                urllib.urlretrieve(url, fname, reportprogress)
            except Exception as ex:
                print("Unable to download %s, exception: %s" % (url, ex))
        else:
            print("%s already exists... pass" % fname)

if __name__ == '__main__':
    sessions = getsessions()
    print("Found %d sessions..." % len(sessions))
    download(sessions)