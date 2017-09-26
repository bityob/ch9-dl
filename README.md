# ch9-dl
Simple to use [channel9](https://channel9.msdn.com/) downloader.

## Usage

```bash
$ python ./ch9-dl.py -h
usage: ch9-dl.py [-h] -t {Events,Shows} -n NAME -q {mp4high,mp4,mp3}

optional arguments:
  -h, --help            show this help message and exit
  -t {Events,Shows}, --type {Events,Shows}
                        There are two types of series: 'Events' or 'Shows'
  -n NAME, --name NAME  The name of the series to download: 'Azure-Friday'
                        (For a Show) or 'dotnetconf/2017'(For an event, you
                        must specify the year)
  -q {mp4high,mp4,mp3}, --quality {mp4high,mp4,mp3}
                        'mp4high' (high quality) or 'mp4' (low quality) or
                        'mp3' (just mp3, sound without video)
```

Download **dotnetconf** 2017 videos, high quality.
```bash
$ python ./ch9-dl.py --type Events --name dotnetconf/2017 --quality mp4high
```

Download **Azure-Friday** episodes, as mp3.
```bash
$ python ./ch9-dl.py --type Shows --name Azure-Friday --quality mp3
```

## Feed types 
- There are two types of RSS feeds, "Events" or "Shows":    
    **Show** - https://s.ch9.ms/Shows/Azure-Friday/RSS/mp4high   
    **Event** - https://s.ch9.ms/Events/dotnetconf/2017/RSS/mp4high   

- For event, you need to specify the year of the event, for example: **dotnetconf/2017**.

## File types and quality

There are 4 options:
1. Video - low quailiy - mp4 (mp4)
2. Video - medium quailiy - mp4 (mp4med)
3. Video - high quaily - mp4 (mp4high)
4. Sound - mp3 (mp3)

## Thanks
The code was forked from [here](https://gist.github.com/tdavisjr/e5e78282052a10701954).

