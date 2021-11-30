import os
from dotenv import load_dotenv, find_dotenv
from jwt import encode, decode
from datetime import datetime
import json

def generate_token(user):
	load_dotenv(find_dotenv())
	secret = os.environ.get("SECRET")
	return encode({'id': user.id, 'username': user.username, 'email': user.email, 'preferredGenre': user.genre, 'commonMood': user.mood, 'timestamp': datetime.now()}, secret, algorithm="HS256")

def verify_token(token):
	load_dotenv(find_dotenv())
	secret = os.environ.get("SECRET")
	try:
		user = json.loads(json.dumps(decode(token, secret, algorithms=["HS256"])))
		return {'username': user.get('username'), 'email': user.get('email'), 'preferredGenre': user.get('preferredGenre'), 'commonMood': user.get('commonMood')}
	except:
		return None
