from app.users import bp
from flask import request, jsonify, make_response
from sqlalchemy import asc
from app.models import User, Genre, Mood
from app.utils import crypto, auth, validate, mail, COOKIE_NAME, DEFAULT_COUNT, CACHE_TIMEOUT
from app import db
import logging
from jwt import encode, decode
import json
import os

@bp.route('/account', methods=['GET'])
def getUser():
	logging.info(f'request: GET /user/account')
	# FIXME: add number of upvotes, number of downvotes, number of personnal playlists (links to personnel playlists)
	# FIXME: add history of recently iupvoted playlists
	# added to api documentation
	tokenString = request.cookies.get(COOKIE_NAME)
	user = auth.Token.verify(tokenString)
	if user is None:
		return {'success': False, 'message': 'invalid username'}, 404
	return user

@bp.route('/multiple/', methods=['GET'])
def getUsers():
	# implement having multiple pages of users of length `count`
	# count is specified as a query parameter
	# pages are implemented using an `offset` variable that defaults to 0
	# FIXME: for each user, add number of upvotes, number of downvotes, number of personnal playlists (links to personnel playlists) 
	start = request.args.get('start') or 0
	count = request.args.get('count') or DEFAULT_COUNT
	logging.info(f'request: GET /user/multiple - {"start":start, "count":count}')
	users = User.query.order_by(asc(User.id)).offset(start).limit(count).all()
	res = []
	for user in users:
		res.append(user.toDict())
	return {'success': True, 'users': res}

@bp.route('/check/<username>', methods=['GET'])
def checkUsername(username: str):
	# TODO: if not valid add existing user info
	# added to api documentation
	logging.info(f'request: GET /user/check/{username}')
	users = User.query.filter_by(username=username).all()
	if len(users) != 0:
		return {"valid": False}
	return {"valid": True}

@bp.route('/login', methods=['POST'])
def login():
	# TODO: return link to profil photo
	# added to api documentation
	logging.info(f'request: POST /user/login - {request.get_json()}')
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
	token = auth.Token(user)
	response = make_response(jsonify({'success': True, 'message': 'authenticated successfully', 'username': content.get('username')}))
	response.set_cookie(COOKIE_NAME, value = token.tokenString, max_age = 604800, httponly = True)
	return response

@bp.route('/register', methods=['POST'])
def register():
	# added to api documentation
	logging.info(f'request: POST /user/register - {request.get_json()}')
	content = request.get_json()
	if content.get('username') is None or content.get('password') is None or content.get('email') is None:
		return {'success': False, 'message': 'missing username, password and/or email'}, 422
	if User.query.filter_by(username=content.get('username')).count() != 0:
		return {'success': False, 'message': 'invalid username (already bound to another account)'}, 422
	if not validate.validate_email_form():
		return {'success': False, 'message': 'invalid email'}, 400
	if User.query.filter_by(email=content.get('email')).count() != 0:
		return {'success': False, 'message': 'invalid email (already bound to another account)'}, 422
	# else: all imputs are present, and username is valid
	jwt = encode(content, os.environ.get("SECRET"), algorithm="HS256")
	mail.cache_mail(mail=content.get('email'))
	sent = mail.send_mail(mail=content.get('email'), subject="MoodyMusic Email Verification", contents=mail.template_validate_email(content, jwt))
	if sent:
		return {'success': True, 'message': 'waiting for email validation', 'delay': CACHE_TIMEOUT}

@bp.route('/register/validate/<token>', methods=['GET'])
def validate_registration(token):
	logging.info(f'request: GET /user/register/validate/{token}')
	try:
		content = json.loads(json.dumps(decode(token, os.environ.get("SECRET"), algorithms=["HS256"])))
		if not mail.validate_cached_mail(mail=content.get('email')):
			raise Exception('invalid verification token')
		passwordHash = crypto.hash(content.get('password'))
		newUser = User(username=content.get('username'), email=content.get('email'), passwordHash=passwordHash, genre=Genre.get_default_genre(), commonMood=Mood.get_default_mood())
		db.session.add(newUser)
		db.commit()
		return {'success': True, 'message': f'added user {newUser.username} successfully'}
	except:
		return {'success': False, 'message': 'invalid verification token'}

@bp.route('/update', methods=['PUT'])
def update():
	# checking auth cookie 
	# added to api documentation
	logging.info(f'request: PUT /user/update - {request.get_json()}')
	tokenString = request.cookies.get(COOKIE_NAME)
	if not auth.Token.verify_blacklist(tokenString):
		return {'success': False, 'message': 'invalid authorization cookie'}, 403
	user = auth.Token.verify(tokenString)
	if user is None:
		return {'success': False, 'message': 'invalid authorization cookie'}, 403
	# processing request
	content = request.get_json()
	if content.get('username') is None:
		return {'success': False, 'message': 'missing username'}, 422
	if content.get('username') != user.username:
		# unauthorized operation
		return {'success': False, 'message': 'invalid authorization cookie'}, 403
	user = User.query.filter_by(username=content['username']).first()
	if user is None:
		return {'success': False, 'message': 'account not found'}, 404
	user.update(content)
	db.session.commit()
	return {'success': True, 'message': f'update successful - {user}'}

@bp.route('/delete', methods=['DELETE'])
def delete():
	# added to api documentation
	logging.info(f'request: DELETE /user/delete')
	tokenString = request.cookies.get(COOKIE_NAME)
	if not auth.Token.verify_blacklist(tokenString):
		return {'success': False, 'message': 'invalid authorization cookie'}, 403
	user = auth.Token.verify(tokenString)
	if user is None:
		return {'success': False, 'message': 'invalid authorization cookie'}, 403
	content = request.get_json()
	if content.get('username') is None:
		return {'success': False, 'message': 'missing username'}, 422
	if content.get('username') != user.username:
		# unauthorized operation
		return {'success': False, 'message': 'invalid authorization cookie'}, 403
	user = User.query.filter_by(username=content['username']).first()
	if user is None:
		return {'success': False, 'message': 'account not found'}, 404
	db.session.delete(user)
	db.session.commit()
	auth.Token.blacklist(tokenString)
	return {'success': True, 'message': f'user {user.username} deleted successfully'}

@bp.route('/logout', methods=['PUT'])
def logout():
	# added to api documentation
	logging.info(f'request: PUT /user/logout - {request.get_json()}')
	tokenString = request.cookies.get(COOKIE_NAME)
	if not auth.Token.verify_blacklist(tokenString):
		return {'success': False, 'message': 'invalid authorization cookie'}, 403
	user = auth.Token.verify(tokenString)
	if user is None:
		return {'success': False, 'message': 'invalid authorization cookie'}, 403
	content = request.get_json()
	if content.get('username') is None:
		return {'success': False, 'message': 'missing username'}, 422
	if content.get('username') != user.username:
		# unauthorized operation
		return {'success': False, 'message': 'invalid authorization cookie'}, 403
	# blacklisting token
	auth.Token.blacklist(tokenString)
	response = make_response(jsonify({'success': True, 'message': 'token invalidated'}))
	response.set_cookie(COOKIE_NAME, '', expires=0, httponly = True)
	return response
