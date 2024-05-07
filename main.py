from fastapi import HTTPException, status
from fastapi.responses import ORJSONResponse
from dotenv import dotenv_values
from fastapi import FastAPI
import logging
from log import log
from fastapi.middleware.cors import CORSMiddleware
from cache.cache_manager import CacheManager
import json
from manager.manager import GPSManager

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
    logger.info(gps)
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
    res = cache.hget(plate)

    return ORJSONResponse(content=res, status_code=status.HTTP_200_OK)


@app.get("/gps_track/{plate}")
def track_location(plate: str, date: dict):
    reader = GPSManager()
    res = reader.reader(plate=plate, interval=date)
    return ORJSONResponse(content=res, status_code=status.HTTP_200_OK)


@app.get("/distance/{plate}")
def distance(plate: str, date: dict):
    pass


log.setup_logger()
