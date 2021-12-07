from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis
import os
from dotenv import load_dotenv, find_dotenv
import click

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

@app.cli.command("initdb")
def initDb():
	# clear all tables
	models.Score.query.delete()
	models.Playlist.query.delete()
	models.User.query.delete()
	models.Mood.query.delete()
	models.Genre.query.delete()
	db.session.commit()

	# initializing mood table with moods happy, sad, neutral, angry, afraid
	mHappy = models.Mood(title='happy', description="happy description")
	mSad = models.Mood(title='sad', description="sad description")
	mNeutral = models.Mood(title='neutral', description="neutral description")
	mAngry = models.Mood(title='angry', description="angry description")
	mAfraid = models.Mood(title='afraid', description="afraid description")
	for mood in [mHappy, mSad, mNeutral, mAfraid, mAngry]:
		db.session.add(mood)
	db.session.commit()
	
	# initializing genre table with genres blues, jazz, rock, rock and roll, country, soul, dance, hip hop
	gBlues = models.Genre(title='chill', description='chill description')
	gJazz = models.Genre(title='jazz', description='jazz description')
	gRock = models.Genre(title='rock', description='rock description')
	gRockAndRoll = models.Genre(title='rock and roll', description='rock and roll description')
	gCountry = models.Genre(title='country', description='country description')
	gSoul = models.Genre(title='soul', description='soul description')
	gDance = models.Genre(title='dance', description='dance description')
	gHipHop = models.Genre(title='hip hop', description='hip hop description')
	for genre in [gBlues, gJazz, gRockAndRoll, gCountry, gSoul, gDance, gHipHop, gRock]:
		db.session.add(genre)
	db.session.commit()

	# initializing user table with users
	user1 = models.User(username='hamza', email='hamzaboudouche@student.emi.ac.ma', passwordHash='$2a$10$wY.SamFlNCZOHzTZCqTUkOAZDO013sId796jzLd4m3B8TONRVjXkG', genre=gDance, commonMood=mHappy)
	test = models.User(username='test', email='test@test.com', passwordHash='$2a$10$UCOR2xkoMh2E.sFeo/1zw.TYYPuqlfyzEspOFQobNlquzO4obBOcG', genre=gDance, commonMood=mHappy)
	db.session.add(user1)
	db.session.commit()

	# initializing playlist table with random playlists
	playlist1 = models.Playlist(id=1, uri='0vvXsWCC9xrXsKd4FyS8kM?si=79e100eacf2e454f', title='lofi hip hop', genre=gHipHop, mood=mNeutral)
	db.session.add(playlist1)
	db.session.commit()

	# initializing score table with random scores
	score1 = models.Score(user=user1, playlist=playlist1, score=1, mood=mNeutral)
	db.session.add(score1)
	db.session.commit()