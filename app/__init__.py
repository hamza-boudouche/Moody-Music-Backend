from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate	

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.users import bp as users_bp
app.register_blueprint(users_bp, url_prefix='/user')

from app.music import bp as music_bp
app.register_blueprint(music_bp, url_prefix='/music')

from app.moodrec import bp as moodrec_bp
app.register_blueprint(moodrec_bp)

from app import models