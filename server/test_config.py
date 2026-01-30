import os

class TestingConfig():
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///test_maasai_mara.db')
    TESTING = True