from fastapi import HTTPException, status
from fastapi.responses import ORJSONResponse
from dotenv import dotenv_values
import logging
from dao.dao import Fleet
from typing import List, Dict, Tuple, Any
from datetime import datetime
from haversine import haversine, Unit
from constants.info_message import InfoMessage
from schemas.schemas import Track
from log import log

Records = List[Dict]

config = dotenv_values(".env")
logger = logging.getLogger(__name__)
Time_Interval = Dict[str, datetime]


class GPSManager:
    def __init__(self):
        self.dao = Fleet(config["MONGO_DB_COLLECTION"])

    def recorder(self, location: dict) -> None:
        location["server_time"] = datetime.now()
        logger.info(location)

        self.dao.insert_one(document=location)

        pass

    def reader(self, track: Track) -> List[dict]:
        res = self.dao.find_by_date(plate=track.plate, start_time=track.start_time, end_time=track.end_time)
        return res


class Distance:
    def __init__(self):
        self.records = None
        self.sorted_location_tuples = None
        self.distance = None
        self.GPS = GPSManager()

    def points_tuple(self, track: Track) -> None:
        self.records = self.GPS.reader(track=track)
        location_list = [(d['location'][1], d['location'][0], d['server_time']['$date']) for d in self.records]
        sorted_location_list = sorted(location_list, key=lambda x: x[2])
        self.sorted_location_tuples = [(t[0], t[1]) for t in sorted_location_list]
        pass

    def calculator(self) -> None:
        self.distance: float = 0
        for i in range(len(self.sorted_location_tuples) - 1):
            distance_between_two_points = haversine(self.sorted_location_tuples[i], self.sorted_location_tuples[i + 1])
            self.distance += distance_between_two_points
        pass


log.setup_logger()
