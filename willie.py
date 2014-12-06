

class Willie:

	def say(self, text, max_messages=1):
		print("chronalrobot: %s" % text)

	def msg(self, text, max_messages=1):
		print("(chronalrobot): %s" % text)

class Trigger:
	def __init__(self, **kwargs):
		for arg in kwargs:
			setattr(self, arg, kwargs[arg])

	def group(self, num):
		if (hasattr(self, "args") and len(self.args) > 1):
			return " ".join(self.args[1].split(" ")[1:])

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