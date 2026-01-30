import uuid
from .base_model import BaseModel, db
from sqlalchemy import Integer, String, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship

class Player(BaseModel):
    __tablename__ = 'players'

    uuid = db.Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(String, nullable=False)
    health = db.Column(Integer, default=100)
    score = db.Column(Integer, default=0)
    inventory = db.Column(JSON, default=lambda: [])
    current_quest = db.Column(JSON, nullable=True)  # Store current quest info as JSON
    
    current_location_id = db.Column(Integer, db.ForeignKey('maps.uuid'))
    current_location = relationship("Map", back_populates="players")
    character_id = db.Column(String(36), db.ForeignKey('characters.uuid'))
    character = relationship("Character", back_populates="player", uselist=False)

    
    serialize_rules = ('-character', '-current_location',)
