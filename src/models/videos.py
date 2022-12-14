from bson import ObjectId
from datetime import datetime
from models import PyObjectId
from pydantic import BaseModel, AnyHttpUrl, Field
from typing import Optional
import db
import pymongo


class Thumbnail(BaseModel):
    url: AnyHttpUrl
    width: float
    height: float

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class Video(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    video_id: str
    title: str
    description: str
    thumbnail: Thumbnail
    published_at: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


conn = db.get_sync_mongo_conn()
collection = conn["videos"]
collection.create_index([("title", "text")])
collection.create_index([("video_id", pymongo.ASCENDING)], unique=True)
