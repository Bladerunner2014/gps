import pymongo
import logging
from dotenv import dotenv_values
import urllib.parse


class DBconnect:
    def __init__(self, collection):
        self.database = 'Syb'
        self.collection = collection
        self.config = dotenv_values(".env")
        self.logger = logging.getLogger(__name__)

    def connect(self):
        username = urllib.parse.quote_plus("admin")
        password = urllib.parse.quote_plus("poiuytrewq")
        port = self.config["MONGO_PORT"]
        try:
            client = pymongo.MongoClient(f"mongodb://mongodb:{port}/")

        except Exception as error:
            self.logger.error(error)
            raise Exception

        try:
            database = client[self.database]
            collection = database[self.collection]
        except Exception as error:
            self.logger.error(error)
            raise Exception

        return collection
