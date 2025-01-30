from pydantic import BaseModel
from enum import Enum


class Role(str, Enum):
    USER = "user"
    SYSTEM = "system"


class Message(BaseModel):
    role: Role
    content: str


class Place(BaseModel):
    name: str
    address: str
    types: list[str]
    rating: float
    editorial_summary: str


class Itinerary(BaseModel):
    id: str
    activities: list[Place]


class ExpandEditorialInputParams(BaseModel):
    place_name: str
    editorial_summary: str


class ProfileParams(BaseModel):
    description: str
    location: str
