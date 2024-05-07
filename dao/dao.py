import pymongo
import logging
import pymongo.errors
from db.db import DBconnect
import json
from bson import json_util

logger = logging.getLogger(__name__)


class Fleet:

    def __init__(self, collection):
        self.db = DBconnect(collection).connect()

    def insert_one(self, query: dict):
        try:
            self.db.insert_one(query)
        except pymongo.errors as error:
            logger.error(error)
            raise error

    def find(self, condition: dict):
        try:
            dt = self.parse_json(self.db.find(condition, {'_id': 0}))

            return dt
            # return self.db.find_one(condition)
        except pymongo.errors as error:
            logger.error(error)
            raise error

    def find_one(self, condition: dict):
        try:
            dt = self.parse_json(self.db.find_one(condition, {'_id': 0}))

            return dt
            # return self.db.find_one(condition)
        except pymongo.errors as error:
            logger.error(error)
            raise error

    def update(self, fltr: dict, new_values: dict):
        newvalues = {"$set": new_values}

        try:
            r = self.db.update_one(fltr, newvalues)
        except pymongo.errors as error:
            logger.error(error)
            raise error
        return r

    def update_one(self, query: dict, update: dict):

        try:
            r = self.db.update_one(query, update, True)
        except pymongo.errors as error:
            logger.error(error)
            raise error
        return r

    def delete(self, condition: dict):
        try:
            self.db.delete_one(condition)
        except pymongo.errors as error:
            logger.error(error)
            raise error

    @staticmethod
    def parse_json(data):
        return json.loads(json_util.dumps(data))
