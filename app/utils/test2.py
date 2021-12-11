import logging
logging.debug('test2 module')

class A:
	def __init__(self, name):
		self.name = name

	def useA(self):
		A.sayHi()

	@staticmethod
	def sayHi():
		print("hello world 2")

class B:
	def __init__(self, thing):
		self.thing = thing
	@staticmethod
	def sayHi():
		print("hello world")