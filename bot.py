
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