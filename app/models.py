from app import db
from app.utils import DEFAULT_MOOD, DEFAULT_GENRE

class Genre(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(64), index=True, unique=True)
	description = db.Column(db.String(256))
	preferredByUsers = db.relationship('User', backref=db.backref('genre', lazy=True), lazy=True)
	playlists = db.relationship('Playlist', backref=db.backref('genre', lazy=True), lazy=True)

	def toDict(self):
		return {'id': self.id, 'title': self.title, 'description': self.description}

	def __repr__(self):
		return f"<Genre {self.id} - title : {self.title} - description : {self.description}>"

	def __eq__(self, other):
		return self.id == other.id

	@staticmethod
	def get_default_genre():
		return Genre.query.filter_by(title=DEFAULT_GENRE).first()
class Mood(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(64), index=True, unique=True)
	description = db.Column(db.String(256))
	users = db.relationship('User', backref=db.backref('commonMood', lazy=True), lazy=True)
	playlists = db.relationship('Playlist', backref=db.backref('mood', lazy=True), lazy=True)
	scores = db.relationship('Score', backref=db.backref('mood', lazy=True), lazy=True)

	def toDict(self):
		return {'id': self.id, 'title': self.title, 'description': self.description}

	def __eq__(self, other):
		return self.id == other.id

	def __repr__(self):
		return f'<Mood {self.id} - title : {self.title} - description : {self.description}>'

	@staticmethod
	def get_default_mood():
		return Mood.query.filter_by(title=DEFAULT_MOOD).first()
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(64), index=True, unique=True, nullable=False)
	email = db.Column(db.String(128), index=True, unique=True, nullable=False)
	passwordHash = db.Column(db.String(128), nullable=False)
	preferredGenreid = db.Column(db.Integer, db.ForeignKey('genre.id'))
	commonMoodid = db.Column(db.Integer, db.ForeignKey('mood.id'))
	newPlaylists = db.relationship('Playlist', lazy='subquery', backref=db.backref('owner', lazy=True), cascade="all, delete")
	playlists = db.relationship('Score', lazy='subquery', backref=db.backref('user', lazy=True), cascade="all, delete")

	def toDict(self, include_email=False):
		if(include_email):
			return {'id': self.id, 'username': self.username, 'email': self.email, 'preferredGenre': self.genre, 'commonMood': self.commonMood}
		return {'id': self.id, 'username': self.username, 'preferredGenre': self.genre, 'commonMood': self.commonMood}

	def __repr__(self):
		return f"<User {self.id} - username : {self.username} - email : {self.email}>"

	def __eq__(self, other):
		return self.id == other.id

	def add(self, uri, title, genre, mood):
		newPlaylist = Playlist(uri=uri, title=title, genre=genre, mood=mood, owner=self)
		db.session.add(newPlaylist)
		db.session.commit()
		return {'success': True, 'message': f'playlist {newPlaylist.title}@{newPlaylist.id} added successfully by user {self.username}@{self.id}'}, 200

	def vote(self, uri, vote, mood):
		playlist = Playlist.query.filter_by(uri=uri)
		if playlist is None:
			return {'success': False, 'message': 'playlist not found'}, 404
		score = Score.query.filter_by(user=self, playlist=playlist).first()
		if score is None:
			score = Score(user=self, playlist=playlist, score=vote, mood=mood)
			db.session.add(score)
			db.session.commit()
		else:
			score.score = vote
			db.session.commit()
		# set string that describes the operation
		operation = "upvoted"
		if vote == -1:
			operation = "downvoted"
		elif vote == 0:
			operation = "reset"
		return {'success': True, 'score': f"{uri} {operation} successfully"}, 200

	def update(self, dict):
		for key in dict:
			# if key == 'username':
			# 	if len(User.query.filter_by(username=dict.get(key)).all()) == 0:
			# 		setattr(self, key, dict.get(key))
			pass
			# update some attributes
class Playlist(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	uri = db.Column(db.String(128))
	title = db.Column(db.String(64), index=True, unique=True, nullable=False)
	genreid = db.Column(db.Integer, db.ForeignKey("genre.id"))
	moodid = db.Column(db.Integer, db.ForeignKey('mood.id'))
	ownerid = db.Column(db.Integer, db.ForeignKey('user.id'))
	users = db.relationship('Score', lazy='subquery', backref=db.backref('playlist', lazy=True))

	def toDict(self):
		return {'uri': self.uri, 'title': self.title, 'genre': self.genre, 'mood': self.mood}

	def __eq__(self, other):
		return self.id == other.id

	def __repr__(self):
		return f"<Playlist {self.uri} - title : {self.title} - genre : {self.genre} - mood : {self.mood}>"

	def delete(self, user):
		db.session.delete(self)
		db.session.commit()
		return {'success': True, 'message': f'user {user.username} deleted successfully'}, 200

# use of association table https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#association-object 
class Score(db.Model):
	userid = 	db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	playlistid = db.Column(db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
	score = db.Column(db.Integer)
	moodid = db.Column(db.Integer, db.ForeignKey('mood.id'))

	def toDict(self):
		return {'user': self.user, 'playlist': self.playlist, 'score': self.score, 'mood': self.mood}

	def __repr__(self):
		return f"<Score - user : {self.user} - playlist : {self.playlist} - score : {self.score} - mood : {self.mood}>"

	def __eq__(self, other):
		return self.id == other.id
