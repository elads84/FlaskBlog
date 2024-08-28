import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    UPLOAD_FOLDER = 'static/profile_photos'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    PROFILE_PIC_WIDTH = 128
    POST_PIC_WIDTH = 500
