import pymongo
import pandas as pd
import settings

class MongoDbTools:
    def __init__(self, collection):
        self.collection = collection

    def connect_to_video_db(self, host, port, username, password, db):
        try:
            if username and password:
                mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
                conn = pymongo.MongoClient(mongo_uri)
            else:
                conn = pymongo.MongoClient(host, port)
            return conn[db]
        except pymongo.errors.ConnectionFailure as e:
            return "Server connection failed: %s" % e

    def read_videodata_from_db(self, query="", no_id=False):
        db = self.connect_to_video_db(settings.MongoHost, settings.MongoPort, settings.MongoUserName,
                                      settings.MongoPassword, settings.MongoDb)
        try:
            if(query != ""):
                cursor = db[self.collection].find(query)
            else: 
                cursor = db[self.collection].find()
            df = pd.DataFrame(list(cursor))
        except:
            return "No data found"
        if no_id:
            del df['_id']
        return df

    def read_text_index_videodata_from_db(self, field, stxt, no_id=False):
        db = self.connect_to_video_db(settings.MongoHost, settings.MongoPort, settings.MongoUserName,
                                      settings.MongoPassword, settings.MongoDb)
        index = db[self.collection].ensure_index([(field, "text"), ("unique", 1), ("dropDups", 1)], default_language ='english')
        try:
            res = db[self.collection].find({'$text': {'$search': stxt}}, {'score':{'$meta':"textScore"}})
            df = pd.DataFrame(list(res))
        except:
            return "No data found"
        if no_id:
            del df['_id']
        return df


    def update_videodata_from_db(self, video_id, updated):
        db = self.connect_to_video_db(settings.MongoHost, settings.MongoPort, settings.MongoUserName,
                                      settings.MongoPassword, settings.MongoDb)
        try:
            db[self.collection].update_one({'id': video_id}, {"$set": updated})
        except:
            return "error"
        return

    def replace_videodata_from_db(self, video_id, replaced):
        db = self.connect_to_video_db(settings.MongoHost, settings.MongoPort, settings.MongoUserName,
                                      settings.MongoPassword, settings.MongoDb)
        try:
            db[self.collection].replace_one({'id': video_id}, replaced)
        except:
            return "error"
        return

    def write_videodata_to_db(self, json):
        db = self.connect_to_video_db(settings.MongoHost, settings.MongoPort, settings.MongoUserName,
                                      settings.MongoPassword, settings.MongoDb)
        try:
            db[self.collection].insert_one(json)
        except:
            return "error"
        return
