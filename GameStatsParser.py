import argparse
import json
import requests
import settings
import mongoTools

def main():
    parser = argparse.ArgumentParser()
    def convert(argument):
        return list(map(str, argument.split(', ')))
    parser.add_argument('games', nargs='+', type=convert)
    args = parser.parse_args()
    gameparser = GamesParser(args.games)
    gameparser.gamelist()


class GamesParser:
    def __init__(self, games):
        self.games = games[0]
        self.appid = settings.PlaysTvAppId
        self.appkey = settings.PlaysTvKey

    def gamelist(self):
        call = 'https://api.plays.tv/data/v1/games?appid={0}&appkey={1}'.format(self.appid, self.appkey)
        print(self.games)
        r = requests.get(call)
        if r.status_code != 404:
            if r.status_code == 200:
                self.parse_gamelist(r.text)
            elif r.status_code == 403:
                return 'forbidden'
            else:
                return 'error {}'.format(r.status_code)
        else:
            return 'down'

    def parse_gamelist(self, gamelist):
        game_data = json.loads(gamelist)
        for i in game_data['content']['games'].values():
            if i['title'] in self.games:
                name = i['title']
                id = i['id']
                videos = i['stats']['videos']
                js = {'id': id, 'videos': videos, 'name': name}
                db = mongoTools.MongoDbTools('GameStats')
                current = db.read_videodata_from_db({"name": name})
                if len(current) == 0:
                    db.write_videodata_to_db(js)
                elif current['videos'][0] < videos:
                    #print(current['id'][0], db.read_videodata_from_db({"id": current['id'][0]}))
                    db.replace_videodata_from_db(current['id'][0], js)
        return


if __name__ == "__main__":
    main()