from app.users import bp
from flask import request, jsonify, make_response, asc
from app.models import User, Genre, Mood
from app.utils import crypto, auth, DEFAULT_MOOD, DEFAULT_GENRE, COOKIE_NAME, BLACKLISTED, DEFAULT_COUNT
from app import db

@bp.route('/<username>', methods=['GET'])
def getUser(username: str):
	token = request.cookies.get(COOKIE_NAME)
	user = auth.verify_token(token)
	if user is None:
		return {'success': False, 'message': 'invalid username'}, 404
	return user

@bp.route('/multiple/', methods=['GET'])
def getUsers():
	# implement having multiple pages of users of length `count`
	# count is specified as a query parameter
	# pages are implemented using an `offset` variable that defaults to 0
	start = request.args.get('start') or 0
	count = request.args.get('count') or DEFAULT_COUNT
	users = User.query.order_by(asc(User.id)).offset(start).limit(count).all()
	res = []
	for user in users:
		res.append(user.toDict())
	return {'success': True, 'users': res}

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

@bp.route('/update', methods=['PUT'])
def update():
	# checking auth cookie 
	token = request.cookies.get(COOKIE_NAME)
	if not auth.verify_blacklist(token):
		return {'success': False, 'message': 'invalid authorization cookie'}, 403
	user = auth.verify_token(token)
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
	exceptions = ['username', 'passwordHash', 'preferredGenreid', 'commonMoodid', 'genre', 'commonMood']
	for key in content:
		if key not in exceptions and hasattr(user, key):
			setattr(user, key, content.get(key))
	db.session.commit()
	return {'success': True, 'message': 'update successful'}

@bp.route('/delete', methods=['DELETE'])
def delete():
	token = request.cookies.get(COOKIE_NAME)
	if not auth.verify_blacklist(token):
		return {'success': False, 'message': 'invalid authorization cookie'}, 403
	user = auth.verify_token(token)
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
	auth.blacklist_token(token)
	return {'success': True, 'message': 'user deleted successfully'}

@bp.route('/logout', methods=['PUT'])
def logout():
	token = request.cookies.get(COOKIE_NAME)
	if not auth.verify_blacklist(token):
		return {'success': False, 'message': 'invalid authorization cookie'}, 403
	user = auth.verify_token(token)
	if user is None:
		return {'success': False, 'message': 'invalid authorization cookie'}, 403
	content = request.get_json()
	if content.get('username') is None:
		return {'success': False, 'message': 'missing username'}, 422
	if content.get('username') != user.username:
		# unauthorized operation
		return {'success': False, 'message': 'invalid authorization cookie'}, 403
	# blacklisting token
	auth.blacklist_token(token)
	response = make_response(jsonify({'success': True, 'message': 'token invalidated'}))
	response.set_cookie(COOKIE_NAME, '', expires=0)
	return response
