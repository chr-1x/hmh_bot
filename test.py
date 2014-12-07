import handmade
import willie
import random
from datetime import datetime
from pytz import timezone

bot = willie.Willie()

def printTitle(title):
	numeq = len(title) + 12
	print("="*numeq)
	print("///   %s   ///" % title)
	print("="*numeq)

def testAllCommands():
	printTitle("Handmade Hero Command Test Cases")

	for cfp in willie.module.funcs:
		#print(cfp.cmds)
		print("\n%s" % ", ".join(cfp.cmds))
		cfp.func(bot, None)

		handmade.aliasList(bot, willie.Trigger(nick="senderGuy", args=["#channel", "!alias %s" % random.choice(cfp.cmds)]))


	print("\nTotal Commands: %s\n" % len(handmade.commands))

def testInfoCommands():
	printTitle("Handmade Hero Info Commands Test Cases")

	handmade.time(bot, willie.Trigger(nick="senderGuy"))
	handmade.time(bot, willie.Trigger(nick="senderGuy", args=["#channel", "!cmd dumbGuy dummyArg"]))
	handmade.keyboardInfo(bot, willie.Trigger(nick="senderGuy", args=["#channel", "!cmd dumbGuy dummyArg"]))

	print("\n")

# Cases we need to check:
# 1) stream time greater than now time
# 2) stream time less than now time
# 3) stream time where now time is during stream
# 4) stream time where now time is during Q&A
# 5) stream time is in different year
# 6) timezones don't match
def testStreamTimer():

	printTitle("Stream Timer Test Cases")

	def t(year, month, day, hour, minute=0, second=0):
		return datetime(year, month, day, hour, minute, second, 0, timezone("PST8PDT"))
	def tUtc(year, month, day, hour, minute=0, second=0):
		return datetime(year, month, day, hour, minute, second, 0)

	streamTimes = [ t(2014, 12, 1, 20    ), t(2014, 12, 1, 20), t(2014, 12, 1, 20    ), t(2014, 12, 1, 20    ), t(2015, 1, 1, 11, 36), tUtc(2014, 12, 2, 4) ]
	nowTimes = 	  [ t(2014, 12, 1, 15, 41), t(2014, 12, 2, 15), t(2014, 12, 1, 20, 35), t(2014, 12, 1, 21, 15), t(2014, 12, 29, 21), t(2014, 12, 2, 4, 2) ]

	for i in range(len(streamTimes)):
		print(handmade.timeToStream(streamTimes[i], nowTimes[i]))

testAllCommands()
testInfoCommands()
testStreamTimer()