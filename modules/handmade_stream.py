from datetime import datetime, timedelta, date, time
import pytz
from pytz import timezone
import parsedatetime
from willie.tools import stderr
import math

import os, sys
sys.path.append(os.path.dirname(__file__))

from handmade import command, info, whitelisted, adminonly, whitelisted_streamtime, adminonly_streamtime

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

PST = timezone("PST8PDT")
UTC = timezone("UTC")

streams = []
db = None
dateParser = parsedatetime.Calendar()
scheduleTableColumns = [("streamDate", "INTEGER"), ("startTime", "INTEGER"), ("streamLength", "INTEGER"), ("qaLength", "INTEGER")]
scheduleTableRequestColumns = ("streamDate", "startTime", "streamLength", "qaLength")
scheduleTableKey = "streamDate"


class StreamEpisode:
    def __init__(self, streamDate=-1, startTime=-1, streamLength=60, qaLength=30):
        self.streamDate = streamDate
        self.startTime = startTime
        self.streamLength = streamLength
        self.qaLength = qaLength

    def startTZ(self, tz):
        return datetime.utcfromtimestamp(self.startTime).replace(tzinfo=UTC).astimezone(timezone(tz))

    def startDT(self):
        return datetime.utcfromtimestamp(self.startTime).replace(tzinfo=UTC).astimezone(PST)

    def qaDT(self):
        return self.startDT() + timedelta(minutes=self.streamLength)

    def endDT(self):
        return self.startDT() + timedelta(minutes=self.streamLength) + timedelta(minutes=self.qaLength)

    def date(self):
        return self.startDT().date() if self.startTime > 0 else None

    @staticmethod
    def FromDateTime(newTime):
        return StreamEpisode(streamDate=newTime.strftime("%Y%m%d"), startTime=getTimestamp(newTime))

    @staticmethod
    def FromTableColumns(columns):
        return StreamEpisode(streamDate=columns[0], startTime=columns[1], streamLength=columns[2], qaLength=columns[3])

    def __str__(self):
        return "Stream Ep %s at %s which is %d minutes long with %d minute q&a" % (self.streamDate, self.startTime, self.streamLength, self.qaLength)

    def columnDict(self):
        return { "streamDate":str(self.streamDate), "startTime":str(self.startTime), "streamLength":str(self.streamLength), "qaLength":str(self.qaLength) }

    def strftime(self, format):
        return self.startDT().strftime(format)

    def isoformat(self):
        return self.startDT().isoformat()

    def getStreamLength(self):
        return timedelta(minutes=self.streamLength)

    def getTotalStreamLength(self):
        return timedelta(minutes=self.streamLength+self.qaLength)

    def getQaLength(self):
        return timedelta(minutes=self.qaLength)

def setup(bot):
    global streams, db
    db = bot.db

    createScheduleTable()
    streams = getStreams(db)
    #stderr([str(s) for s in streams])

def shutdown(bot):
    stderr("Shutdown ran!")

def getTimestamp(dt, epoch=datetime(1970,1,1,tzinfo=UTC)):
    if (hasattr(dt, "timestamp")):
        return dt.timestamp()

    ##NOTE(chronister): It's not really this function's responsibility to deal with naive datetimes.
    ##  Anything which passes to it should have already taken care of the timezone.
    assert(dt.tzinfo != None)

    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6 


def now():
    return datetime.now(PST)

def createScheduleTable():
    global db
    if (db):

        if (hasattr(db, "schedules") and db.check_table("schedules", scheduleTableColumns, scheduleTableKey)):
            stderr("Schedule table exists.")
        else:
            stderr("Schedule table does not exist. Creating...")
            db.add_table("schedules", scheduleTableColumns, scheduleTableKey)

def updateStreamInTable(stream):
    global db,streams
    stderr("Updating stream on %s to be at %s" % (stream.strftime("%m %d"), stream.startDT().isoformat()))
    db.schedules.update(row=stream.streamDate, key=scheduleTableKey, values=stream.columnDict())
    streams = getStreams(db)


def getStreams(db):
    result = []
    if (hasattr(db, "schedules")):
        keys = db.schedules.keys()
        for key in keys:
            result.append(StreamEpisode.FromTableColumns(db.schedules.get(key=scheduleTableKey, row=str(key[0]), columns=scheduleTableRequestColumns)))
    return result

def colloquialDate(dt):
    today = now().date()
    if (type(dt) is datetime):
        dt = dt.date()
    if (dt == today):
        return "today"
    elif (dt == today + timedelta(days=1)):
        return "tomorrow"
    elif (dt == today - timedelta(days=1)):
        return "yesterday"
    else:
        return dt.strftime("%b %d")

def colloquialDateAndTime(dt, timeFormat="%I %p"):
    cdate = colloquialDate(dt.date())
    return cdate + " at " + dt.strftime(timeFormat).lstrip("0")

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

def scheduleStream(newTime):
    """Sets the time of any existing stream on that day to the new time, or creates one if there is
        no entry.

        newTime is a datetime.
    """

    updateStreamInTable(newTime)

def getNextStream(nowTime=None, scheduleNew=True):
    """Returns the datetime of the start of the next stream from the nowTime given if a stream is 
        not currently on, or the datetime of the start of the current stream if the nowTime is
        during one.
    """
    if (nowTime == None):
        nowTime = now()

    ###REFACTOR(chronister): This is pretty inefficient...
    #todayStream = next((t for t in streams if t.date() == nowTime.date()), None) 
    def countsAsNearFuture(futureTime, nowTime):

        delta = ((futureTime.endDT()) - nowTime)
        
        if (delta.days < 0): return False
        if (delta.days > 3): return False
        if (futureTime.startDT().weekday() <= FRIDAY and delta.days > 0): return False

        return True

    # gives first stream date in the future of the given time
    streamTime = next((t for t in streams if countsAsNearFuture(t, nowTime)), None) 
    isNew = False
    if (scheduleNew and streamTime == None):
        isNew = True
        # Default schedule behavior: Finds the next weekday and schedules it at 8pm or 11am
        streamDate = nowTime.date()

        #Check if there was one today
        today = getNextStream(datetime.combine(streamDate, time(0, tzinfo=PST)), scheduleNew=False)
        if (today == None):
            hour = 20 if nowTime.weekday() < FRIDAY else 11
            today = StreamEpisode.FromDateTime(datetime.combine(streamDate, time(hour=hour, tzinfo=PST)))


        if (streamDate.weekday() < SATURDAY 
         and (nowTime > today.endDT())):
            streamDate += timedelta(days=1) # If we've already had a stream today, the next one will be tomorrow

        while (streamDate.weekday() >= SATURDAY): 
            streamDate += timedelta(days=1)

        hour = 20 if streamDate.weekday() < FRIDAY else 11

        streamTime = StreamEpisode.FromDateTime(datetime.combine(streamDate, time(hour, tzinfo=PST)))
        scheduleStream(streamTime)

    return streamTime

@adminonly
@command("isStreaming", hide=True)
def isStreamingCommand(bot, trigger):
    streaming = isCurrentlyStreaming()
    if (streaming):
        bot.say("Stream is currently going!")
    else:
        bot.say("Stream is not currently going.")

def isCurrentlyStreaming(nowTime=None):
    """Utility function that returns a boolean indicating whether or not the given time falls within
        a livestream.
    """
    if (nowTime == None):
        nowTime = now()
    streamTime = getNextStream(nowTime)

    sinceStream = nowTime - streamTime.startDT();

    untilStream = streamTime.startDT() - nowTime;
    
    return (sinceStream > timedelta(0) and nowTime < streamTime.endDT()) or untilStream < timedelta(minutes=45)

def timeToStream(streamTime, nowTime):
    """Utility function that returns a string specifying one of three things:
        1. The time until the next stream, in (days) hours minutes
        2. The amount of time the stream/Q&A has been going on
        3. The given streamTime occurs before the given nowTime, which is sort of undefined
            behavior.
    """
    ###TODO(chronister): Would it be a better idea to make this function return a more elementary
    ###     type of value (int?) and then build the string elsewhere?

    if (type(nowTime) is datetime and not (nowTime.tzinfo == PST)):
        nowTime = pytz.utc.localize(nowTime)
        nowTime = nowTime.astimezone(PST)

    sinceStream = nowTime - streamTime.startDT();

    untilStream = streamTime.startDT() - nowTime;

    if (sinceStream > timedelta(0)):
        if (sinceStream < streamTime.getStreamLength()):
            timeLeft = streamTime.getStreamLength() - sinceStream
            return "%s into stream (%s until Q&A) if Casey is on schedule" % (getDurationString(sinceStream), getDurationString(timeLeft))
        elif (sinceStream < streamTime.getTotalStreamLength()):
            timeLeft = streamTime.getTotalStreamLength() - sinceStream
            return "%s into the Q&A (%s until end) if Casey is on schedule" % (getDurationString(sinceStream - streamTime.getStreamLength()), getDurationString(timeLeft))

    if (nowTime > streamTime.endDT()):
        return "I'm confused and think that the stream is %s in the past!" % (getDurationString(sinceStream))


    return 'Next stream is in %s' % getDurationString(untilStream)



@command('timer', "when", "howlong", "timeleft")
def timer(bot, trigger):
    """Info command that prints out the time until the next stream.
    """
    nowTime = now()
    streamTime = getNextStream(nowTime) # Make "now" the default argument?

    info(bot, trigger, timeToStream(streamTime, nowTime))


@whitelisted_streamtime
@command('today', 'nextStream')
def nextSchedule(bot, trigger):
    """Info command that prints out the expected time of the next stream
    """
    streamTime = getNextStream(now())
    info(bot, trigger, "The stream should next be live on %s PST" % streamTime.strftime("%a at %I:%M %p"))


@whitelisted_streamtime
@command('thisweek')
def currentSchedule(bot, trigger):
    """Info command that prints out this week's schedule
    """
    nowDate = now().date()
    if (nowDate.weekday() <= FRIDAY):
        while(nowDate.weekday() > MONDAY):
            nowDate = nowDate - timedelta(days=1)
    else: # It's a weekend, go forward to the next week
        while(nowDate.weekday() > MONDAY):
            nowDate = nowDate + timedelta(days=1)

    times = []
    while(nowDate.weekday() <= FRIDAY):
        #check from 12AM for arbitrary reasons
        times.append(getNextStream(datetime.combine(nowDate, time(hour=0, tzinfo=PST))))
        nowDate = nowDate + timedelta(days=1)
    
    info(bot, trigger, "Schedule for week of %s: %s (times in PST)" 
            % (times[0].strftime("%m/%d"), " :: ".join([t.strftime("%I %p on %a").lstrip("0") for t in times])))

@whitelisted_streamtime
@command('schedule')
def seeSchedule(bot, trigger):
    args = trigger.group(2)
    if (args):
        if (trigger.admin):
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
        pTime,flag = dateParser.parseDT(args)
        stderr(pTime)
        if (type(pTime) is datetime or type(pTime) is time):
            pTime = pTime.replace(tzinfo=PST)

        if (flag == 1):
            #parsed as a date, so we can't really do anything with it. Just print the schedule for that day.
            if (type(pTime) is datetime):
                pTime = pTime.date()
            streamTime = getNextStream(datetime.combine(pTime, time(hour=0, tzinfo=PST)))
            stderr(streamTime.isoformat())
            stderr(now().isoformat())
            tense = "should air"
            if (streamTime.endDT() < now()): tense = "should have aired"
            bot.say("@%s: The stream %s %s PST" % (trigger.nick, tense, colloquialDateAndTime(streamTime)))
            return

        if (flag == 2):
            #parsed as a time. Assume if its an admin that they want to change the stream time for today.
            if (trigger.admin): 
                if (type(pTime) is datetime):
                    pTime = pTime.timetz()

                scheduleStream(datetime.combine(date.today(), pTime))
                bot.say("@%s: Set the stream time for today to %s PST" % (trigger.nick, pTime.strftime("%I:%M %p").lstrip("0")))
                return

        if (flag == 3):
            #parsed as a datetime. All is well.
            if (trigger.admin):
                
                scheduleStream(StreamEpisode.FromDateTime(pTime))
                bot.say("@%s: Set the stream time for %s to %s PST" % (trigger.nick, pTime.strftime("%b %d"), pTime.strftime("%I:%M %p")))
                return

        else:
            #Unable to parse. Only respond if its an admin so that non-admins can't spam failed attempts
            if (trigger.admin):
                bot.say("@%s: Sorry, I couldn't figure out what %s meant." % (trigger.nick, args))
                return
    else:
        currentSchedule(bot, trigger)
        return

def getPYTZTimezoneNameFromFriendlyName (friendlyName):
    if (friendlyName == "PST"):
        return "PST8PDT"
    else:
        return friendlyName

@command("tzschedule", "tzs")
def timezoneAwareSchedule(bot, trigger):
    """Info command that prints out this week's schedule, TimeZone aware
    Usage: tzs time-zone-name
    Usage: tzs nick-to-respon-to time-zone-name
    """
    nowDate = now().date()
    if (nowDate.weekday() <= FRIDAY):
        while(nowDate.weekday() > MONDAY):
            nowDate = nowDate - timedelta(days=1)
    else: # It's a weekend, go forward to the next week
        while(nowDate.weekday() > MONDAY):
            nowDate = nowDate + timedelta(days=1)

    times = []
    
    while(nowDate.weekday() <= FRIDAY):
        #check from 12AM for arbitrary reasons
        times.append(getNextStream(datetime.combine(nowDate, time(hour=0, tzinfo=PST))))
        nowDate = nowDate + timedelta(days=1)

    friendlyTzName = "PST" #default timezone name
    respondTo = trigger.nick
    words = trigger.bytes.split()
    nWords = len(words)

    if nWords == 2:
        friendlyTzName = words[1]
    elif nWords == 3:
        respondTo = words[1].lower()
        if respondTo[0] == "@":
            respondTo = respondTo [1:]
        friendlyTzName = words[2]
        if respondTo in ["cmuratori", "handmade_hero"]:
            bot.say("@%s: Please do not direct info at Casey or HandmadeHero." % trigger.nick)
            return

    tzName = getPYTZTimezoneNameFromFriendlyName(friendlyTzName)
    try:
        bot.say("@%s, schedule for week of %s: %s (times in %s)" 
                % (respondTo,
                   times[0].strftime("%m/%d"),
                   ", ".join([t.startTZ(tzName).strftime("%I %p on %a").lstrip("0") for t in times]),
                   friendlyTzName))
    except pytz.exceptions.UnknownTimeZoneError:
        bot.say("@%s, I don't know timezone with name '%s', sorry." % (respondTo, friendlyTzName))
