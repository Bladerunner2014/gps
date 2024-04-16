from fastapi import HTTPException, status
from fastapi.responses import ORJSONResponse
from dotenv import dotenv_values
from fastapi import FastAPI
import logging
from log import log
from fastapi.middleware.cors import CORSMiddleware
from cache.cache_manager import CacheManager
from rtdb.rethink import RethinkDBConnection
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
    latitude = gps['data']['latitude']
    longitude = gps['data']['longitude']

    # Insert the extracted data into RethinkDB
    document = {"plate": gps['plate'], "location": [longitude, latitude],
                "driver_id": gps['data']['driver_id']}
    cache = CacheManager()

    rt = RethinkDBConnection()

    res = cache.hset(str(gps['plate']), gps['data'])
    rt.connect()
    # rt.create_table('geo_data')
    rt.insert_document(table_name='geo_data', document=document)
    rt.close()

    return res


@app.get("/gps/{plate}")
def read_location(plate: str):
    print(plate)
    cache = CacheManager()
    res = cache.hget(plate)

    return res


@app.get("/gps_track/{plate}")
def track_location(plate: str):
    print(plate)
    rt = RethinkDBConnection()
    rt.connect()
    docs = rt.get_documents_by_key(table_name='people', key='plate', value=plate)

    return docs


@app.post("/geo_query/")
def geo_query(location: dict):
    print(location)
    rt = RethinkDBConnection()
    rt.connect()
    rt.create_geo_index('geo_data', 'location')

    radius_in_km = 10  # Adjust the radius as needed
    documents = rt.get_documents_by_geo('geo_data', 'location', 98756875986, 987765424, 10)

    return documents


log.setup_logger()
