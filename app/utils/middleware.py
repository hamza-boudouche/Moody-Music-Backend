from functools import wraps

def check_auth(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		# do something here
		return f(*args, **kwargs)
	return decorated_function

