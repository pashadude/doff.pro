from __future__ import unicode_literals
import youtube_dl
import requests
import json
import pickle


class VideoStatsFetcher:
    def __init__(self, game, top, appid, appkey):
        gamedata = pickle.load(open('data/games.pkl', 'wb+'))
        self.gameid = gamedata[game]['id']
        self.appid = appid
        self.appkey = appkey

    def get_vid_stats(self):
        page = np.random.random_integers(int(self.maxvideos//self.videos))
        call = 'https://api.plays.tv/data/v1/games?appid={0}&appkey={1}&gameId={2}&limit=1&sort=popular&sortdir=asc'.format(self.appid, self.appkey, self.gameid)
        r = requests.get(call)
        data =  json.loads(r.text)
        info = {}
        info['id'] = data['items'][0]['id']
        info['game'] = data['items'][0]['game']['title']
        return 


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
        
