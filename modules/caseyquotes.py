from willie.tools import stderr
from sqlobject import *
from sqlobject.dbconnection import dbConnectionForScheme
import parsedatetime
import arrow
import random

import os, sys
sys.path.append(os.path.dirname(__file__))

from handmade import command, adminonly, whitelisted_streamtime

dbURI = 'sqlite:/:memory:'
defaultTz = 'US/Pacific'

def requireDb():
	if ( not hasattr(sqlhub, 'threadConnection') ): # Ensure whatever thread we are in has its own db connection.
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
	dbURI = bot.config.db.userdb_type+':/'+os.path.abspath(bot.config.db.userdb_file) # URI must be absolute.
	requireDb()
	Quote.createTable(ifNotExists=True)

@adminonly
@command("addquote", "aq")
def addQuote(bot, trigger):
	requireDb()
	text = trigger.group(2)
	# Perhaps someone would want to set the time for a quote.
	Quote(text=text, timestamp=arrow.now().timestamp)
	bot.say("Quote added!")

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
	bot.say('"%s" -Casey %s' % (quote.text, quote.time.strftime("%b %d")))

