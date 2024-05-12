from fastapi import HTTPException, status
from fastapi.responses import ORJSONResponse
from dotenv import dotenv_values
import logging
from dao.dao import Fleet
from typing import List, Dict
from datetime import datetime
from haversine import haversine, Unit
from constants.info_message import InfoMessage

Records = List[Dict]

config = dotenv_values(".env")
logger = logging.getLogger(__name__)
Time_Interval = Dict[str, datetime]


class GPSManager:
    def __init__(self):
        self.dao = Fleet(config["MONGO_DB_COLLECTION"])

    def recorder(self, location: dict) -> None:
        location["server_time"] = datetime.now()
        self.dao.insert_one(document=location)
        logger.info(location)

        pass

    def reader(self, plate: str, start_time: int, end_time: int) -> List[dict]:
        res = self.dao.find_by_date(plate=plate, start_time=start_time, end_time=end_time)
        print("@@@@@@@@@@@@@@@@@@{}".format(res))
        return res


class Distance:
    def __init__(self, plate: str):
        self.distance = None
        self.plate = plate
        self.GPS = GPSManager()

    def records(self, start_time: datetime, end_time: datetime) -> Records:
        records = self.GPS.reader(plate=self.plate, start_time=start_time, end_time=end_time)
        return records

    def points(self, records: Records) -> list:
        sorted_records = self.sorter(records=records)
        return sorted_records

    def sorter(self, records: Records) -> list:
        pass

    def points_tuple(self, records: Records) -> list:
        list_of_tuples = [(d.pop('lat'), d.pop('long')) for d in records]
        return list_of_tuples

    def calculator(self, points: list) -> None:
        self.distance: float = 0
        for i in range(len(points)):
            distance_between_two_points = haversine(points[i], points[i + 1])
            self.distance += distance_between_two_points
        pass
