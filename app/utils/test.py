from functools import wraps

def middleware1(f):
	@wraps(f)
	def decorated_function(var, *args, **kwargs):
		# some_input = input()
		print("call middleware 1")
		if(var == "exit"):
			return
		return f(var, *args, **kwargs)
	return decorated_function

def middleware2(f):
	@wraps(f)
	def decorated_function(var, *args, **kwargs):
		# some_input = input()
		print("call middleware 2")
		if(var == "exit"):
			return
		return f(var, *args, **kwargs)
	return decorated_function

@middleware1
@middleware2
def f(var):
	print("f executed")
	return 

if __name__ == "__main__":
	some_global_var = "don't exit"
	f(some_global_var)