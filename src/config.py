import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TESTING = False
    DEBUG=False
    SECRET_KEY=os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI")
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG=True
    SECRET_KEY="dev"
    SQLALCHEMY_DATABASE_URI="sqlite:///posts.sqlite"
    JWT_SECRET_KEY="super secret"

class TestingConfig(Config):
    SECRET_KEY="test"
    SQLALCHEMY_DATABASE_URI="sqlite://"
    JWT_SECRET_KEY="test"