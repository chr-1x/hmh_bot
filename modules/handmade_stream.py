from datetime import datetime, timedelta, date, time
import pytz
from pytz import timezone

import os, sys
sys.path.append(os.path.dirname(__file__))

from handmade import command, info

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

streams = []

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
        appendDuration(int(delta.seconds / 3600), "hour", "hours")

    if (showMinutes):
        appendDuration(int((delta.seconds % 3600) / 60), "minute", "minutes", showZero=True)

    if (showSeconds):
        appendDuration(delta.seconds % 60, "second", "seconds")

    return string[0][:-1]

def getTotalStreamLength():
    ###TODO(chronister): Make this settable with commands
    return getStreamLength() + getQALength()

def getQALength():
    return timedelta(hours=0, seconds=1800)

def getStreamLength():
    return timedelta(hours=1)

def scheduleStream(newTime):
    """Sets the time of any existing stream on that day to the new time, or creates one if there is
        no entry.

        newTime is a datetime.
    """

    ###REFACTOR(chronister): This code uses two loops, could it be collapsed to one?

    # gives first stream date in the future of the given time
    streamTime = next((t for t in streams if t.date() == newTime.date()), None) 

    if (streamTime == None):
        streams.append(newTime)
    else:
        for i,t in enumerate(streams):
            if (t == streamTime):
                streams[i] = newTime

def getNextStream(nowTime):
    """Returns the datetime of the start of the next stream from the nowTime given if a stream is 
        not currently on, or the datetime of the start of the current stream if the nowTime is
        during one.
    """
    if (nowTime == None):
        nowTime = datetime.now(timezone("PST8PDT"))

    # gives first stream date in the future of the given time
    streamTime = next((t for t in streams if ((t + getTotalStreamLength()) - nowTime).days >= 0), None) 

    if (streamTime == None):
        # Default schedule behavior: Finds the next weekday and schedules it at 8pm or 11am
        streamDate = nowTime.date()
        hour = 20 if nowTime.weekday() < FRIDAY else 11

        if (streamDate.weekday() < SATURDAY 
         and (nowTime.hour > hour+1 
         or (nowTime.hour == hour+1 and nowTime.minute > 30))):

            streamDate += timedelta(days=1) # If we've already had a stream today, the next one will be tomorrow

        while (streamDate.weekday() >= SATURDAY): 
            streamDate += timedelta(days=1)

        hour = 20 if streamDate.weekday() < FRIDAY else 11

        streamTime = datetime.combine(streamDate, time(hour, tzinfo=timezone("PST8PDT")))
        scheduleStream(streamTime)

    return streamTime

def isCurrentlyStreaming(nowTime):
    """Utility function that returns a boolean indicating whether or not the given time falls within
        a livestream.
    """

    streamTime = getNextStream(nowTime)

    sinceStream = nowTime - streamTime;
    sinceHours = int(sinceStream.seconds / 3600)
    sinceMinutes = (sinceStream.seconds - sinceHours * 3600.0) / 60.0

    untilStream = streamTime - nowTime;
    untilHours = int(untilStream.seconds / 3600)
    untilMinutes = (untilStream.seconds - untilHours * 3600.0) / 60.0
    
    return (sinceHours < 1 or (sinceHours < 2 and sinceMinutes < 30) or untilMinutes < 45)

def timeToStream(streamTime, nowTime):
    """Utility function that returns a string specifying one of three things:
        1. The time until the next stream, in (days) hours minutes
        2. The amount of time the stream/Q&A has been going on
        3. The given streamTime occurs before the given nowTime, which is sort of undefined
            behavior.
    """
    ###TODO(chronister): Would it be a better idea to make this function return a more elementary
    ###     type of value (int?) and then build the string elsewhere?
    if (not (streamTime.tzinfo == timezone("PST8PDT"))):
        streamTime = pytz.utc.localize(streamTime)
        streamTime = streamTime.astimezone(timezone("PST8PDT"))
    if (not (nowTime.tzinfo == timezone("PST8PDT"))):
        nowTime = pytz.utc.localize(nowTime)
        nowTime = nowTime.astimezone(timezone("PST8PDT"))

    sinceStream = nowTime - streamTime;
    sinceHours = int(sinceStream.seconds / 3600)
    sinceMinutes = (sinceStream.seconds - sinceHours * 3600.0) / 60.0

    untilStream = streamTime - nowTime;
    untilHours = int(untilStream.seconds / 3600)
    untilMinutes = (untilStream.seconds - untilHours * 3600.0) / 60.0

    if (sinceStream > timedelta(0)):
        if (sinceStream < getStreamLength()):
            timeLeft = getStreamLength() - sinceStream
            return "%s into stream (%s until Q&A) if Casey is on schedule" % (getDurationString(sinceStream), getDurationString(timeLeft))
        elif (sinceStream < getTotalStreamLength()):
            timeLeft = getTotalStreamLength() - sinceStream
            return "%s into the Q&A (%s until end) if Casey is on schedule" % (getDurationString(sinceStream), getDurationString(timeLeft))

    if (nowTime > streamTime + getTotalStreamLength()):
        return "I'm confused and think that the stream is %s in the past!" % (getDurationString(sinceStream))


    return 'Next stream is in %s' % getDurationString(untilStream)



@command('timer', "when", "howlong", "timeleft")
def timer(bot, trigger):
    """Info command that prints out the time until the next stream.
    """
    nowTime = datetime.now(timezone("PST8PDT"))
    streamTime = getNextStream(nowTime) # Make "now" the default argument?

    #TEST CODE
    #stream.scheduleStream(newTime) # sets the time of any existing stream on that day to the new time, or creates one if there is no entry
    #stream.setStreamLength(date, lengthInMinutes) # set the length of the stream (not including Q&A) on that date to the given length

    info(bot, trigger, timeToStream(streamTime, nowTime))