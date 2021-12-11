DEFAULT_GENRE = "happy"
DEFAULT_MOOD = "happy"
COOKIE_NAME = "moodymusiclogin"
BLACKLISTED = "blacklisted"
DEFAULT_COUNT = 10
AWAITING_CONFIRMATION = "awaiting confirmation"
CACHE_TIMEOUT = 30*60

from app.utils import crypto
from app.utils import auth
from app.utils import validate
from app.utils import mail
from app.utils import middleware