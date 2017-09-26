#!/usr/bin/python
import os
import urllib
import feedparser
import math
import sys
import argparse
import re

BASE_FEED = "https://s.ch9.ms/{type}/{name}/RSS/{quality}"

def handleunicode(title):
    return title.encode(encoding='ascii',errors='replace')

def tofile(title, file_extension):
    title = title.replace("?", "-").replace("$", "-").replace("/", "-").replace(":", "-").replace(",", "-").replace("<", "").replace(">","")
    return title + file_extension

def getsessions(url, name, file_extension):
    '''
    This requires feedparser to be loaded. E.g (pip install feedparser)
    '''
    try:	
        rss = feedparser.parse(url)
        
        if not os.path.exists(name):
            os.makedirs(name)

        return [(os.path.join(name, tofile(handleunicode(e.title), file_extension)), e.enclosures[0].href) for e in rss.entries]
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

def main(url, name, file_extension):
    sessions = getsessions(url, name, file_extension)
    print("Found %d sessions..." % len(sessions))
    download(sessions)

def run(type, name, quality):
    url = BASE_FEED.format(type=type, name=name, quality=quality)
    print("Current feed: " + url)
    file_extension = "." + quality[:3]

    main(url, name, file_extension)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", choices=["Events", "Shows"],
                                        help="There are two types of series: 'Events' or 'Shows'",
                                        required=True)
    parser.add_argument("-n", "--name", help="""The name of the series to download: """ \
                                            """'Azure-Friday' (For a Show) or 'dotnetconf/2017'""" \
                                            """(For an event, you must specify the year)""",
                                            required=True)
    parser.add_argument("-q", "--quality", choices=["mp4high", "mp4", "mp3"],
                        help="'mp4high' (high quality) or 'mp4' (low quality) or 'mp3' (just mp3, sound without video)",
                        required=True)
    args = parser.parse_args(sys.argv[1:])

    # validate if it is an event, that the name pattern is 'confname/year'
    pattern = '\w+/\d{4}'
    if args.type == "Events" and not re.match(pattern, args.name):
        parser.error("For events, the name pattern must be: '%s', for example: 'dotnetconf/2017'" % pattern)

    return args

if __name__ == '__main__':
    args = get_args()

    run(args.type, args.name, args.quality)