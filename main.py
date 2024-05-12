from fastapi import HTTPException, status
from fastapi.responses import ORJSONResponse
from dotenv import dotenv_values
from fastapi import FastAPI
import logging
from log import log
from fastapi.middleware.cors import CORSMiddleware
from cache.cache_manager import CacheManager
import json
from typing import List, Dict
from datetime import datetime

from constants.info_message import InfoMessage
from constants.error_message import ErrorMessage
from manager.manager import GPSManager

Time_Interval = Dict[str, datetime]

app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
config = dotenv_values(".env")
logger = logging.getLogger(__name__)


@app.post("/gps/")
def record_location(gps: dict):
    latitude = gps['data']['latitude']
    longitude = gps['data']['longitude']
    document = {"plate": gps['plate'], "location": [longitude, latitude],
                "driver_id": gps['data']['driver_id']}
    cache = CacheManager()

    cache.hset(str(gps['plate']), gps['data'])
    recorder = GPSManager()
    recorder.recorder(document)


pass


@app.get("/gps/{plate}")
def read_location(plate: str):
    cache = CacheManager()
    try:
        res = cache.hget(plate)
        logger.info(InfoMessage.GET_LIVE_LOCATION)
    except Exception as error:
        logger.error(ErrorMessage.GET_LIVE_LOCATION)
        logger.error(error)
        raise Exception

    return ORJSONResponse(content=res, status_code=status.HTTP_200_OK)


@app.post("/gps/track/")
def track_location(
        plate: str, start_time: int, end_time: int
):
    reader = GPSManager()

    locations = reader.reader(plate, start_time, end_time)
    if not locations:
        raise HTTPException(status_code=404, detail="No locations found for the specified parameters")
    return locations


@app.get("/distance/{plate}")
def distance(plate: str, date: dict):
    pass


log.setup_logger()
