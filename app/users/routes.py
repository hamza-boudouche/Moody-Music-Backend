from app.users import bp
from markupsafe import escape
from flask import request, jsonify, set_cookie, make_response
from app.models import User, Genre, Mood
from app.utils import crypto, auth, DEFAULT_MOOD, DEFAULT_GENRE, COOKIE_NAME
from datetime import datetime
from app import db
import json

@bp.route('/<username>', methods=['GET'])
def getUser(username: str):
	token = request.cookies.get(COOKIE_NAME)
	user = auth.verify_token(token)
	if user is None:
		return {'success': False, 'message': 'invalid username'}, 404
	return user

@bp.route('/check/<username>', methods=['GET'])
def checkUsername(username: str):
	users = User.query.filter_by(username=username).all()
	if len(users) != 0:
		return {"valid": False}
	return {"valid": True}

@bp.route('/login', methods=['POST'])
def login():
	content = request.get_json()
	if(content.get('username') is None or content.get('password') is None):
		# return a 422 response : missing username or password
		return {'success': False, 'message': 'missing username and/or password'}, 422
	user = User.query.filter_by(username=content.get('username')).first()
	if user == None:
		return {'success': False, 'message': 'wrong username and/or password'}, 403
	if not crypto.check_password(content.get('password'), user.passwordHash):
		return {'success': False, 'message': 'wrong username and/or password'}, 403
	# else: the user is connected successfully, send auth cookie
	token = auth.generate_token(user)
	response = make_response(jsonify({'success': True, 'message': 'authenticated successfully', 'username': content.get('username')}))
	response.set_cookie(COOKIE_NAME, value = token, max_age = 604800, httponly = True)
	return response

@bp.route('/register', methods=['POST'])
def register():
	# FIXME: check if email is valid (regex and email verification)
	content = request.get_json()
	if content.get('username') is None or content.get('password') is None or content.get('email') is None:
		return {'success': False, 'message': 'missing username, password and/or email'}, 422
	if User.query.filter_by(username=content.get('username')).count() != 0:
		return {'success': False, 'message': 'invalid username (already bound to another account)'}, 422
	# else: all imputs are present, and username is valid
	passwordHash = crypto.hash(content.get('password'))
	defaultGenre = Genre.query.filter_by(title=DEFAULT_GENRE).first()
	defaultMood = Mood.query.filter_by(title=DEFAULT_MOOD).first()
	newUser = User(username=content.get('username'), email=content.get('email'), passwordHash=passwordHash, genre=defaultGenre, commonMood=defaultMood)

# TODO: add update and delete methods and endpoints

@bp.route('/logout', methods=['POST'])
def logout():
	# FIXME: check cookie auth
	# TODO: use redis cash to blacklist tokens
	pass
