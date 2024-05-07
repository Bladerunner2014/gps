from fastapi import HTTPException, status
from fastapi.responses import ORJSONResponse
from dotenv import dotenv_values
import logging
from dao.dao import Fleet
from typing import List, Dict
from datetime import datetime

config = dotenv_values(".env")
logger = logging.getLogger(__name__)
Records = List[Dict]
Time_Interval = Dict[str, datetime]


class GPSManager:
    def __init__(self):
        self.dao = Fleet(config["MONGO_DB_COLLECTION"])

    def recorder(self, location: dict) -> None:
        self.dao.insert_one(query=location)
        pass

    def reader(self, plate: str, interval: Time_Interval) -> Records:
        return self.dao.find_by_date(condition={"plate": plate,
                                                "start_date": interval["start_date"], "end_date": interval["end_date"]})
