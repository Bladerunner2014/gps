from fastapi import HTTPException, status
from fastapi.responses import ORJSONResponse
from dotenv import dotenv_values
from fastapi import FastAPI
import logging
from log import log
from fastapi.middleware.cors import CORSMiddleware
from cache.cache_manager import CacheManager
import json

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
    cache = CacheManager()

    res = cache.hset(str(gps['plate']), gps['data'])

    return res


@app.get("/gps/{plate}")
def read_location(plate: str):
    print(plate)
    cache = CacheManager()
    res = cache.hget(plate)

    return res


log.setup_logger()
