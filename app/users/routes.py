from app.users import bp
from markupsafe import escape

@bp.route('/<username>', methods=['GET'])
def getUser(username: str):
	# FIXME: output based on cookie auth
	pass

@bp.route('/check/<username>', methods=['GET'])
def checkUsername(username: str):
	pass

@bp.route('/login', methods=['POST'])
def login():
	pass

@bp.route('/logout', methods=['POST'])
def logout():
	# FIXME: check cookie auth
	pass

@bp.route('/register', methods=['POST'])
def register():
	pass

# TODO: add update and delete methods and endpoints