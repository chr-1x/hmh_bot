#
# Dummy module for testing handmade methods
#
class CmdFuncPair:
	def __init__(self, cmds, func):
		self.cmds = cmds
		self.func = func

cmds = []
funcs = []

def commands(*args):
	cmds.extend(args)
	def res(func):
		funcs.append(CmdFuncPair(args, func))
		return func
	return res