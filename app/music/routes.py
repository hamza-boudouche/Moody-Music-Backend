from app.music import bp
from flask import request
from flask import db
from models import Genre, Mood, Playlist

@bp.route('/<mood>', methods=['GET'])
def getMusic(mood: str):
	pass

@bp.route('/add', methods=['POST'])
def addMusic():
	# FIXME: add cookie auth
	content = request.get_json()
	if content.get('uri') is None or content.get('title') is None or content.get('genreid') is None or content.get('moodid') is None:
		return {'success': False, 'message': 'missing uri, title, genreid, and/or moodid'}, 422
	genre = Genre.query.filter_by(id=content.get('genreid')).first()
	if genre is None:
		return {'success': False, 'message': 'genre not found (invalid genreid)'}, 404
	mood = Mood.query.filter_by(id=content.get('moodid')).first()
	if mood is None:
		return {'success': False, 'message': 'mood not found (invalid moodid)'}, 404
	# TODO: verify validity of uri
	newPlaylist = Playlist(uri=content.get('uri'), title=content.get('title'), genre=genre, mood=mood)
	db.session.add(newPlaylist)
	db.session.commit()

@bp.route('/vote', methods=['PUT'])
def vote():
	# FIXME: add cookie auth
	pass
