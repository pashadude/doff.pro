from __future__ import unicode_literals
import youtube_dl
import requests
import settings
import mongoTools
import datetime
import os
import cv2

class VideoStatsFetcher:
    def __init__(self, game, top, resolution):
        self.game = game
        self.resolution = resolution
        db = mongoTools.MongoDbTools('GameStats')
        gamedata = db.read_videodata_from_db({"name": game})
        self.gameid = gamedata[game]['id'][0]
        self.maxvideos = int(gamedata[game]['videos'][0])
        self.videos = top
        self.appid = settings.PlaysTvAppId
        self.appkey = settings.PlaysTvKey

    def get_game_vids_page(self, page, limit):
        call = 'https://api.plays.tv/data/v1/videos/search?appid={0}&appkey={1}' \
               '&gameId={2}&limit={3}&page={4}'.format(self.appid, self.appkey, self.gameid, limit, page)
        try:
            r = requests.get(call).json()
            r = r['content']['items']
        except Exception as e:
            r = 'the error is %s' % e
        return r

    def turn_metatags_to_hashtags(self, metatags):
        hashtags = []
        for i in metatags:
            hashtag = self.parse_metatag(i)
            hashtags.append(hashtag)
        return hashtags

    def parse_metatag(self, metatag):
        parts = metatag["metatag"].split(":")
        return parts[-1]

    def hashtag_list_to_str(self, hashtag_list):
        request = " ".join(str(x) for x in hashtag_list)
        return request

    def get_game_vids(self):
        if int(self.videos) > int(self.maxvideos):
            self.videos = self.maxvideos
        k = 1
        vids = 0
        while vids < self.videos:
            vids += settings.PlaysTvLinesPerPage/settings.PlaysTvLinesPerVid
            get_vids = self.get_game_vids_page(k, settings.PlaysTvLinesPerPage)
            if get_vids == []:
                break
            k += 1
            self.store_game_videos(get_vids)
        return

    def store_game_videos(self, data):
        db = mongoTools.MongoDbTools(self.game)
        for i in data:
            if not (isinstance(i, str)):
                if i['resolutions'] != None:
                    if len(db.read_videodata_from_db({"id": i['id']})) != 0 and (self.resolution in i['resolutions']):
                        video = {}
                        video['id'] = i['id']
                        video['author'] = i['author']['id']
                        video['time'] = datetime.datetime.fromtimestamp(int(i['upload_time'])).strftime(
                            '%Y-%m-%d %H:%M:%S')
                        video['hashtags'] = []
                        video['title'] = i['title']
                        if 'metatags' in i:
                            video['hashtags'] = self.turn_metatags_to_hashtags(i['metatags'])
                        if 'hashtags' in i:
                            for hash in i['hashtags']:
                                video['hashtags'].append(hash['tag'])
                        if video['hashtags'] != []:
                            db.write_videodata_to_db(video)

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
        self.videoFolderPath = '{0}/{1}/{2}/'.format(settings.VideosDirPath, self.game, self.id)
        myFilePath = os.path.join(self.videoFolderPath, 'video.mp4')
        vidcap = cv2.VideoCapture(myFilePath)
        count = 0
        success = True
        while success:
            success, image = vidcap.read()
            cv2.imwrite(os.path.join(self.videoFolderPath, 'frame{0}.jpg'.format(count)), image)
            if cv2.waitKey(10) == 27:
                break
            count += 1
        return


        
