from willie.tools import stderr
from sqlobject import *
from sqlobject.dbconnection import dbConnectionForScheme
import parsedatetime
import arrow
import random

import os, sys
sys.path.append(os.path.dirname(__file__))

from handmade import command, adminonly, whitelisted_streamtime

dateParser = parsedatetime.Calendar()
dbURI = 'sqlite:/:memory:'
defaultTz = 'US/Pacific'

def requireDb():
	if (not hasattr(sqlhub, 'threadConnection') ): # Ensure whatever thread we are in has its own db connection.
		sqlhub.threadConnection = dbConnectionForScheme('sqlite').connectionFromURI(dbURI)

class Quote(SQLObject):
	text = StringCol()
	timestamp = IntCol()

	def _get_time(self, tz=defaultTz):
		return arrow.get(self.timestamp).to(tz)

	def _set_time(self, newStart):
		self.timestamp = newStart.to('UTC').timestamp

def setup(bot):
	global dbURI
	dbURI = bot.config.db.userdb_type+'://'+os.path.abspath(bot.config.db.userdb_file) # URI must be absolute.
	requireDb()
	Quote.createTable(ifNotExists=True)

def getQuote(quoteId):
	try:
		return Quote.get(quoteId);
	except SQLObjectNotFound:
		return None

@adminonly
@command("addquote", "aq")
def addQuote(bot, trigger):
	requireDb()
	if(not trigger.group(2)):
		bot.say("No quote Text provided!")
		return

	text = trigger.group(2)
	# Perhaps someone would want to set the time for a quote.
	newQuote = Quote(text=text, timestamp=arrow.now().timestamp)
	bot.say("Quote #%d added!" % (newQuote.id))

@adminonly
@command("deletequote", "dq")
def delQuote(bot, trigger):
	requireDb()
	if(not trigger.group(2)):
		bot.say("Usage: !deletequote <quote id>")
		return

	quote = getQuote(trigger.group(2))
	if(quote == None): #NOTE(dustin) was this change of != to == correct?
		bot.say("Could not find quote #%s" % (trigger.group(2)))
		return

	bot.say("Deleted quote %i '%s'" % (quote.id, quote.text))
	quote.destroySelf()

@adminonly
@command("fixquote", "fq", "edit", "editQuote")
def fixQuote(bot, trigger):
	requireDb()
	if(not trigger.group(2)):
		bot.say("Usage: !fixquote <quote id> <quote text>")
		return

	split = trigger.group(2).split(' ', 1);
	if(len(split) != 2):
		bot.say("Please provide the fixed quote!")
		return

	quote = getQuote(split[0])
	if(quote == None):
		bot.say("Could not find quote #%s" % (split[0]))
		return

	quote.text = split[1]
	bot.say('Quote #%d fixed to "%s"' % (quote.id, quote.text))

@adminonly
@command("fixquotetime", "fqt")
def fixQuoteTime(bot, trigger):
	requireDb()
	if(not trigger.group(2)):
		bot.say("Usage: !fixquotetime <quote id> <quote time>")
		return

	split = trigger.group(2).split(' ', 1);
	if(len(split) != 2):
		bot.say("Please provide the fixed quote time!")
		return

	quote = getQuote(split[0])
	if(quote == None):
		bot.say("Could not find quote #%s" % (split[0]))
		return

	pTime,flag = dateParser.parseDT(split[1], sourceTime=arrow.now(defaultTz)) # use beginning of today as the source day to ensure DT returned.
	#Anything not explicitly dated will go to next occurance of that date
	#so check if the date given was pushed more than 6 months in the future
	#if it was assume the issuer ment the past. Will break setting dates manually with years.
	pTime = arrow.get(pTime, defaultTz) # avoid python AWFUL datetimes.
	if (pTime > arrow.now(defaultTz).replace(months=+6)):
			pTime = pTime.replace(years=-1)

	quote.timestamp = pTime.to('UTC').timestamp;
	bot.say("Quote #%d moved to date: %s" %(quote.id, quote.time.strftime("%b %d")))


@whitelisted_streamtime
@command("randomquote", "rq")
def randomQuote(bot, trigger):
	requireDb()
	query = Quote.select()
	numQuotes = query.count()
	if(numQuotes < 1):
		return
	randomNum = random.randrange(numQuotes)
	quote = query[randomNum]
	bot.say('(#%d)"%s" -Casey %s' % (quote.id, quote.text, quote.time.strftime("%b %d")))

#flamedog alais is because of flamedog using all the time.
@whitelisted_streamtime
@command("sayquote", "quote", "flamedog", "q")
def sayQuote(bot, trigger):
	args = trigger.group(2);
	if(args):
		quoteNum = -1
		try:
			quoteNum = int(args)
		except ValueError:
			bot.say("Hey now, quotes have integer IDs! I can't read %s as an integer!" % args)
		quote = getQuote(quoteNum)
		if(quote == None):
			bot.say("No such quote found!")
		else:
			bot.say('(#%d)"%s" -Casey %s' % (quote.id, quote.text, quote.time.strftime("%b %d")))
	else:
		randomQuote(bot, trigger)

#NOTE(effect0r): This should probably be changed to query the db using a regex of searchString to eliminate the forloop,
#                but my knowledge of SQLobject is too limited to properly form such a statement
#searchquote - find a quote basted on a search string
@whitelisted_streamtime
@command("findquote", "fquote")
def findQuote(bot, trigger):
	requireDb()
	reply = ""
	totalQuotes = 0

	searchString = trigger.group(2)
	if (searchString):
		quotes = Quote.select()
		for q in quotes:
			if q.text.lower().find(searchString.lower()) > -1:
				reply = reply + str(q.id) + " "
				totalQuotes += 1
		if reply == "":
			bot.say("No quotes found with string %s" % searchString.lower())
		else:
			bot.say("Found %d quote(s) matching %s: %s" % (totalQuotes, searchString.lower(), reply))
	else:
		bot.say("Usage: !findquote <word> or !fquote <word>")


