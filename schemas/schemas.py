from pydantic import BaseModel
from typing import Optional


class Track(BaseModel):
    plate: str
    start_time: str
    end_time: str

