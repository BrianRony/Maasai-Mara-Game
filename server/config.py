import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///maasai_mara.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    DEFAULT_START_LOCATION_COORDINATES = {"x": 0, "y": 0}
    CACHE_TYPE = 'simple'