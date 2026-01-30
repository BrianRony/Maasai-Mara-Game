from .base_model import BaseModel, db
from sqlalchemy import String, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4


class Quest(BaseModel):
    __tablename__ = 'quests'

    uuid = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title = db.Column(String(255), nullable=False)
    description = db.Column(String(255), nullable=False)
    outcomes = db.Column(JSON, nullable=False)
    is_completed = db.Column(Boolean, default=False)

    location_id = db.Column(db.Integer, db.ForeignKey('maps.uuid'))
    location = relationship("Map", back_populates="quests")

    serialize_rules = ('-location',)