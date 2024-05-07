import pymongo
import logging
from dotenv import dotenv_values
import urllib.parse

config = dotenv_values(".env")


class DBconnect:
    def __init__(self, collection):
        self.database = config["MONGO_DB"]
        self.collection = collection
        self.logger = logging.getLogger(__name__)

    def connect(self):
        username = urllib.parse.quote_plus(config["MONGO_USERNAME"])
        password = urllib.parse.quote_plus(config["MONGO_PASSWORD"])
        try:
            client = pymongo.MongoClient("mongodb://%s:%s@mongodb/" % (username, password))

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
