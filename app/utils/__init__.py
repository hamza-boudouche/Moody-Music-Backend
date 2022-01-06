DEFAULT_GENRE = "chill"
DEFAULT_MOOD = "happy"
COOKIE_NAME = "moodymusiclogin"
BLACKLISTED = b"blacklisted"
DEFAULT_COUNT = 10
AWAITING_CONFIRMATION = b"awaiting confirmation"
CACHE_TIMEOUT = 30 * 60
DEFAULT_PLAYLIST_HISTORY_COUNT = 5
URL_BASE = "http://localhost:5000"

from app.utils import crypto
from app.utils import auth
from app.utils import validate
from app.utils import mail
from app.utils import middleware
from app.utils import recognition

from enum import Enum


class Mood(Enum):
    ANGRY = 0
    DISGUSTED = 1
    FEARFUL = 2
    HAPPY = 3
    NEUTRAL = 4
    SAD = 5
    SURPRISED = 6
