from willie.tools import stderr
from sqlobject import *
from sqlobject.dbconnection import dbConnectionForScheme
import parsedatetime
import arrow
import math

import os, sys
sys.path.append(os.path.dirname(__file__))

from handmade import command, info, whitelisted, adminonly, whitelisted_streamtime, adminonly_streamtime

dateParser = parsedatetime.Calendar()
defaultTz = 'US/Pacific'
dbURI = 'sqlite:/:memory:' # default to memory so we dont accidently anything
MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

def requireDb():
	if ( not hasattr(sqlhub, 'threadConnection') ): # Ensure whatever thread we are in has its own db connection.
		sqlhub.threadConnection = dbConnectionForScheme('sqlite').connectionFromURI(dbURI)

class StreamEpisode(SQLObject):
	startTimestamp = IntCol(default=-1)
	streamLength = IntCol(default=60)
	qaLength = IntCol(default=30)

	
	def _init(self, *args, **kw):
		SQLObject._init(self, *args, **kw)

	def _get_start(self, tz=defaultTz):
		return arrow.get(self.startTimestamp).to(tz)

	def _set_start(self, newStart):
		self.startTimestamp = newStart.to('UTC').timestamp

	def getQaStart(self):
		return self.start.replace(minutes=+self.streamLength)

	def getEnd(self):
		return self.start.replace(minutes=+self.streamLength+self.qaLength)

	def __str__(self):
		return "Stream Ep on %s which is %d minutes long with a %d minute q&a" % (self.start.strftime("%b %d %Y at %I:%M%p %Z"), self.streamLength, self.qaLength)

	def getTotalStreamLength(self):
		return timedelta(minutes=self.streamLength+self.qaLength)

def getDurationString(delta, showDays=True, showHours=True, showMinutes=True, showSeconds=False):
	string = [""]

	def appendDuration(num, singular, plural, showZero=False):
		if (num < 0 or num > 1):
			string[0] += "%d %s " % (num, plural)
		elif (num == 1):
			string[0] += "%d %s " % (num, singular)
		elif(showZero):
			string[0] += "%d %s " % (num, plural)
	
	if (showDays):
		appendDuration(delta.days, "day", "days")

	if (showHours):
		appendDuration(int(math.floor(delta.seconds / 3600)), "hour", "hours")

	if (showMinutes):
		appendDuration(int(math.ceil((delta.seconds % 3600) / 60)), "minute", "minutes", showZero=True)

	if (showSeconds):
		appendDuration(delta.seconds % 60, "second", "seconds")

	return string[0][:-1]

def getStartOfDay(someTime=None):
	if(someTime == None):
		someTime = arrow.now(defaultTz)

	return someTime.floor('day')

def getEndOfDay(someTime=None):
	if(someTime == None):
		someTime = arrow.now(defaultTz)
	
	return someTime.ceil('day')

def setup(bot):
	global dbURI 
	dbURI = bot.config.db.userdb_type+'://'+os.path.abspath(bot.config.db.userdb_file) # URI must be absolute.
	requireDb()
	StreamEpisode.createTable(ifNotExists=True)


def getStreamsOnDay(day):
	return getStreamsBetween(getStartOfDay(day), getEndOfDay(day))

def getStreamsToday():
	return getStreamsOnDay(arrow.now(defaultTz))

def getStreamAt(someTime):
	possibleStreams = getStreamsOnDay(someTime)
	for stream in possibleStreams:
		if( stream.start < someTime and someTime < stream.getEnd() ):
			return stream
	return None

def getStreamsBetween(startTime, endTime):
	requireDb()
	streams = StreamEpisode.select(
		AND(
			StreamEpisode.q.startTimestamp > startTime.timestamp, 
			StreamEpisode.q.startTimestamp < endTime.timestamp
		)
	)
	return list(streams)

def getNextStream(fromTime=None):
	if(fromTime == None):
		fromTime = arrow.now()
	requireDb()
	futureStreams = StreamEpisode.select(
		AND(
			StreamEpisode.q.startTimestamp > fromTime.timestamp, 
		), orderBy = StreamEpisode.q.startTimestamp
	)
	for stream in futureStreams:
		return stream
	return None

def isStreamingAt(someTime):
	return getStreamAt(someTime) != None;

def isCurrentlyStreaming():
	return isStreamingAt(arrow.now())

def scheduleStream(newTime):
	"""Sets the time of any existing stream on that day to the new time, or creates one if there is
		no entry.

		newTime is an arrow.arrow.
	"""
	scheduledStreams = getStreamsOnDay(newTime.to('US/Pacific'))
	if(len(scheduledStreams) > 0):
		for streams in scheduledStreams:
			streams.start = newTime
	else:
		StreamEpisode(start=newTime) # Create the new episode.

@adminonly
@command("isStreaming", hide=True)
def isStreamingCommand(bot, trigger):
	streaming = isCurrentlyStreaming()
	if (streaming):
		bot.say("Stream is currently going!")
	else:
		bot.say("Stream is not currently going.")


@command('timer', "when", "howlong", "timeleft")
def timer(bot, trigger):
	"""Info command that prints out the time until the next stream.
	"""
	now = arrow.now();
	currentStream = getStreamAt(now)

	if(currentStream == None):
		# Check if there is a stream coming up.
		nextStream = getNextStream()
		if(nextStream == None):
			return info(bot, trigger, "No more streams scheduled in the bot, Try checking www.handmadehero.org")
		else:
			return info(bot, trigger, "Next stream is in %s" % getDurationString(nextStream.start - now ))

	if( currentStream.start < now  and now < currentStream.getQaStart() ):
		return info(bot, trigger, "%s into stream (%s until Q&A) if Casey is on schedule" % (getDurationString(now - currentStream.start), getDurationString(currentStream.getQaStart() - now)))

	if( currentStream.getQaStart() < now  and now < currentStream.getEnd() ):
		return info(bot, trigger, "%s into the Q&A (%s until end) if Casey is on schedule" % (getDurationString(now - currentStream.getQaStart()), getDurationString(currentStream.getEnd() - now)))

@whitelisted_streamtime
@command('today', 'nextStream')
def nextSchedule(bot, trigger):
	"""Info command that prints out the expected time of the next stream
	"""
	nextStream = getNextStream()
	if( nextStream != None):
		info(bot, trigger, "The stream should next be live on %s PST" % nextStream.start.strftime("%a at %I:%M %p"))
	else:
		info(bot, trigger, "No more streams scheduled in the bot, Try checking www.handmadehero.org")


@whitelisted_streamtime
@command('thisweek')
def currentSchedule(bot, trigger):
	"""Info command that prints out this week's schedule
	"""
	startOfWeek = getStartOfDay()
	if (startOfWeek.weekday() <= FRIDAY):
		startOfWeek = startOfWeek.replace(days=-(startOfWeek.weekday()-MONDAY))
	else: # It's a weekend, go forward to the next week
		startOfWeek = startOfWeek.replace(days=+(SUNDAY-startOfWeek.weekday())+1)

	endOfWeek = startOfWeek.replace(days=+7)

	streams = getStreamsBetween(startOfWeek, endOfWeek)
	streamTimes = " :: ".join([stream.start.strftime("%I %p on %a").lstrip("0") for stream in streams])
	info( bot, trigger, "Schedule for week of %s: %s (times in PST)" % (startOfWeek.strftime("%m/%d"), streamTimes) )

@whitelisted_streamtime
@command('schedule')
def seeSchedule(bot, trigger):
	args = trigger.group(2)
	if (args and trigger.admin):
		reschedule(bot, trigger)
	else:
		currentSchedule(bot, trigger)

@adminonly
@command('setschedule', 'reschedule', hide=True)
def reschedule(bot, trigger):
	"""Allows admins to set stream times on the fly
	"""

	args = trigger.group(2)
	if (args):
		pTime,flag = dateParser.parseDT(args, sourceTime=getStartOfDay().replace(months=-6)) # use beginning of today as the source day to ensure DT returned.
		pTime = arrow.get(pTime, defaultTz) # avoid python AWFUL datetimes.

		if (flag == 1):
			# parsed as a date, so we can't really do anything with it. Just print the schedule for that day.
			stream = getNextStream(pTime)
			if (stream != None):
				tense = "should air"
				if (stream.getEnd() < arrow.now()): 
					tense = "should have aired"
				bot.say("@%s: The stream %s %s" % (trigger.nick, tense, stream.start.strftime("%b %d %I:%M %p %Z")))
			else:
				bot.say("@%s: No stream scheduled for %s" % (trigger.nick, pTime.strftime("%b %d")))
			return

		if (flag == 2):
			#parsed as a time. Assume if its an admin that they want to change the stream time for today.
			if (trigger.admin): 
				scheduleStream(pTime)
				bot.say("@%s: Set the stream time for today(%s) to %s" % (trigger.nick, pTime.strftime("%b %d"), pTime.strftime("%I:%M %p %Z").lstrip("0")))
				return

		if (flag == 3):
			#parsed as a datetime. All is well.
			if (trigger.admin):
				scheduleStream(pTime)
				bot.say("@%s: Set the stream time for %s to %s" % (trigger.nick, pTime.strftime("%b %d"), pTime.strftime("%I:%M %p %Z").lstrip("0")))
				return

		else:
			#Unable to parse. Only respond if its an admin so that non-admins can't spam failed attempts
			if (trigger.admin):
				bot.say("@%s: Sorry, I couldn't figure out what %s meant." % (trigger.nick, args))
				return
	else:
		currentSchedule(bot, trigger)
		return
