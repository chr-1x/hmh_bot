

class Willie:

	def say(self, text, max_messages=1):
		print("chronalrobot: %s" % text)

	def msg(self, text, max_messages=1):
		print("(chronalrobot): %s" % text)

class CmdFuncPair:
	def __init__(self, cmds, func):
		self.cmds = cmds
		self.func = func

class module:
	cmds = []
	funcs = []

	def commands(*args):
		module.cmds.extend(args)
		def res(func):
			module.funcs.append(CmdFuncPair(args, func))
			return func
		return res