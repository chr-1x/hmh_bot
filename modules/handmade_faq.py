import willie
import willie.module
import random
from willie.modules.search import google_search
from datetime import datetime, timedelta
import pytz
from pytz import timezone
from willie.modules.search import google_search

import os, sys
sys.path.append(os.path.dirname(__file__))

from handmade import Cmd, command, info
import handmade_stream as stream

#TODO(chronister): engine FAQ

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
    if stream.isCurrentlyStreaming(datetime.now(timezone("PST8PDT"))) and not trigger.admin: return
    if not trigger.group(2):
        bot.say("@%s: http://msdn.microsoft.com/" % trigger.nick)
    else:
        query = trigger.group(2).strip()
        bot.say("@%s: %s" % (trigger.nick, google(query)))

@command('time', 'now', 'pst', 'PST')
def getTime(bot, trigger):
    """Info command that prints out the current time in PST. For the purposes of the handmade hero
        stream, we don't really care about other time zones.
    """
    now = datetime.now(timezone("PST8PDT"))
    info(bot, trigger, "The current time in Seattle is %s PST" % (now.strftime("%I:%M %p")))

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

@command('hello', 'hi')
def helloMessage(bot, trigger):
    """Command that shows hello,world style information. 
        Possible addition: name-based trigger? e.g. "Chronalrobot: hi" or "hi Chronalrobot"
    """
    bot.say("Hello, I am an IRC bot! Try some commands: !help, !list, !when, !what")

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

@command('q&a, qa')
def qaInfo(bot, trigger):
    bot.say("Q&A session. Please prefix questions w/ @cmuratori. The shorter the question, and if related to the stream, the higher the chances of getting it answered.")

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
    info(bot, trigger, "It is estimated that the project will take 2 years to finish at the rate of one 1-hour stream per weeknight.")


@command('thankCasey', hide=True)
def thanksMessage(bot, trigger):
    """Command that thanks Casey for streaming. Could be automated, somehow?
    """
    bot.say("Thanks for streaming, Casey! <3")

@command('thanks', hide=True)
def thanksMessage(bot, trigger):
    """Command to thank a user.
    """
    if (trigger and trigger.group(2)):
        info(bot, trigger, "Your thanking has been noted.")
    else:
        info(bot, trigger, "You're welcome <3")