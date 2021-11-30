from app.music import bp

@bp.route('/<mood>', methods=['GET'])
def getMusic(mood: str):
	pass

@bp.route('/add', methods=['POST'])
def addMusic():
	# FIXME: add cookie auth
	pass

@bp.route('/vote', methods=['PUT'])
def vote():
	# FIXME: add cookie auth
	pass