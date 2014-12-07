import willie
import random
from datetime import datetime, timedelta
import pytz
from pytz import timezone
from time import sleep

class Cmd:
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

    def passthrough(func):
        commands.append(Cmd(args,func,kwargs.get("hide")))
        return willie.module.commands(*args)(func)

    return passthrough

def info(bot, trigger, text):
    if (trigger):
        if (trigger.group(2)):
            args = trigger.group(2).split(" ")
            bot.say("@%s: %s" % (args[0], text))
        else:
            bot.say("@%s: %s" % (trigger.nick, text))
    else:
        bot.say(text)

@command('isAdmin')
def isAdmin(bot, trigger):
    if (trigger):
        if (trigger.admin or trigger.owner):
            bot.say("%s, you are an admin!" % trigger.nick)
        else:
            bot.say("%s, you are not an admin." % trigger.nick)

@command('time', 'now', 'pst', 'PST')
def time(bot, trigger):
    now = datetime.now(timezone("PST8PDT"))
    info(bot, trigger, "The current time in Seattle is %s:%s %s PST" % (now.strftime("%I"), now.strftime("%M"), "PM" if now.hour > 11 else "AM"))

@command('timer', "when", "howlong", "timeleft")
def timer(bot, trigger):

    streamTime = datetime.now(timezone("PST8PDT"))
    nowTime = datetime.now(timezone("PST8PDT"))
    while(not(streamTime.minute == 0 and 
        (streamTime.weekday() == 4 and streamTime.hour == 11) or
        (streamTime.weekday() < 4 and streamTime.hour == 20 ))):

        streamTime = streamTime + timedelta(minutes=1) #inc minutes

    info(bot, trigger, timeToStream(streamTime, nowTime))

def timeToStream(streamTime, nowTime):
    
    if (not (streamTime.tzinfo == timezone("PST8PDT"))):
        streamTime = pytz.utc.localize(streamTime)
        streamTime = streamTime.astimezone(timezone("PST8PDT"))
    if (not (nowTime.tzinfo == timezone("PST8PDT"))):
        nowTime = pytz.utc.localize(nowTime)
        nowTime = nowTime.astimezone(timezone("PST8PDT"))

    sinceStream = nowTime - streamTime;
    sinceHours = int(sinceStream.seconds / 3600)
    sinceMinutes = (sinceStream.seconds - sinceHours * 3600) / 60  

    untilStream = streamTime - nowTime;
    untilHours = int(untilStream.seconds / 3600)
    untilMinutes = (untilStream.seconds - untilHours * 3600) / 60

    if (sinceHours < 1):
        return "%d minutes into stream (if Casey is on schedule)" % sinceMinutes
    elif (sinceHours < 2 and sinceMinutes < 30):
        return "%d minutes into the Q&A (if Casey is on schedule)" % sinceMinutes

    if (nowTime > streamTime + timedelta(hours=1, minutes=30)):
        return "I'm confused and think that the stream is %d hours %d minutes in the past!" % (abs(untilStream.days * 24 + untilHours), untilMinutes)

    if (untilStream.days != 0):
        return 'Next stream is in %d days, %d hours %d minutes' % (untilStream.days, untilHours, untilMinutes)
    else:
        return 'Next stream is in %d hours %d minutes' % (untilHours, untilMinutes)


@command('site')
def siteInfo(bot, trigger):
    info(bot, trigger, 'HH Website: http://handmadehero.org/  ::  HH Forums: http://forums.handmadehero.org/')

@command('old', 'archive')
def archiveInfo(bot, trigger):
    info(bot, trigger, 'YT Archive: https://www.youtube.com/user/handmadeheroarchive')

@command('wrist', 'braces')
def wristInfo(bot, trigger):
    info(bot, trigger, 'The wrist braces Casey wears help make typing more comfortable and prevent Repetitive Strain Injury.')

@command('milk', 'almondmilk')
def milkInfo(bot, trigger):
    info(bot, trigger, "One of Casey's drinks of choice is Almond Milk, a delicious and refreshing beverage. Some common brands are Silk and Almond Breeze.")

@command('who', 'casey')
def caseyInfo(bot, trigger):
    info(bot, trigger, "Casey Muratori is a software engineer who lives in Seattle. He has done work for various companies such as RAD game tools and on games such as The Witness, and has also done fiction writing and podcasting. He started Handmade Hero to give the general public a better idea of what coding a game from scratch in C is like based on his experiences in the industry.")

@command('thanks')
def thanksMessage(bot, trigger):
    bot.say("Thanks for streaming, Casey! <3")

@command('hello', 'hi')
def helloMessage(bot, trigger):
    bot.say("Hello, I am an IRC bot! Try some commands: !when, !now, !site, !game, !info")

@command('info')
def infoMessage(bot, trigger):
    bot.say("I am a Python IRC bot based on Willie (http://willie.dftba.net/). I am run by ChronalDragon, who can be contacted via https://tinyurl.com/ChronalDragon")

@command('buy', 'purchase')
def buyInfo(bot, trigger):
    info(bot, trigger, "Handmade Hero, the compiled game with art assets and full source code, can be purchased at http://handmadehero.org/#buy_now")

@command('game', 'what')
def gameInfo(bot, trigger):
    info(bot, trigger, "Handmade Hero is a project to build an entire game in C from scratch, no libraries. We don't know what kind of game it will be yet, but we know it will be 2D, cross-platform, and feature art by Yangtian Li as well as specially licensed music. For more information, visit http://handmadehero.org/")

@command('beep', 'boop', hide=True)
def beepBoop(bot, trigger):
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
    if (random.random() < 0.5):
        badLanguage(bot, trigger)
    else:
        bestEditor(bot, trigger)

@command('throwdown', 'badlanguage', hide=True)
def badLanguage(bot, trigger):
    langs = [ "Ruby", "Python", "C++", "PHP", "Rust", "Go", "Perl", "C#", "Java", "Scala", "Objective-C", "F#",
    "Haskell", "Clojure", "BASIC", "Visual Basic", "HTML", "CSS", "Javascript", "Actionscript", "D" ]
    bot.say("%s is a bad language :)" % random.choice(langs))

@command('holywar', 'besteditor', hide=True)
def bestEditor(bot, trigger):
    editors = ["emacs", "vim"]
    bot.say("%s is the best editor :)" % random.choice(editors))

@command('why')
def whyInfo(bot, trigger):
    bot.say("Because he can.")

@command('random')
def randomNumber(bot, trigger):
    info(bot, trigger, "Your random number is %s" % 4)

@command('lang', 'language', 'codedin')
def langInfo(bot, trigger):
    info(bot, trigger, "The language we are using in Handmade Hero is C++ coded in a C-like style. We will most likely not be using classes, inheritance, or polymorphism to any significant degree.")

@command('ide', 'emacs', 'editor')
def ideInfo(bot, trigger):
    info(bot, trigger, "Casey uses emacs to edit his code, because that is what he is used to. It is getting pretty old, so you should use whatever you feel most comfortable in.")

@command('keyboard', 'kb')
def keyboardInfo(bot, trigger):
    info(bot, trigger, "The mechanical keyboard Casey uses is a Das Keyboard 4.")

@command('alias', 'alt')
def aliasList(bot, trigger):
    args = trigger.group(2).split(" ") if trigger else None
    if (args and len(args) > 0):
        for arg in args:
            cmd = next((c for c in commands if arg in c.cmds), None)
            if (cmd):
                bot.say("Aliases of !%s: !%s" % (arg, ", !".join(cmd.cmds)))
                if (len(args) > 1): 
                    sleep(0.300)
            else:
                bot.say("No aliases found for %s!" % arg)

    else:
        bot.say("Please specify a command to list the aliases of.")

@command('list', 'commands', 'cmds', hide=True)
def commandList(bot, trigger): 
    bot.say("Here are all of the HH stream commands: !%s" % ", !".join([c.main for c in commands if not(c.hide==True)]))