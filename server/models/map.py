from .base_model import BaseModel, db
from sqlalchemy import String, JSON
from sqlalchemy.orm import relationship
from uuid import uuid4


class Map(BaseModel):
    __tablename__ = 'maps'

    uuid = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    location_name = db.Column(String(130), nullable=False, unique=True)
    coordinates = db.Column(JSON, nullable=False)
    description = db.Column(String, nullable=True)
    quests_available = db.Column(JSON, default=lambda: [])

    players = relationship("Player", back_populates="current_location")
    quests = relationship("Quest", back_populates="location")

    serialize_rules = ('-players', '-quests',)