from app import db

class Genre(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(64), index=True, unique=True)
	description = db.Column(db.Text)
	preferredByUsers = db.relationship('User', backref=db.backref('genre', lazy=True), lazy=True)
	playlists = db.relationship('Playlist', backref=db.backref('genre', lazy=True), lazy=True)

	def toDict(self):
		return {'id': self.id, 'title': self.title, 'description': self.description}

	def __repr__(self):
		return f"<Genre {self.id} - title : {self.title} - description : {self.description}>"

class Mood(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(64), index=True, unique=True)
	description = db.Column(db.Text)
	users = db.relationship('User', backref=db.backref('commonMood', lazy=True), lazy=True)
	playlists = db.relationship('Playlist', backref=db.backref('mood', lazy=True), lazy=True)
	scores = db.relationship('Score', backref=db.backref('mood', lazy=True), lazy=True)

	def toDict(self):
		return {'id': self.id, 'title': self.title, 'description': self.description}

	def __repr__(self):
		return f'<Mood {self.id} - title : {self.title} - description : {self.description}>'
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(64), index=True, unique=True, nullable=False)
	email = db.Column(db.String(128), index=True, unique=True, nullable=False)
	passwordHash = db.Column(db.String(128), nullable=False)
	preferredGenreid = db.Column(db.Integer, db.ForeignKey('genre.id'))
	commonMoodid = db.Column(db.Integer, db.ForeignKey('mood.id'))
	newPlaylists = db.relationship('Playlist', lazy='subquery', backref=db.backref('owner', lazy=True))
	playlists = db.relationship('Score', lazy='subquery', backref=db.backref('user', lazy=True))

	def toDict(self, include_email=False):
		if(include_email):
			return {'id': self.id, 'username': self.username, 'email': self.email, 'preferredGenre': self.genre, 'commonMood': self.commonMood}
		return {'id': self.id, 'username': self.username, 'preferredGenre': self.genre, 'commonMood': self.commonMood}

	def __repr__(self):
		return f"<User {self.id} - username : {self.username} - email : {self.email}>"

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

	def __repr__(self):
		return f"<Playlist {self.uri} - title : {self.title} - genre : {self.genre} - mood : {self.mood}>"

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
