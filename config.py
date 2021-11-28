import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
username: str = os.environ.get("USERNAME")
password: str = os.environ.get("PASSWORD")
ip: str = os.environ.get("IPADRESS")
port: int = os.environ.get("PORT")
db: str = os.environ.get("DBNAME")

class Config(object):
	SQLALCHEMY_DATABASE_URI: str = f"postgresql://{username}:{password}@{ip}:{port}/{db}"
	SQLALCHEMY_TRACK_MODIFICATIONS: str = False