from app import db

class Genre(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(64), index=True, unique=True)
	description = db.Column(db.Text)
	preferredByUsers = db.relationship('User', backref=db.backref('genre', lazy=True), lazy=True)
	playlists = db.relationship('Playlist', backref=db.backref('genre', lazy=True), lazy=True)

	def __repr__(self):
		return f"<Genre {self.id} - title : {self.title} - description : {self.description}>"

class Mood(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(64), index=True, unique=True)
	description = db.Column(db.Text)
	users = db.relationship('User', backref=db.backref('commonMood', lazy=True), lazy=True)
	playlists = db.relationship('Playlist', backref=db.backref('mood', lazy=True), lazy=True)
	scores = db.relationship('Score', backref=db.backref('mood', lazy=True), lazy=True)

	def __repr__(self):
		return f'<Mood {self.id} - title : {self.title} - description : {self.description}>'
class User(db.Model):
	# __table_args__ = {'extend_existing': True}
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(64), index=True, unique=True, nullable=False)
	email = db.Column(db.String(128), index=True, unique=True, nullable=False)
	passwordHash = db.Column(db.String(128), nullable=False)
	preferredGenreid = db.Column(db.Integer, db.ForeignKey('genre.id'))
	commonMoodid = db.Column(db.Integer, db.ForeignKey('mood.id'))
	# playlists = db.relationship('Score', back_populates='playlist')
	playlists = db.relationship('Score', lazy='subquery', backref=db.backref('user', lazy=True))

	def __repr__(self):
		return f"<User {self.id} - username : {self.username} - email : {self.email}>"

class Playlist(db.Model):
	# __table_args__ = {'extend_existing': True}
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	uri = db.Column(db.String(64))
	title = db.Column(db.String(64), index=True, unique=True, nullable=False)
	genreid = db.Column(db.Integer, db.ForeignKey("genre.id"))
	moodid = db.Column(db.Integer, db.ForeignKey('mood.id'))
	users = db.relationship('Score', lazy='subquery', backref=db.backref('playlist', lazy=True))

	def __repr__(self):
		return f"<Playlist {self.uri} - title : {self.title} - genre : {self.genre} - mood : {self.mood}>"

# use of association table https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#association-object 
class Score(db.Model):
	# __table_args__ = {'extend_existing': True}
	userid = 	db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	playlistid = db.Column(db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
	score = db.Column(db.Integer)
	moodid = db.Column(db.Integer, db.ForeignKey('mood.id'))
	# user = db.relationship('User', back_populates='playlists')
	# playlist = db.relationship('Playlist', back_populates='users')

	def __repr__(self):
		return f"<Score - user : {self.user} - playlist : {self.playlist} - score : {self.score} - mood : {self.mood}>"
