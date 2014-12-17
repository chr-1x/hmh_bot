from datetime import datetime, timedelta
import time
import pytz
from pytz import timezone


streams = []

def getNextStream(nowTime):
	"""Returns the datetime of the start of the next stream from the nowTime given if a stream is 
		not currently on, or the datetime of the start of the current stream if the nowTime is
		during one.
	"""
	if (nowTime == None):
		nowTime = datetime.now(timezone("PST8PDT"))

	# gives first stream date in the future of the given time
	streamTime = next((t for t in streams if (t - nowTime).days > 0), None) 

	if (streamTime == None):
		


def scheduleStream(newTime):
	"""Sets the time of any existing stream on that day to the new time, or creates one if there is no entry.

		newTime is a datetime.
	"""








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

    if (sinceHours < 1):
        return "Currently streaming (if Casey is on schedule)" #% sinceMinutes #%d minutes into stream
    elif (sinceHours < 2 and sinceMinutes < 30):
        return "Currently doing Q&A (if Casey is on schedule)" #% sinceMinutes #%d minutes into the Q&A

    if (nowTime > streamTime + timedelta(hours=1, minutes=30)):
        return "I'm confused and think that the stream is %d hours %d minutes in the past!" % (abs(untilStream.days * 24 + untilHours), untilMinutes)

    if (untilStream.days != 0):
        return 'Next stream is in %d days, %d hours %d minutes' % (untilStream.days, untilHours, untilMinutes)
    else:
        return 'Next stream is in %d hours %d minutes' % (untilHours, untilMinutes)