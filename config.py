import os

# DB 환경변수
BASE_URL = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_URL, 'collection.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 폼모듈 환경변수
SECRET_KEY = 'dev'