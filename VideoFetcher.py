from __future__ import unicode_literals
import youtube_dl
import requests
import json
import pickle
import settings

class VideoStatsFetcher:
    def __init__(self, game, top):
        gamedata = pickle.load(open(settings.GamesDataPath, 'rb+'))
        pickle.dump(gamedata, open(settings.GamesDataPath, 'wb+'))
        self.gameid = gamedata[game]['id']
        self.maxvideos = int(gamedata[game]['videos'])
        self.videos = top
        self.appid = settings.PlaysTvAppId
        self.appkey = settings.PlaysTvKey

    def get_vid_stats_page(self, page, limit):
        call = 'https://api.plays.tv/data/v1/videos/search?appid={0}&appkey={1}' \
               '&gameId={2}&limit={3}&page={4}'.format(self.appid, self.appkey, self.gameid, limit, page)
        try:
            r = requests.get(call).json()
            r = r['content']['items']
        except Exception as e:
            r = 'the error is %s' % e
        return r

    def get_vid_stats(self):
        if int(self.videos) > int(self.maxvideos):
            self.videos = self.maxvideos
        k = 1
        vids = 0
        data = {}
        while vids < self.videos:
            vids += settings.PlaysTvLinesPerPage/settings.PlaysTvLinesPerVid
            get_vids = self.get_vid_stats_page(k, settings.PlaysTvLinesPerPage)
            if get_vids == []:
                break
            if k == 1:
                data = get_vids
            else:
                data += get_vids
            k += 1
        print(vids)
       

class VideoFetcher:
    def __init__(self, uri, game, videoid):
        self.uri = uri
        self.game = game
        self.id = videoid

    def fetch_video(self):
        ydl_opts = {
            'format': 'best',
            'preferredcodec': 'mp3',
            'outtmpl': 'videos/{0}/{1}/%(title)s'.format(self.game, self.id),
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.uri])
        return
        
