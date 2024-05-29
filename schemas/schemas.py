from pydantic import BaseModel, Field
from constants.id_generator import IDGenerator
from datetime import datetime
from datetime import timezone

from typing import Optional, List

unique_id = IDGenerator("L")


class Track(BaseModel):
    plate: str
    start_time: str
    end_time: str


class RecordTrack(BaseModel):
    track_id: str = Field(default=unique_id.generate_custom_id())
    plate: str
    location: List[float]
    recorded_time: str = Field(default=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f"))

    def __init__(self, **data):
        super().__init__(**data)
        self.track_id = unique_id.generate_custom_id()
        self.recorded_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")


class LocationData(BaseModel):
    latitude: int = Field(..., description="The latitude value")
    longitude: int = Field(..., description="The longitude value")


class LocationInRedis(BaseModel):
    plate: str = Field(..., description="The vehicle's plate number")
    data: LocationData

    class Config:
        schema_extra = {
            "example": {
                "plate": "efyvgerfgre83",
                "data": {
                    "latitude": 987765424,
                    "longitude": 98756875986
                }
            }
        }
