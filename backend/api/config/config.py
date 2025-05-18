import os
from pathlib import Path
from dotenv import load_dotenv


basedir = Path(__file__).parent.parent

# .env の読み込み
load_dotenv(dotenv_path=basedir / '.env')

class LocalConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 追跡を無効化
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1時間