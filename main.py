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
from schemas.schemas import Track
from constants.info_message import InfoMessage
from constants.error_message import ErrorMessage
from manager.manager import GPSManager, Distance

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
    document = {"plate": gps['plate'], "location": [longitude, latitude]}
    cache = CacheManager()

    cache.hset(str(gps['plate']), gps['data'])
    recorder = GPSManager()
    recorder.recorder(document)
    return ORJSONResponse(content={"message": InfoMessage.RECORDED}, status_code=status.HTTP_200_OK)


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
    return res


@app.post("/gps/track/")
def track_location(track: Track):
    reader = GPSManager()
    locations = reader.reader(track)
    if not locations:
        raise HTTPException(status_code=404, detail=ErrorMessage.NOT_FOUND)
    return ORJSONResponse(content=locations, status_code=status.HTTP_200_OK)


@app.post("/distance/")
def distance(track: Track):
    distance_calc = Distance()
    distance_calc.points_tuple(track=track)
    distance_calc.calculator()

    return ORJSONResponse(content=distance_calc.distance, status_code=status.HTTP_200_OK)


log.setup_logger()
