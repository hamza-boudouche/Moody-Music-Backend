import os
from dotenv import load_dotenv, find_dotenv
from jwt import encode, decode
from datetime import datetime
import json
from app import cache
from app.utils import BLACKLISTED

class Token:
	def __init__(self, user):
		load_dotenv(find_dotenv())
		self.tokenString = encode({'id': user.id, 'username': user.username, 'email': user.email, 'preferredGenre': user.genre, 'commonMood': user.mood, 'timestamp': datetime.now()}, os.environ.get("SECRET"), algorithm="HS256")

	@staticmethod
	def verify(tokenString: str) -> dict:
		load_dotenv(find_dotenv())
		secret = os.environ.get("SECRET")
		try:
			user = json.loads(json.dumps(decode(tokenString, secret, algorithms=["HS256"])))
			return {'username': user.get('username'), 'email': user.get('email'), 'preferredGenre': user.get('preferredGenre'), 'commonMood': user.get('commonMood')}
		except:
			return None

	@staticmethod
	def verify_blacklist(tokenString: str):
		return cache.get(tokenString) != BLACKLISTED

	@staticmethod
	def blacklist(tokenString: str) -> None:
		cache.set(tokenString, BLACKLISTED)