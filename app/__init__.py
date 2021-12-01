from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis
import os
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

load_dotenv(find_dotenv())
redis_host = os.environ.get("REDIS_HOST")
redis_port = os.environ.get("REDIS_PORT")
cache = Redis(host=redis_host, port=redis_port, db=0)

from app.users import bp as users_bp
app.register_blueprint(users_bp, url_prefix='/user')

from app.music import bp as music_bp
app.register_blueprint(music_bp, url_prefix='/music')

from app.moodrec import bp as moodrec_bp
app.register_blueprint(moodrec_bp, url_prefix='/mood')

from app import models