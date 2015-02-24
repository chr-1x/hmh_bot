from willie.tools import stderr
from sqlobject import *
from sqlobject.dbconnection import dbConnectionForScheme
import parsedatetime
import arrow

import os, sys
sys.path.append(os.path.dirname(__file__))

from handmade import command, whitelisted, whitelisted_streamtime

dateParser = parsedatetime.Calendar()

class ManOrWomanDog:
	pass

__m = ManOrWomanDog()

__m.whoDog = None
__m.manOrWomanDog = None

def sayWhoIsTheManOrWomanNowDog(bot):
	if __m.whoDog is None:
		bot.say("I don't know who's the man now, dog.")
		return
	bot.say("@%s You're the %s now, dog!" % (__m.whoDog, __m.manOrWomanDog))

def youreTheManOrWomanNowDog(bot, trigger, manOrWomanDog):
        __m.whoDog = trigger.group(2)
	__m.manOrWomanDog = manOrWomanDog
	sayWhoIsTheManOrWomanNowDog(bot)

@whitelisted
@command("ytmnd")
def youreTheManNowDog(bot, trigger):
	youreTheManOrWomanNowDog(bot, trigger, 'man')

@whitelisted
@command("ytwnd")
def youreTheWomanNowDog(bot, trigger):
	youreTheManOrWomanNowDog(bot, trigger, 'woman')

@whitelisted
@command("wtmnd", "wtwnd")
def whosTheManNowDog(bot, trigger):
	sayWhoIsTheManOrWomanNowDog(bot)

