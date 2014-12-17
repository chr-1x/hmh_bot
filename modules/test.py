import random
from datetime import datetime
from pytz import timezone

def printTitle(title):
    numeq = len(title) + 12
    print("="*numeq)
    print("///   %s   ///" % title)
    print("="*numeq)

# Cases we need to check:
# 1) stream time explicitly scheduled
#   a) before
#   b) during
#   c) after
# 2) stream time rescheduled
# 3) stream time inferred
#   a) before
#   b) during
#   c) after
#   d) weekend
def testStreamScheduler():
    import stream
    printTitle("Stream Scheduling Test Cases")

    def t(year, month, day, hour, minute=0, second=0):
        return datetime(year, month, day, hour, minute, second, 0, timezone("PST8PDT"))

    streamTimes = [ t(2014, 12, 1, 19), t(2014, 12, 2, 21), t(2014, 12, 2, 14)]
    for times in streamTimes:
        stream.scheduleStream(times)

    nowTimes = [ t(2014, 12, 1, 12), t(2014, 12, 1, 19, 30), t(2014, 12, 1, 22), t(2014, 12, 2, 11), t(2014, 12, 6, 14) ]
    for t in nowTimes:
        print("Next stream after %s is %s" % (t.isoformat(), stream.getNextStream(t).isoformat()))

    print("\n")


# Cases we need to check:
# 1) stream time greater than now time
# 2) stream time less than now time
# 3) stream time where now time is during stream
# 4) stream time where now time is during Q&A
# 5) stream time is in different year
# 6) timezones don't match
def testStreamTimeCalculator():
    import stream
    printTitle("Stream Timer Test Cases")

    def t(year, month, day, hour, minute=0, second=0):
        return datetime(year, month, day, hour, minute, second, 0, timezone("PST8PDT"))
    def tUtc(year, month, day, hour, minute=0, second=0):
        return datetime(year, month, day, hour, minute, second, 0)

    streamTimes = [ t(2014, 12, 1, 20    ), t(2014, 12, 1, 20), t(2014, 12, 1, 20    ), t(2014, 12, 1, 20    ), t(2015, 1, 1, 11, 36), tUtc(2014, 12, 2, 4) ]
    nowTimes =    [ t(2014, 12, 1, 15, 41), t(2014, 12, 2, 15), t(2014, 12, 1, 20, 35), t(2014, 12, 1, 21, 15), t(2014, 12, 29, 21), t(2014, 12, 2, 4, 2) ]

    for i in range(len(streamTimes)):
        print(stream.timeToStream(streamTimes[i], nowTimes[i]))

    print("\n")


testStreamTimeCalculator()
testStreamScheduler()