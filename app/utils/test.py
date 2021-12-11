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
	# some_global_var = "don't exit"
	# f(some_global_var)
	# import logging
	# with open('example.log', 'w'):
	# 	pass
	# logging.basicConfig(filename='example.log', level=logging.DEBUG)
	# logging.debug('This message should go to the log file')
	# logging.info('So should this')
	# logging.warning('And this, too')
	# logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
	# from test2 import A
	# from test2 import A, B
	# a = A("hamza")
	# a.useB()
	# def test_func():
	# 	return 1, 2
	# first, second = test_func()
	# print(first, second)
	# from test2 import A
	# a = A("hamza")
	# a.useA()
	# from test2 import A
	# a = A("hello")
	# b = A("hello")
	# print(a == b)
	pass