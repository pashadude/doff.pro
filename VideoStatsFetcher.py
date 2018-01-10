from __future__ import unicode_literals
import requests
import settings
import mongoTools
import datetime
import argparse
import smilarities
import pandas as pd
from py2neo import Graph, Node, Relationship, authenticate


def main():
    parser = argparse.ArgumentParser(prog='GameVidStats', allow_abbrev=False)
    parser.add_argument('game', nargs=1, type=str)
    parser.add_argument('games', type=int, nargs=1)
    parser.add_argument('--res', nargs='?', type=str, const='1080', default='1080')
    args = parser.parse_args()
    stats = VideoStatsFetcher(args.game[0], args.games[0], args.res)
    stats.get_game_vids()
    stats.fill_similarities_graph()


class VideoStatsFetcher:
    def __init__(self, game, top, resolution):
        self.game = game
        self.resolution = resolution
        db = mongoTools.MongoDbTools('GameStats')
        gamedata = db.read_videodata_from_db({"name": self.game})
        self.gameid = gamedata['id'][0]
        self.maxvideos = int(gamedata['videos'][0])
        self.videos = top
        #print(self.maxvideos, self.videos)
        self.appid = settings.PlaysTvAppId
        self.appkey = settings.PlaysTvKey
        self.db_game = mongoTools.MongoDbTools(self.game)
        self.db_sim = mongoTools.MongoDbTools("Similarities_{0}".format(self.game))

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
        for i in data:
            if not (isinstance(i, str)):
                if i['resolutions'] != None:
                    #print(self.resolution in i['resolutions'])
                    if len(self.db_game.read_videodata_from_db({"id": i['id']})) == 0 and (self.resolution in i['resolutions']):
                        video = {}
                        video['id'] = i['id']
                        video['author'] = i['author']['id']
                        video['time'] = datetime.datetime.fromtimestamp(int(i['upload_time'])).strftime(
                            '%Y-%m-%d %H:%M:%S')
                        video['hashtags'] = []
                        video['title'] = i['description']
                        video['rating'] = (int(i['stats']['views']) + int(i['stats']['likes'])*5)/(int(i['author']['stats']['followers'])+1)
                        #print(rating)
                        #break
                        if 'metatags' in i:
                            video['hashtags'] = self.turn_metatags_to_hashtags(i['metatags'])
                        if 'hashtags' in i:
                            for hash in i['hashtags']:
                                video['hashtags'].append(hash['tag'])
                        video['hashtags'].append(i['author']['id'])
                        video['hashtags'].append(video['title'])
                        self.db_game.write_videodata_to_db(video)
        return

    def fill_similarities_graph(self):
        authenticate(settings.NeoHost, settings.NeoLog, settings.NeoPass)
        graph = Graph("{0}/db/data/".format(settings.NeoHost))
        graph.delete_all()
        data = pd.DataFrame(self.db_game.read_videodata_from_db())
        if not isinstance(data, str) and not data.empty:
            data = data[pd.notnull(data['title'])]
            data = data[pd.notnull(data['rating'])]
            #print(data)
            k = len(data)
            mes = smilarities.SimilarityMeasures()
            vid = 0
            while vid < k:
                data1 = pd.DataFrame(self.db_game.read_text_index_videodata_from_db('hashtags', data['hashtags'][vid]))
                subg = graph.begin()
                node = Node("Video", id=str(data['id'][vid]), rating=data['rating'][vid], title=data['title'][vid])
                subg.merge(node)
                vid1 = 0
                while vid1 <= len(data1):
                    node1 = Node("Video", id=str(data1['id'][vid1]), rating=data1['rating'][vid1], title=data1['title'][vid1])
                    subg.merge(node1)
                    num = mes.jaccard_similarity(data['hashtags'][vid], data1['hashtags'][vid1])
                    #print(len(data['hashtags'][vid]))
                    if (num > 0.5 and len(data['hashtags'][vid])>3):
                        jaccard = Relationship(node, "Jaccard", node1, jaccard_similarity = num)
                        #print(jaccard)
                        subg.merge(jaccard)
                    num = mes.jaccard_similarity(data1['hashtags'][vid1], data['hashtags'][vid])
                    #if (num > 0.5 and len(data['hashtags'][vid1])>3):
                        #jaccard1 = Relationship(node1, "Jaccardback", node, jaccard_similarity = num)
                        #subg.merge(jaccard1)
                    vid1 += 1
                #graph.merge(subg)
                subg.commit()
                vid += 1
            #print(pd.DataFrame(graph.run("MATCH (a:Video) RETURN a.id, a.title, a.rating LIMIT 10").data()))
        return


if __name__ == "__main__":
    main()
