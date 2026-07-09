from tests.Hash import *

reg = []
def register(value):
	def wrapper(*args, **kwargs):
		a = args
		reg.append([HASHash(value).hash(), args[0]])
		#_REGISTER += {HASHash(value).hash(): args[0]}
	return wrapper

