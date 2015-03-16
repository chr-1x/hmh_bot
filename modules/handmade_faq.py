import willie
import willie.module
import random
from willie.modules.search import google_search
import arrow

import os, sys
sys.path.append(os.path.dirname(__file__))

from handmade import Cmd, command, info, whitelisted, adminonly, whitelisted_streamtime, adminonly_streamtime
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

@whitelisted_streamtime
@command('msdn', hide=True)
def msdnSearch(bot, trigger):
    """Command that searches msdn for the string provided in the command arguments. Performs this
        with the Google API and site:msdn.microsoft.com
    """
    ###TODO(chronister): Add hidden C++ keyword to search?
    ###TODO(chronister): Are there any subdomains we don't want? See commented -site above
    if not trigger: return
    if stream.isCurrentlyStreaming() and not trigger.admin: return
    if not trigger.group(2):
        bot.say("@%s: http://msdn.microsoft.com/" % trigger.nick)
    else:
        query = trigger.group(2).strip()
        bot.say("@%s: %s" % (trigger.nick, google(query)))

@command('now', 'pst', 'PST')
def getTime(bot, trigger):
    """Info command that prints out the current time in PST. For the purposes of the handmade hero
        stream, we don't really care about other time zones.
    """
    now = arrow.now('US/Pacific')
    info(bot, trigger, "The current time in Seattle is %s" % (now.strftime("%I:%M %p %Z")))

@command('site')
def siteInfo(bot, trigger):
    """Info command that prints out the site/forum links.
    """
    info(bot, trigger, 'HH Website: http://goo.gl/fmjocD  ::  HH Forums: http://goo.gl/NuArvD')

@command('old', 'archive')
def archiveInfo(bot, trigger):
    """Info command that prints out the forum/youtube archive links.
    """
    info(bot, trigger, 'Forum Archive: http://goo.gl/8ouung   ::   YT Archive: http://goo.gl/u3hKKj')

@command('wrist', 'wrists', 'braces', 'hands')
def wristInfo(bot, trigger):
    """Info command that prints out info about Casey's wrist braces
    """
    info(bot, trigger, "The wrist braces Casey wears help make typing more comfortable and prevent Repetitive Strain Injury. They were made by Medi-Active (the ones without the thumb brace) but are no longer in production.")

@command('milk', 'almondmilk', 'drink')
def milkInfo(bot, trigger):
    """Info command that prints out info about almond milk.
    """
    info(bot, trigger, "One of Casey's drinks of choice is Almond Milk, a delicious and refreshing beverage. Some common brands are Silk and Almond Breeze.")

@command('who', 'casey')
def caseyInfo(bot, trigger):
    """Info command that prints out info about Casey. Could be refactored into multiple commands
        for better clarity.
    """
    info(bot, trigger, "Casey Muratori is 38 and a software engineer who lives in Seattle. He started Handmade Hero to give the general public a better idea of what coding a game from scratch in C is like based on his experiences in the industry. For a full bio, see http://mollyrocket.com/casey/about.html")

@command('hello', 'hi', hide=True)
def helloMessage(bot, trigger):
    """Command that shows hello,world style information.
        Possible addition: name-based trigger? e.g. "Chronalrobot: hi" or "hi Chronalrobot"
    """
    bot.say("Hello, I am an IRC bot! Try some commands: !help, !list, !when, !what")

@whitelisted_streamtime
@command('botinfo', hide=True)
def infoMessage(bot, trigger):
    """Command that shows information about the chatbot. Should be updated with contributor info
        and github page once that happens.
    """
    bot.say("I am a Python IRC bot based on Willie (http://willie.dftba.net/). I was started by ChronalDragon and am now jointly maintained by the good folks who commit to my github repo (https://github.com/Chronister/ChronalRobot)")

@whitelisted_streamtime
@command('credits', hide=True)
def creditsMessage(bot, trigger):
    """Shows contributor info! If you make changes, add yourself here (or get someone else to)
    """
    bot.say("Thanks to chronaldragon (chronister), alexwidener (iamdefinitelybatman), dspecht (drive137) and itsuart (isuart2) for their contributions to my code.")

@command('buy', 'purchase', 'support', 'patreon')
def buyInfo(bot, trigger):
    """Info command that prints out where you can buy the game/support the project.
    """
    info(bot, trigger, "The Handmade Hero art assets and full source code, can be purchased at http://goo.gl/y20Q9C . You can also support Casey monthly at http://www.patreon.com/cmuratori")


@command('game', 'gameinfo')
def gameInfo(bot, trigger):
    """Info command that displays basic information about the game being built.
    """
    info(bot, trigger, "Handmade hero will be a 2D, top-down game inspired by classic Zelda games and modern games like the Binding of Isaac. The entire development of the game will be catalogued in these streams. (More: !art, !lang)")

@command('friday', hide=True)
def fridays(bot, trigger):
    """Until we have a set schedule and while Casey keeps up doing early Fridays"""
    info(bot, trigger, "Handmade Hero typically happens on Fridays at 11 AM PST. This is not necessarily the definitive schedule, for the time being. "
        "The replays are on Youtube and Twitch if you missed them.")

@command('stream', 'about', 'info', 'what')
def streamInfo(bot, trigger):
    """Info command that displays basic information about the stream itself.
    """
    info(bot, trigger, "In this stream, game programmer Casey Muratori is walking us through the creation of a game from scratch in C. The game is being developed for educational purposes: he will explain what he is doing every step of the way. For more information, visit http://goo.gl/fmjocD")

@command('lang', 'language', 'codedin')
def langInfo(bot, trigger):
    """Info command that provides a description of the language and style used on the stream.
        Could be split into two commands, one for simple info and one about the structural choices.
    """
    info(bot, trigger, "The language used in the stream is essentially C (with a few C++ features like operator overloading and function overloading anticipated). Since we're writing everything from scratch, we will not be using the C standard library wherever possible.")

@command('ide', 'emacs', 'editor')
def ideInfo(bot, trigger):
    """Info command that provides information about the editor (emacs) used by Casey.
    """
    info(bot, trigger, "Casey uses Emacs to edit his code, because that is what he is used to. There are a lot of editors out there, however, so you should use whatever you feel most comfortable in. The version he uses is GNU Emacs 23.4.1 (i386-mingw-nt6.1.7601), released in 2012.")

@command('college', 'school')
def collegeInfo(bot, trigger):
    info(bot, trigger, "Casey did not go to college; he has been coding in the gaming industry since 1995. You can read his biography here: http://mollyrocket.com/casey/about.html")

@command('keyboard', 'kb')
def keyboardInfo(bot, trigger):
    """Info command that provides information about what keyboard Casey uses.
    """
    info(bot, trigger, "The mechanical keyboard Casey uses is a Das Keyboard 4.")

@command('totalTime','length', 'years', 'total')
def timeOfProject(bot, trigger):
    """How long is the project going on?"""
    info(bot, trigger, "It is estimated that the project will take 2 years to finish at the rate of one 1-hour stream per weeknight.")

@command('art', 'artist')
def artCreatorInfo(bot, trigger):
    """Command to state who the art is done by
        TODO: maybe look to casey to get a link the artists profile for viewing
    """
    info(bot, trigger, "The art in Handmade Hero will be created by Yangtian Li (http://www.yangtianli.com/), an artist Casey knows whom he contracted using the funds provided by purchases of the game.")

@command('compiler', 'cl', 'msvc', 'clang')
def usedCompilierInfo(bot, trigger):
    """Command to answer the many what compiler is he using
    """
    info(bot, trigger, "Casey compiles from a batch file using MSVC on windows, but has told us he uses Clang to compile on GNU/Linux, BSD, and OS X. You can get the same version of MSVC which he uses on stream completely free as part of Visual Studio 2013 Community Edition here: http://goo.gl/BzGwMC (More: !build, !batch)")

@command('templates')
def whyNoTemplatesInfo(bot, trigger):
	"""Command to answer the many why Casey avoids using C++ templates where possible
	"""
	info(bot, trigger, "Casey avoids using C++ templates where not absolutely necessary, as they lead to longer compile times and make debugging harder. See also: http://mollyrocket.com/forums/molly_forum_402.html")
	
@command('build', 'batch')
def usedBuildBatchInfo(bot, trigger):
    """Command to answer the many why Casey builds HMH the way he does
    """
    info(bot, trigger, "Casey compiles from a batch file using MSVC on windows, allowing a rebuild from the command line, from Emacs (his editor), or even from within MSVC. The program is actually compiled as a single translation unit (it uses #include to compile all involved files in one go), this keeps things simple, as the build script mostly needs to be changed only when adding a dependency. (More: !editor, !compiler)")
	
@command('render', 'opengl', 'd3d')
def renderInfo(bot, trigger):
    """Command to give render information to the chat target
    """
    info(bot, trigger, "We are currently using software rendering in order to implement our own renderer. Ultimately the game will take advantage of hardware acceleration (i.e. using OpenGL, Direct3D, etc.) to maximize performance.")

@command('learning', 'learnProgramming')
def gettingStartedLearning(bot, trigger):
    """Command for basic learning instructions for all those where to start learning questions we get during the stream
    """
    info(bot, trigger, "One way to start programming in this manner is to watch the Intro to C series on www.youtube.com/handmadeheroarchive to get a general feel of things. Later, read 'The C Programming Language' by Brian W. Kernighan and Dennis M. Ritchie and work through all the exercises. The most important part is to start coding and to make lots of things in code. Good luck!")

@command("lib", "library", "api")
def libCommand(bot, trigger):
    info(bot, trigger, "The point of Handmade Hero is to build it all from scratch. To that extent, the only external libraries we'll be referencing are platform libraries (such as the Windows API).")

@command("wrench")
def codeIsATool(bot, trigger):
    info(bot, trigger, "Programming is not about the languages. Code is the tool used to solve the problems programmers must address. For more on this perspective, refer to Mike Acton's talk: 'Data-Oriented Design and C++' (https://www.youtube.com/watch?v=rX0ItVEVjHc)")

@command("partner")
def twitchPartner(bot, trigger):
    info(bot, trigger, "A Twitch partnership would require Casey to hold the archive videos for 24 hours before uploading to YouTube.")

@command("math")
def whyMath(bot, trigger):
    info(bot, trigger, "Tackling game programming issues, such as vectors for player movement, can be a roadblock for many. To learn math for games, please check out: http://goo.gl/bOn6To")

@command('wheel', 'gamasutra')
def reinventingWheel(bot, trigger):
    info(bot, trigger, "Why reinvent the wheel? Please check out http://goo.gl/zzDW3d, specifically questions #3 and #4 posed by the interviewer.")

@command("cleancode")
def cleanCode(bot, trigger):
    info(bot, trigger, "'Clean Code' can at times be misleading or dogmatic. See http://goo.gl/N4AJdu or http://goo.gl/xqUMK0")

@command("jai")
def jai(bot, trigger):
    info(bot, trigger, "JAI is a new programming language designed for games being created by Jonathan Blow, the designer of Braid and The Witness. You can find out more about JAI here: http://goo.gl/oS9Er4 Follow Jonathan Blow on twitch for new demos here: http://goo.gl/wEPKq5")

@command("unittest", "unittests", "tests")
def unitTest(bot, trigger):
    info(bot, trigger, "We won't be doing unit tests on Handmade Hero because the structure of a game changes a lot over the course of its development, and game systems don't tend to fit into easily testable components.")
    
@command("compression")
def compressionOriented(bot, trigger):
    info(bot, trigger, "Casey programs using an approach which he often calls Compression Oriented Programming, in which he will code things in the most straightforward way first, and only loft up common functionality into higher level structures as it becomes apparent that it is necessary. You can read more about the approach here: http://goo.gl/rVgCHI")

@command("break", "vacation")
def breakInfo(bot, trigger):
    info(bot, trigger, "Handmade Hero is on break and will resume March 18th due to Casey traveling March 16th through the 17th.")

@command("jeffandcasey", "jeffandcaseyshow")
def jeffandcasey(bot, trigger):
    info(bot, trigger, "The Jeff and Casey show! http://mollyrocket.com/jacs/index.html")

@command("software", "programs")
def software(bot, trigger):
    info(bot, trigger, "The software visibly used on the stream are: Mischief, emacs, cmd, cloc, MS Visual Studio 2013 (Community Edition), and OBS")

@command("port", "porting")
def port(bot, trigger):
    info(bot, trigger, "Handmade Hero is being programmed for Windows and is planned to be ported to Mac OS, Linux, Raspberry Pi, and Android.")
