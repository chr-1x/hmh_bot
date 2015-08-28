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
    text = text.strip('"')
    # Perhaps someone would want to set the time for a quote.
    newQuote = Quote(text=text, timestamp=arrow.now().timestamp)
    bot.say("Added as !quote %d." % (newQuote.id))

@adminonly
@command("deletequote", "dq")
def delQuote(bot, trigger):
	requireDb()
	if(not trigger.group(2)):
		bot.say("Usage: !deletequote <quote id>")
		return

	quote = getQuote(trigger.group(2))
	if(quote == None): #NOTE(dustin) was this change of != to == correct?
		bot.say("Could not find quote id%s" % (trigger.group(2)))
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
		bot.say("Could not find quote id%s" % (split[0]))
		return

	quote.text = split[1]
	bot.say('Quote #%d fixed to "%s"' % (quote.id, quote.text))

@adminonly
@command("fixquotetime", "fqt")
def fixQuoteTime(bot, trigger):
    requireDb()
    if(not trigger.group(2)):
        bot.say("Usage: !fixquotetime <quote id> month day year ")
        return

    # NOTE(effect0r): splits to [id] [month day year] then to [mm][dd][yy] 
    #                 to provide an error condition.
    split = trigger.group(2).split(' ', 1)

    date = split[1].split(' ') #split splits
    if(len(date) < 3):
        bot.say("Please provide the fixed quote time!")
        return

    if(len(date[2]) < 4):
        bot.say("Please provide a year!")
        return
    
    quote = getQuote(split[0])
    if(quote == None):
        bot.say("Could not find quote id%s" % (split[0]))
        return

    pTime,flag = dateParser.parseDT(split[1], sourceTime=arrow.now(defaultTz)) # use beginning of today as the source day to ensure DT returned.
    
    pTime = arrow.get(pTime, defaultTz) # avoid python AWFUL datetimes.
    
    quote.timestamp = pTime.to('UTC').timestamp;
    bot.say("Quote #%d moved to date: %s" %(quote.id, quote.time.strftime("%b %d %Y")))


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
	bot.say('(#%d) "%s" --Casey, %s' % (quote.id, quote.text, quote.time.strftime("%b %d %Y")))

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
			bot.say('(#%d) "%s" --Casey, %s' % (quote.id, quote.text, quote.time.strftime("%b %d %Y")))
	else:
		randomQuote(bot, trigger)

#searchquote - find a quote basted on a search string. Outputs the quote if only one is found
@whitelisted_streamtime
@command("searchquote", "squote", "sq")
def findQuote(bot, trigger):
    requireDb()
    reply = ""
    
    searchString = trigger.group(2)
    if (searchString):
        searchString = searchString.replace("'", "\'")
        try:
            selectQuotes = Quote.select(LIKE(Quote.q.text,"%" + searchString + "%"))
        except SQLObjectNotFound:
            pass
        if (selectQuotes):
            quotes = selectQuotes
            totalQuotes = 0
            for q in quotes:
                reply = reply + str(q.id) + ", "
                totalQuotes += 1
                
            if reply == "":
                bot.say("No quotes found with string %s" % searchString.lower())
            else:
                if (totalQuotes == 1):
                    # remove the final ", ", and cast to an integer to lookup quote.
                    try:
                        quoteNumber = int(reply[:(len(reply)-2)])
                    except ValueError:
                        print("findQuote: Couldn't cast reply to int")
                    quote = getQuote(quoteNumber)
                    bot.say('(#%d)" %s" --Casey, %s' % (quote.id, quote.text, quote.time.strftime("%b %d %Y")))
                        
                else:
                    # remove the final ", "
                    reply = reply[:(len(reply)-2)]
                    bot.say("Found %d quotes matching %s: %s" % (totalQuotes, searchString.lower(), reply))
        else:
            bot.say("No quotes found with string %s" % searchString.lower())
    else:
        bot.say("Usage: !searchquote, !squote, or !sq <word>")
