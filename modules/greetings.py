from willie.tools import stderr
from sqlobject import *
from sqlobject.dbconnection import dbConnectionForScheme
import parsedatetime
import arrow

import os, sys
sys.path.append(os.path.dirname(__file__))

from handmade import command, whitelisted, whitelisted_streamtime

@command("o/", hide=True)
def MorningYou(bot, trigger) :
	if(trigger) :
		args = trigger.group(2)
		if (args) :
			bot.say("Good Morning @%s!" % (args))

@command("\\\\o/", hide=True)
def MorningAll(bot, trigger):
	bot.say("Good Morning Everyone!")

@command("UGT", hide=True)
def ExplainUGT(bot, trigger):
	bot.say("Use UGT to greet people! It's always morning when you arrive, and always night when you leave ;) You can also use !o/ and !\o/.")