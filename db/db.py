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
        host = config["MONGO_HOST"]
        # username = config["MONGO_USERNAME"]
        # password = config["MONGO_PASSWORD"]
        port = config["MONGO_PORT"]
        username = urllib.parse.quote_plus('admin')
        password = urllib.parse.quote_plus('poiuytrewq')
        try:
            client = pymongo.MongoClient(
                f"mongodb://{username}:{password}@{host}:{port}/{self.database}?authSource=admin")

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
