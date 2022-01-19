from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv
import logging
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

load_dotenv(find_dotenv())
redis_host = os.environ.get("REDIS_HOST")
redis_port = os.environ.get("REDIS_PORT")
cache = Redis(host=redis_host, port=redis_port, db=0)

logging_level = (
    logging.DEBUG if os.environ.get("FLASK_ENV") == "development" else logging.INFO
)
logging.basicConfig(filename="moodylog.log", level=logging.DEBUG)

from app.users import bp as users_bp

CORS(users_bp, resources=r"/*")

app.register_blueprint(users_bp, url_prefix="/user")

from app.music import bp as music_bp

CORS(music_bp, resources=r"/*")

app.register_blueprint(music_bp, url_prefix="/music")

from app.moodrec import bp as moodrec_bp

CORS(moodrec_bp, resources=r"/*")

app.register_blueprint(moodrec_bp, url_prefix="/mood")

from app import models


@app.cli.command("initdb")
def initDb():
    logging.info("initializing database")
    # clear all tables
    models.Score.query.delete()
    models.Playlist.query.delete()
    models.User.query.delete()
    models.Mood.query.delete()
    models.Genre.query.delete()
    db.session.commit()

    logging.info("filling Mood table")
    # initializing mood table with moods happy, sad, neutral, angry, afraid
    mHappy = models.Mood(id=3, title="happy", description="happy description")
    mSad = models.Mood(id=5, title="sad", description="sad description")
    mNeutral = models.Mood(id=4, title="neutral", description="neutral description")
    mAngry = models.Mood(id=0, title="angry", description="angry description")
    mFearful = models.Mood(id=2, title="fearful", description="fearful description")
    mDisgusted = models.Mood(
        id=1, title="disgusted", description="disgusted description"
    )
    for mood in [mHappy, mSad, mNeutral, mAngry, mFearful, mDisgusted]:
        db.session.add(mood)
    db.session.commit()

    logging.info("filling Genre table")
    # initializing genre table with genres blues, jazz, rock, rock and roll, country, soul, dance, hip hop
    gBlues = models.Genre(title="chill", description="chill description")
    gJazz = models.Genre(title="jazz", description="jazz description")
    gRock = models.Genre(title="rock", description="rock description")
    gRockAndRoll = models.Genre(
        title="rock and roll", description="rock and roll description"
    )
    gCountry = models.Genre(title="country", description="country description")
    gSoul = models.Genre(title="soul", description="soul description")
    gDance = models.Genre(title="dance", description="dance description")
    gHipHop = models.Genre(title="hip hop", description="hip hop description")
    for genre in [gBlues, gJazz, gRockAndRoll, gCountry, gSoul, gDance, gHipHop, gRock]:
        db.session.add(genre)
    db.session.commit()

    logging.info("filling Users table")
    # initializing user table with users
    user1 = models.User(
        username="hamza",
        email="hamzaboudouche@student.emi.ac.ma",
        passwordHash="$2a$10$wY.SamFlNCZOHzTZCqTUkOAZDO013sId796jzLd4m3B8TONRVjXkG",
        genre=gDance,
        commonMood=mHappy,
    )
    test = models.User(
        username="test",
        email="test@test.com",
        passwordHash="$2a$10$UCOR2xkoMh2E.sFeo/1zw.TYYPuqlfyzEspOFQobNlquzO4obBOcG",
        genre=gDance,
        commonMood=mHappy,
    )
    db.session.add(user1)
    db.session.add(test)
    db.session.commit()

    logging.info("filling Playlists table")
    # initializing playlist table with random playlist
    playlists = [
        {
            "uri": "album/0vvXsWCC9xrXsKd4FyS8kM",
            "title": "lofi hip hop",
            "mood": mNeutral,
        },
        {
            "uri": "playlist/37i9dQZF1DX720GaRlTmKS",
            "title": "concentration maximum",
            "mood": mNeutral,
        },
        {
            "uri": "playlist/6Fbvmc7cfthnhhPq68a09E",
            "title": "good vibes",
            "mood": mHappy,
        },
        {
            "uri": "album/1x5rOJPgIMZhoYnkZp0htl",
            "title": "fire and darkness",
            "mood": mFearful,
        },
        {
            "uri": "playlist/37i9dQZF1DWWEJlAGA9gs0",
            "title": "classical essentials",
            "mood": mNeutral,
        },
        {
            "uri": "playlist/3NrIlsfVP62YZdwzNpX6gp",
            "title": "songs that make you feel like a villain",
            "mood": mAngry,
        },
        {
            "uri": "playlist/37i9dQZF1DXa9wYJr1oMFq",
            "title": "pop punk powerhouse",
            "mood": mHappy,
        },
        {
            "uri": "playlist/3uQaubDvQvBSYIObVHtbnN",
            "title": "disgusted by people and by myself",
            "mood": mDisgusted,
        },
        {
            "uri": "playlist/3c0Nv5CY6TIaRszlTZbUFk",
            "title": "sad songs 2022",
            "mood": mSad,
        },
        {
            "uri": "album/6vvN8noC5dToR8W9WZPyRO",
            "title": "the missing man ",
            "mood": mAngry,
        },
        {
            "uri": "playlist/37i9dQZF1DXb3m918yXHxA",
            "title": "yacht rock",
            "mood": mHappy,
        },
        {
            "uri": "playlist/1xFTW4idq3merKc6M1qjAe",
            "title": "sad songs for crying at 3am",
            "mood": mSad,
        },
        {
            "uri": "album/1Zd0oRtoHZa6HTQ7f0diiZ",
            "title": "sad cello and piano",
            "mood": mSad,
        },
        {
            "uri": "album/6HQ5FnWEsk4rJ2vKgHx1O6",
            "title": "scary world",
            "mood": mFearful,
        },
        {
            "uri": "album/2NkWrhAySgDGEUOTcMV4uG",
            "title": "die die lullaby",
            "mood": mFearful,
        },
        {
            "uri": "playlist/0l9dAmBrUJLylii66JOsHB",
            "title": "angry mood",
            "mood": mAngry,
        },
        {
            "uri": "playlist/37i9dQZF1DWVlYsZJXqdym",
            "title": "happy pop hits",
            "mood": mHappy,
        },
        {
            "uri": "playlist/1w5U47CbmVgcGqIHMxyIgE",
            "title": "original windows down speakers up",
            "mood": mHappy,
        },
        {
            "uri": "playlist/37i9dQZF1DX7KNKjOK0o75",
            "title": "have a great day",
            "mood": mHappy,
        },
        {"uri": "playlist/37i9dQZF1DX7qK8ma5wgG1", "title": "sad songs", "mood": mSad},
    ]
    for playlist in playlists:
        db.session.add(
            models.Playlist(
                uri=playlist["uri"],
                title=playlist["title"],
                genre=gDance,
                mood=playlist["mood"],
            )
        )
    db.session.commit()

    # logging.info("filling Scores table")
    # # initializing score table with random scores
    # score1 = models.Score(
    #     user=user1, playlist=playlist1, score=1, mood=mNeutral, date=datetime.now()
    # )
    # db.session.add(score1)
    # db.session.commit()
    logging.info("database initializing complete")
