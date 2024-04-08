import os, dotenv
from datetime import timedelta
import redis

dotenv.load_dotenv()

# app.config 설정
class AppConfig:
    SECRET_KEY = f'{os.getenv('SECRET_KEY')}'
    BCRYPT_LEVEL = 10

    SESSION_TYPE = 'redis'
    SESSION_PERMANENT= False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url(f'redis://{os.getenv('RD_URL')}')
    
    SESSION_PERMANENT = True
    PERMENENT_SESSION_LIFETIME = timedelta(minutes=1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PW')}@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DBNAME')}'
