import willie
import willie.module
import random
from datetime import datetime, timedelta
import time
import pytz
from pytz import timezone
from willie.modules.search import google_search

#TODO(chronister): engine FAQ

##TODO(chronister): Move out into stream module

def getStreamTime(nowTime):
    """Temporary function for getting the next stream from the given time. Will soon be superceded 
        by a more thorough system!
    """
    streamTime = nowTime
    while(not(streamTime.minute == 0 and 
        (streamTime.weekday() == 4 and streamTime.hour == 11) or
        (streamTime.weekday() < 4 and streamTime.hour == 20 ))):

        streamTime = streamTime + timedelta(minutes=1) #inc minutes

    return streamTime

def isCurrentlyStreaming(nowTime):
    streamTime = getStreamTime(nowTime)

    sinceStream = nowTime - streamTime;
    sinceHours = int(sinceStream.seconds / 3600)
    sinceMinutes = (sinceStream.seconds - sinceHours * 3600.0) / 60.0

    untilStream = streamTime - nowTime;
    untilHours = int(untilStream.seconds / 3600)
    untilMinutes = (untilStream.seconds - untilHours * 3600.0) / 60.0
    
    return (sinceHours < 1 or (sinceHours < 2 and sinceMinutes < 30) or untilMinutes < 45)

class Cmd:
    """ Wrapper class that stores the list of commands, main command name (assumed to be first in 
        list), and function to call for the command.
    """
    def __init__(self, cmds, func, hide=False):
        self.main = cmds[0]
        self.cmds = cmds
        self.func = func
        self.hide = hide

    def randCmd(self):
        return random.choice(self.cmds)

    def __str__(self):
        return self.main

commands = []

def command(*args, **kwargs):
    """Decorator that just passes it on to the built-in willie command decorator, but also adds it 
        to the module's command list (for !list function, etc)
    """
    def passthrough(func):
        commands.append(Cmd(args,func,kwargs.get("hide")))
        return willie.module.commands(*args)(func)

    return passthrough

###TODO(chronister): Whitelisted commands that only work if the caller is admin.
###    Ideally, this should just be an alternate decorator you can call.
#def whitelistedcommand(*args, **kwargs):

    #result = command(args, kwargs)


def whitelistedfunc(func):
    """When passed a function, returns a new function that will conditionally call the original 
        depending on whether or not the user is on the whitelist (Note: only admins are whitelisted 
        right now, do we want a separate admin list and white list?)
    """
    def wrapperFunc(trigger, bot):
        if (trigger.admin or trigger.owner):
            func(trigger, bot)
        else:
            pass #Don't say anything back to the user, to avoid spam.
    return wrapperFunc        

def info(bot, trigger, text):
    """Handles directed informational text -- will either direct the text to @caller or to @nick 
        specified in the first argument. Commands which use this method should put "Info Command"
        in their docstring (and maybe in something user-facing...!infocommands?)
    """
    ###TODO(chronister): Can this be done as a decorator? (would have to give a custom bot 
    ###     or something?)
    streaming = isCurrentlyStreaming(datetime.now(timezone("PST8PDT")))
    if ((streaming and trigger and trigger.admin) or not streaming):
        if (trigger):
            if (trigger.group(2)):

                args = trigger.group(2).split(" ")
                if (args[0][0] == "@"): 
                    args[0] = args[0][1:]

                if (args[0].lower() != "cmuratori"):
                    bot.say("@%s: %s" % (args[0], text))
                else:
                    bot.say("@%s: Please do not direct info at Casey." % trigger.nick)
            else:
                bot.say("@%s: %s" % (trigger.nick, text))
        else:
            bot.say(text)
    else:
        #temporary measure: whitelist to admins
            pass

    

@willie.module.commands('amIadmin', 'isAdmin', 'isWhitelisted', 'whitelisted')
def isAdmin(bot, trigger):
    """Simple command that simply tells the user whether or not they are an admin. Mostly 
        implemented for debugging (double-checking case sensitivity and things)
    """
    if (trigger):
        args = trigger.group(2).split(" ")
        if (args):
            admins = bot.config.core.admins
            for arg in args:
                if (admins and arg in admins):
                    bot.say("%s is an admin!" % arg)
                else:
                    bot.say("%s is not an admin." % arg)
        elif (trigger.admin or trigger.owner):
            bot.say("%s, you are an admin!" % trigger.nick)
        else:
            bot.say("%s, you are not an admin." % trigger.nick)


sites_query = ' site:msdn.microsoft.com' # -site:' + ' -site:'.join(ignored_sites)
def google(query):
    """Wraps the google search performed by the msdn command (borrowed from the xkcd command).
        Note: might not be necessary, unless other commands start using google as well. Consider
        merging into msdnSearch.
    """
    url = google_search(query + sites_query)
    return url

@command('msdn')
def msdnSearch(bot, trigger):
    """Command that searchs msdn for the string provided in the command arguments. Performs this
        with the Google API and site:msdn.microsoft.com
    """
    ###TODO(chronister): Add hidden C++ keyword to search?
    ###TODO(chronister): Are there any subdomains we don't want? See commented -site above
    if not trigger: return
    if isCurrentlyStreaming(datetime.now(timezone("PST8PDT"))) and not trigger.admin: return
    if not trigger.group(2):
        bot.say("@%s: http://msdn.microsoft.com/" % trigger.nick)
    else:
        query = trigger.group(2).strip()
        bot.say("@%s: %s" % (trigger.nick, google(query)))

@command('time', 'now', 'pst', 'PST')
def time(bot, trigger):
    """Info command that prints out the current time in PST. For the purposes of the handmade hero
        stream, we don't really care about other time zones.
    """
    now = datetime.now(timezone("PST8PDT"))
    info(bot, trigger, "The current time in Seattle is %s PST" % (now.strftime("%I:%M %p")))

@command('timer', "when", "howlong", "timeleft")
def timer(bot, trigger):
    """Info command that prints out the time until the next stream.
    """

    nowTime = datetime.now(timezone("PST8PDT"))
    ###TODO(chronister): Need a way better stream scheduling system! 
    ###     Needs to have the following abilities:
    ###      1. Quickly and easily (read: no git push necessary) add rescheduled stream times
    ###      2. Utility function to determine how far into a stream the current time is (or how
    ###         long until the next stream --- basically something for this command to wrap)
    ###TODO(chronister): This method ends up returning "now" if the stream is currently on! ack!
    streamTime = getStreamTime(nowTime)

    info(bot, trigger, timeToStream(streamTime, nowTime))


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

    mydays = ''
    myhours = ''
    myminutes = ''

    if untilStream.days == 1:
        mydays = 'day'
    else:
        mydays = 'days'
    
    if untilHours == 1:
        myhours = 'hour'
    else:
        myhours = 'hours'

    if untilMinutes == 1:
        myminutes = 'minute'
    else:
        myminutes = 'minutes'

    if untilStream.days != 0:
        # look at format here after substitution is working
        return 'Next stream is in %d %s, %d %s, %d %s' % (untilStream.days, mydays, untilHours, myhours, untilMinutes, myminutes)
    elif untilStream.days == 0:
        return 'Next stream is in %d %s, %d %s' % (untilHours, myhours, untilMinutes, myminutes)

@command('site')
def siteInfo(bot, trigger):
    """Info command that prints out the site/forum links.
    """
    info(bot, trigger, 'HH Website: http://handmadehero.org/  ::  HH Forums: http://forums.handmadehero.org/')

@command('old', 'archive')
def archiveInfo(bot, trigger):
    """Info command that prints out the forum/youtube archive links.
    """
    info(bot, trigger, 'Forum Archive: https://forums.handmadehero.org/jace/   ::   YT Archive: https://www.youtube.com/user/handmadeheroarchive')

@command('wrist', 'wrists', 'braces')
def wristInfo(bot, trigger):
    """Info command that prints out info about Casey's wrist braces
    """
    info(bot, trigger, "The wrist braces Casey wears help make typing more comfortable and prevent Repetitive Strain Injury. They probably aren't made anymore, but they're the Medi-Active ones without the thumb brace.")

@command('milk', 'almondmilk')
def milkInfo(bot, trigger):
    """Info command that prints out info about almond milk.
    """
    info(bot, trigger, "One of Casey's drinks of choice is Almond Milk, a delicious and refreshing beverage. Some common brands are Silk and Almond Breeze.")

@command('who', 'casey')
def caseyInfo(bot, trigger):
    """Info command that prints out info about Casey. Could be refactored into multiple commands
        for better clarity.
    """
    info(bot, trigger, "Casey Muratori is a software engineer who lives in Seattle. He has done work for various companies such as RAD game tools and on games such as The Witness, and has also done fiction writing and podcasting. He started Handmade Hero to give the general public a better idea of what coding a game from scratch in C is like based on his experiences in the industry.")

@command('thanks')
def thanksMessage(bot, trigger):
    """Command that thanks Casey for streaming. Could be automated, somehow?
    """
    bot.say("Thanks for streaming, Casey! <3")

@command('hello', 'hi')
def helloMessage(bot, trigger):
    """Command that shows hello,world style information. 
        Possible addition: name-based trigger? e.g. "Chronalrobot: hi" or "hi Chronalrobot"
    """
    bot.say("Hello, I am an IRC bot! Try some commands: !when, !now, !site, !game, !info")

@command('botinfo')
def infoMessage(bot, trigger):
    """Command that shows information about the chatbot. Should be updated with contributor info
        and github page once that happens.
    """
    bot.say("I am a Python IRC bot based on Willie (http://willie.dftba.net/). I am run by ChronalDragon, who can be contacted via https://tinyurl.com/ChronalDragon")

@command('buy', 'purchase', 'support')
def buyInfo(bot, trigger):
    """Info command that prints out where you can buy the game/support the project.
    """
    info(bot, trigger, "Handmade Hero, the compiled game with art assets and full source code, can be purchased at http://handmadehero.org/#buy_now You can now also support Casey monthly at http://www.patreon.com/cmuratori")

@command('game', 'what')
def gameInfo(bot, trigger):
    """Info command that displays basic information about the game being built.
    """
    info(bot, trigger, "Handmade Hero is a project to build an entire game in C from scratch, no libraries. "
        "We don't know what kind of game it will be yet, but we know it will be 2D, cross-platform, and feature art by Yangtian Li "
        "as well as specially licensed music. For more information, visit http://handmadehero.org/")

@command('friday')
def fridays(bot, trigger):
    """Until we have a set schedule and while Casey keeps up doing early Fridays"""
    info(bot, trigger, "Handmade Hero typically happens on Fridays at 11 AM PST. This is not necessarily the definitive schedule, for the time being. " 
        "The replays are on Youtube and Twitch if you missed them.")

@command('stream', 'about', 'info')
def streamInfo(bot, trigger):
    """Info command that displays basic information about the stream itself.
    """
    info(bot, trigger, "In this stream, game programmer Casey Muratori is walking us through the creation of a game from scratch in C. The game is being developed for educational purposes: he will explain what he is doing every step of the way. For more information, visit http://handmadehero.org/")

### NOTE:
# These functions are easter eggy, probably not good to keep on all the time. 

@command('beep', 'boop', hide=True)
def beepBoop(bot, trigger):
    """Easter egg command that prints out some programming/robot joke type responses
    """
    responses = [
    "Don't speak of my mother that way!",
    "That command was deprecated as of version 1.6.7, please use 1.3.1 for more a more updated API",
    ":)",
    "Pushing random buttons isn't meaningful communication, you know!",
    "What goes around, comes around",
    "Do it again. I dare you.",
    "What good is an IRC bot without easter egg commands?"
    ]
    bot.say(random.choice(responses))

@command('flame', hide=True)
def flameWar(bot, trigger):
    """Easter egg command that randomly chooses whether to insult a language or endorse an
       editor.
    """
    if (random.random() < 0.5):
        badLanguage(bot, trigger)
    else:
        bestEditor(bot, trigger)

@command('throwdown', 'badlanguage', hide=True)
def badLanguage(bot, trigger):
    """Easter egg command that insults a random language from this list. Feel free to add lots
       more languages >:) (Possibly including C???)
    """
    langs = [ "Ruby", "Python", "C++", "PHP", "Rust", "Go", "Perl", "C#", "Java", "Scala", "Objective-C", "F#",
    "Haskell", "Clojure", "BASIC", "Visual Basic", "HTML", "CSS", "Javascript", "Actionscript", "D" ]
    info(bot, None, "%s is a bad language :)" % random.choice(langs))

@command('holywar', 'besteditor', hide=True)
def bestEditor(bot, trigger):
    """Easter egg command that endorses either emacs or vim. Feel free to add more editors.
    """
    editors = ["emacs", "vim"]
    info(bot, None, "%s is the best editor :)" % random.choice(editors))

@command('hug')
def hug(bot, trigger):
    """Easter egg info command that attempts to provide human warmth and empathy in times of 
        emotional trauma.
    """
    info(bot, trigger, "Were I not a transient being circling through an ether of intangible bits and bytes, I would hug you, with all the human emotional context it implies")

@command('why')
def whyInfo(bot, trigger):
    """Easter egg command that answers one of the remaining basic questions. Could possibly be made
        more descriptive and/or actually useful
    """
    bot.say("Because he can.")

@command('random')
def randomNumber(bot, trigger):
    """Easter egg info command that returns a randomly-selected number.
    """
    info(bot, trigger, "Your random number is %s" % (random.randint(100) if random.random() < 0.0001 else 4))

# End easter egg commands (Should these be in a different file?)

@command('lang', 'language', 'codedin')
def langInfo(bot, trigger):
    """Info command that provides a description of the language and style used on the stream.
        Could be split into two commands, one for simple info and one about the structural choices.
    """
    info(bot, trigger, "The language we are using in Handmade Hero is C++ coded in a C-like style. We will most likely not be using classes, inheritance, or polymorphism to any significant degree.")

@command('ide', 'emacs', 'editor')
def ideInfo(bot, trigger):
    """Info command that provides information about the editor (emacs) used by Casey. 
    """
    ###TODO(chronister): Get emacs version info, it's a common question
    info(bot, trigger, "Casey uses emacs to edit his code, because that is what he is used to. It is getting pretty old, so you should use whatever you feel most comfortable in.")

@command('college', 'school')
def collegeInfo(bot, trigger):
    info(bot, trigger, "Casey did not go to college, he has been coding in the gaming industry since 1995. You can read his biography here: http://mollyrocket.com/casey/about.html")

@command('keyboard', 'kb')
def keyboardInfo(bot, trigger):
    """Info command that provides information about what keyboard Casey uses.
    """
    info(bot, trigger, "The mechanical keyboard Casey uses is a Das Keyboard 4.")

@command('length', 'years', 'total')
def timeOfProject(bot, trigger):
    """How long is the project going on?"""
    info(bot, trigger, "The project does not have an exact finish date. This is an ongoing project, although it is estimated to take longer than a year at a rate of one hour per night, 5 days a week.")


@command('alias', 'alt')
def aliasList(bot, trigger):
    """Command that provides a list of registered aliases for the given command. Must be registered
        in the same decorator, commands that simply call the same function aren't grouped.
        Note that you must use the custom-defined @command decorator instead of the built-in
        Willie module one for this to work.
    """
    args = trigger.group(2).split(" ") if trigger and trigger.group(2) else None
    if (args and len(args) > 0):
        for arg in args:
            cmd = next((c for c in commands if arg in c.cmds), None)
            if (cmd):
                bot.say("Aliases of !%s: !%s" % (arg, ", !".join(cmd.cmds)))
                if (len(args) > 1): 
                    time.sleep(0.300)
            else:
                bot.say("No aliases found for %s!" % arg)

    else:
        bot.say("Please specify a command to list the aliases of.")

@command('list', 'commands', 'cmds', hide=True)
def commandList(bot, trigger): 
    """Command that lists all of the (non-hidden) registered commands. 
        Note that you must use the custom-defined @command decorator for commands to appear here, 
        not the built-in Willie module one.
    """
    bot.say("Here are all of the HH stream commands: !%s" % ", !".join([c.main for c in commands if not(c.hide==True)]))


