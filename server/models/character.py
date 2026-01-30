import uuid
from .base_model import BaseModel, db
from sqlalchemy import String, JSON
from sqlalchemy.orm import relationship

class Character(BaseModel):
    __tablename__ = 'characters'

    uuid = db.Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    character_type = db.Column(String, nullable=False)
    abilities = db.Column(String, nullable=False)
    inventory = db.Column(JSON, default=lambda: [])
    description = db.Column(String, nullable=True)

    player = relationship("Player", back_populates="character")

    serialize_rules = ('-player',)
