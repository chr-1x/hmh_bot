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

@whitelisted_streamtime
@command('google', 'g' ,'search', 's', hide=True)
def googleSearch(bot,trigger):
    """Command that searches google for the string provided
    """
    if not trigger: return
    if stream.isCurrentlyStreaming() and not trigger.admin: return
    if not trigger.group(2):
        bot.say("@%s: https://google.com/" % trigger.nick)
    else:
        query = trigger.group(2).strip()
        bot.say("@%s: %s" % (trigger.nick, google_search(query)))

@command('now', 'pst', 'PST', hide=False, cooldown=10)
def getTime(bot, trigger):
    """Info command that prints out the current time in PST. For the purposes of the handmade hero
        stream, we don't really care about other time zones.
    """
    now = arrow.now('US/Pacific')
    info(bot, trigger, "The current time in Seattle is %s" % (now.strftime("%I:%M %p %Z")))

@command('site', 'forum', 'forums', hide=False, cooldown=10)
def siteInfo(bot, trigger):
    """Info command that prints out the site/forum links.
    """
    info(bot, trigger, 'HMH Website: http://goo.gl/fmjocD  ::  HMH Forums: http://goo.gl/X5JDvT')

@command('old', 'archive', hide=False, cooldown=10)
def archiveInfo(bot, trigger):
    """Info command that prints out the forum/youtube archive links.
    """
    info(bot, trigger, 'Annotated Episode Guide: https://goo.gl/O5ljen   ::   YouTube Archive: http://goo.gl/u3hKKj')

@command('wrist', 'wrists', 'braces', 'hands', hide=False, cooldown=10)
def wristInfo(bot, trigger):
    """Info command that prints out info about Casey's wrist braces
    """
    info(bot, trigger, "The wrist braces Casey wears help make typing more comfortable and prevent Repetitive Strain Injury. They were made by Medi-Active (the ones without the thumb brace) but are no longer in production.")

@command('milk', 'almondmilk', 'drink', cooldown=10)
def milkInfo(bot, trigger):
    """Info command that prints out info about almond milk.
    """
    info(bot, trigger, "One of Casey's drinks of choice is Almond Milk, a delicious and refreshing beverage. Some common brands are Silk and Almond Breeze. Over Summer, Casey has been making his own lemonade.")

@command('who', 'casey', hide=False, cooldown=10)
def caseyInfo(bot, trigger):
    """Info command that prints out info about Casey. Could be refactored into multiple commands
        for better clarity.
    """
    info(bot, trigger, "Casey Muratori is a 38 year old software engineer living in Seattle, Washington. He started Handmade Hero to give the general public a better idea of what coding a game from scratch is like based on his experiences in the industry. For a full bio, see http://mollyrocket.com/casey/about.html")

@command('hello', 'hi', hide=True, cooldown=10)
def helloMessage(bot, trigger):
    """Command that shows hello,world style information.
        Possible addition: name-based trigger? e.g. "Chronalrobot: hi" or "hi Chronalrobot"
    """
    bot.say("Hello, I am an IRC bot! Try some commands: !help, !list, !when, !what")

@whitelisted_streamtime
@command('botinfo', hide=True, hideAlways=False, cooldown=10)
def infoMessage(bot, trigger):
    """Command that shows information about the chatbot. Should be updated with contributor info
        and github page once that happens.
    """
    bot.say("I am a Python IRC bot based on Willie (http://willie.dftba.net/). I was started by ChronalDragon and am now jointly maintained by the good folks who commit to my github repo (https://github.com/Chronister/ChronalRobot). See also: !credits")

@whitelisted_streamtime
@command('credits', hide=True, hideAlways=False, cooldown=10)
def creditsMessage(bot, trigger):
    """Shows contributor info! If you make changes, add yourself here (or get someone else to)
    """
    bot.say("Thanks to chronister (chronaldragon), alexwidener (iamdefinitelybatman), dspecht (drive137), itsuart (isuart2), abnercoimbre, kkartaltepe (kurufu), mvandevander (garlandobloom), deguerre (pseudonym73), effect0r, EpicDavi, nxsy, flamedog, insofaras, soulflare3 and kelimion for their contributions to my code!")

@command('buy', 'purchase', 'support', 'patreon','source','sauce', hide=False, cooldown=10)
def buyInfo(bot, trigger):
    """Info command that prints out where you can buy the game/support the project.
    """
    info(bot, trigger, "The Handmade Hero art assets and full source code can be purchased at http://goo.gl/y20Q9C . You can also support Casey monthly at http://www.patreon.com/cmuratori")


@command('game', 'gameinfo', hide=False, cooldown=10)
def gameInfo(bot, trigger):
    """Info command that displays basic information about the game being built.
    """
    info(bot, trigger, "Handmade Hero is a 2Dish top-down game inspired by classic Zelda games and modern games like The Binding of Isaac. The entire development of the game is being catalogued in these streams. (More: !art, !lang)")

@command('friday', hide=True, cooldown=10)
def fridays(bot, trigger):
    """Until we have a set schedule and while Casey keeps up doing early Fridays"""
    info(bot, trigger, "Handmade Hero used to air at a different time on Fridays. However, it now airs at 5pm most weekdays.")

@command('stream', 'about', 'info', 'what', hide=False, cooldown=10)
def streamInfo(bot, trigger):
    """Info command that displays basic information about the stream itself.
    """
    info(bot, trigger, "In this stream, game programmer Casey Muratori is walking us through the creation of a game from scratch in C. The game is being developed for educational purposes: he will explain what he is doing every step of the way. For more information, visit http://goo.gl/fmjocD")

@command('lang', 'language', 'codedin', hide=False, cooldown=10)
def langInfo(bot, trigger):
    """Info command that provides a description of the language and style used on the stream.
        Could be split into two commands, one for simple info and one about the structural choices.
    """
    info(bot, trigger, "The language used in the stream is a subset of C++ that is very C-like with a few differences, such as the use of operator and function overloading. Since we're writing everything from scratch, we will not be using the C or C++ standard libraries wherever possible.")

@command('ide', 'emacs', 'editor', hide=False, cooldown=10)
def ideInfo(bot, trigger):
    """Info command that provides information about the editor (emacs) used by Casey.
    """
    info(bot, trigger, "Casey uses Emacs to edit his code because that is what he is used to. There are a lot of editors out there, however, so you should use whatever you feel most comfortable in. (See also: !emacsversion)")

@command('editoradvice', 'whicheditor', hide=False, cooldown=10)
def ideAdvice(bot, trigger):
    """Info command that suggests what to use for editing code"""
    info(bot, trigger, "All that's needed to write code is a text editor that preserves formatting. Some editors, such as the classic editors Vim and Emacs, have special features to help streamline the process of writing code. Other, more modern editors that may feel more comfortable are Notepad++ and Sublime Text.")

@command('emacsversion', 'version')
def emacsVersion(bot, trigger):
    """Info command that provides information about the emacs version.
    """
    info(bot, trigger, "The version of emacs that Casey uses is GNU Emacs 23.4.1 (i386-mingw-nt6.1.7601), released in 2012.")

@command('college', 'school', hide=False, cooldown=10)
def collegeInfo(bot, trigger):
    info(bot, trigger, "Casey did not go to college; he has been coding in the gaming industry since 1995. You can read his biography here: http://mollyrocket.com/casey/about.html")

@command('keyboard', 'kb', hide=False, cooldown=10)
def keyboardInfo(bot, trigger):
    """Info command that provides information about what keyboard Casey uses.
    """
    info(bot, trigger, "Casey is currently using a Das Keyboard 3. See also: !switches")

@command('switches', 'switch', 'mechanical', hide=False, cooldown=10)
def moreKeyboardInfo(bot, trigger):
    """What switches are in your keyboard?
    """
    info(bot, trigger, "The keyboard switches are Cherry MX Brown. See also: !keyboard")

@command('totalTime','length', 'years', 'total', hide=False, cooldown=10)
def timeOfProject(bot, trigger):
    """How long is the project going on?"""
    info(bot, trigger, "It is estimated that the project will take at least 2 years (600 episodes) to finish at the current rate of five 1-hour streams per week.")

@command('art', 'artist', hide=False, cooldown=10)
def artCreatorInfo(bot, trigger):
    """Command to state who the art is done by
        TODO: maybe look to casey to get a link the artists profile for viewing
    """
    info(bot, trigger, "The art in Handmade Hero is created by Yangtian Li (http://www.yangtianli.com/), an artist Casey knows whom he contracted using the funds provided by purchases of the game.")

@command('compiler', 'cl', 'msvc', 'clang', hide=False, cooldown=10)
def usedCompilierInfo(bot, trigger):
    """Command to answer the many what compiler is he using
    """
    info(bot, trigger, "Casey compiles from a batch file using MSVC on windows, and has told us he uses Clang to compile on GNU/Linux, BSD, and OS X. You can get the same version of MSVC which he uses on stream completely free as part of Visual Studio 2013 Community Edition here: http://goo.gl/BzGwMC (More: !build, !batch, !unity)")

@command('templates', hide=True, hideAlways=False, cooldown=10)
def whyNoTemplatesInfo(bot, trigger):
	"""Command to answer the many why Casey avoids using C++ templates where possible
	"""
	info(bot, trigger, "Casey avoids using C++ templates where not absolutely necessary, as they lead to longer compile times and make debugging harder. See also: http://mollyrocket.com/forums/molly_forum_402.html")

@command('build', 'batch', 'unity', 'stu', hide=False, cooldown=10)
def usedBuildBatchInfo(bot, trigger):
    """Command to answer the many why Casey builds HMH the way he does
    """
    info(bot, trigger, "On windows, Casey compiles with MSVC from a batch script, also called by Emacs for rebuilds. The program builds as a single translation unit (STU) using #include to compile all involved files in one go, which we call a unity or STU build. The script needs a change only when adding a dependency. See also: Day 011, http://goo.gl/8ATplA (More: !editor, !compiler)")

@command('render', 'renderer', 'd3d', hide=False, cooldown=10)
def renderInfo(bot, trigger):
    """Command to give render information to the chat target
    """
    info(bot, trigger, "We are currently using software rendering in order to implement our own renderer. Ultimately the game will take advantage of hardware acceleration (i.e. using OpenGL, Direct3D, etc.) to maximize performance. See also !opengl.")

@command('opengl', 'ogl', hide=False, cooldown=10)
def renderInfo(bot, trigger):
    """Command to give openGL information to the chat target
    """
    info(bot, trigger, "While Casey will rewrite the renderer using OpenGL in the future - see !render - the current OpenGL code is to allow for vsync, giving a more predictable frame time.")

@command('learning', 'learnProgramming', 'learn', hide=False, cooldown=10)
def gettingStartedLearning(bot, trigger):
    """Command for basic learning instructions for all those where to start learning questions we get during the stream
    """
    info(bot, trigger, "Programming can actually be quite simple if you start out right. For absolute beginners, try khanacademy.org or codecademy.com for garden-path tutorials and explanations, or c.learncodethehardway.org/book/ for a more self-directed introduction to C programming, LearnXinYminutes is a quick way to get a overview of a language found here http://goo.gl/ZEDxDt. See !learnC for more.")

@command('learnC', 'learnC\+\+', 'likeCasey')
def learningC(bot, trigger):
    """Command describing how you can begin learning C, like this
    """
    info(bot, trigger, "One way to start programming in this manner is to watch the Intro to C series at https://hero.handmadedev.org/jace/guide/ to get a general feel of things. Later, read 'The C Programming Language' by Brian W. Kernighan and Dennis M. Ritchie and work through all the exercises, LearnXinYminutes can be used to see the basics of C http://goo.gl/qmluuM. The most important part is to start coding and to make lots of things in code. Good luck!")

@command("lib", "library", "api", "engine", hide=False, cooldown=10)
def libCommand(bot, trigger):
    info(bot, trigger, "The point of Handmade Hero is to build it all from scratch. To that extent, the only external libraries we'll be referencing in the game itself are platform libraries (such as the Windows API). We may make limited use of libraries in tools external to the game such as the asset builder.")

@command("wrench", hide=True, hideAlways=False, cooldown=10)
def codeIsATool(bot, trigger):
    info(bot, trigger, "Programming is not about the languages: code is a tool used to solve problems that programmers face. Some languages address certain tasks better than others, but ultimately you simply need to end up with code that hasn't wasted your users' time or your own time.")

@command("data", "dataOriented", "dataDesign", hideAlways=False, cooldown=10)
def dataOrientation(bot, trigger):
    info(bot, trigger, "A lot of software, including games, require the programmer to focus on the flow of data in the computer rather than the abstract structure of their program. For more on this perspective, refer to Mike Acton's talk: 'Data-Oriented Design and C++' (https://www.youtube.com/watch?v=rX0ItVEVjHc)")

@command("partner", hide=True, hideAlways=False, cooldown=10)
def twitchPartner(bot, trigger):
    info(bot, trigger, "A Twitch partnership would require Casey to hold the archive videos for 24 hours before uploading to YouTube. If you would like to help support the project, see !support")

@command("math", hide=True, hideAlways=False, cooldown=10)
def whyMath(bot, trigger):
    info(bot, trigger, "Tackling the math required to program games can be a roadblock for many. See http://goo.gl/bOn6To for a broad overview of the types of math used in games, or check out Coding Math, a youtube series on simple math for programmers, at https://goo.gl/67ZG1F")

@command('wheel', 'gamasutra', hide=True, hideAlways=False, cooldown=10)
def reinventingWheel(bot, trigger):
    info(bot, trigger, "Why reinvent the wheel? Please check out http://goo.gl/zzDW3d, specifically questions #3 and #4 posed by the interviewer.")

@command("cleancode", hide=True, hideAlways=False, cooldown=10)
def cleanCode(bot, trigger):
    info(bot, trigger, "'Clean Code' can at times be misleading or dogmatic. For some perspectives on this discussion, check out Casey's response here: http://goo.gl/N4AJdu and Jonathon Blow's presentation here: http://goo.gl/xqUMK0")

@command("jai", hide=True, hideAlways=False, cooldown=10)
def jai(bot, trigger):
    info(bot, trigger, "JAI is a new programming language designed for games being created by Jonathan Blow, the designer of Braid and The Witness. You can find out more about JAI here: http://goo.gl/oS9Er4 and follow Jonathan Blow on twitch for new demos here: http://goo.gl/wEPKq5")

@command("unittest", "unittests", "tests", hide=True, hideAlways=False, cooldown=10)
def unitTest(bot, trigger):
    info(bot, trigger, "We won't be doing unit tests on Handmade Hero because the structure of a game changes a lot over the course of its development, and game systems don't tend to fit into easily testable components.")

@command("compression", hide=True, hideAlways=False, cooldown=10)
def compressionOriented(bot, trigger):
    info(bot, trigger, "Casey programs using an approach which he often calls Compression Oriented Programming, in which he will code things in the most straightforward way first, and only loft up common functionality into higher level structures as it becomes apparent that it is necessary. You can read more about the approach here: http://goo.gl/rVgCHI")

@command("break", "vacation", hide=True, hideAlways=True, cooldown=10)
def breakInfo(bot, trigger):
    info(bot, trigger, "Handmade Hero is on break from Oct 30 to Nov 16 as Casey is travelling.")

@command("jeffandcasey", "jeffandcaseyshow", hide=True, hideAlways=False, cooldown=10)
def jeffandcasey(bot, trigger):
    info(bot, trigger, "The Jeff and Casey show! http://mollyrocket.com/jacs/index.html")

@command("software", "programs", hide=False, cooldown=10)
def software(bot, trigger):
    info(bot, trigger, "The programs visibly used on the stream are Mischief (drawing), emacs (coding), cmd (command line), cloc (line counting), MS Visual Studio 2013 - Community Edition (debugging), and OBS (recording)")

@command("port", "porting", "linux", "platform", "platforms", "mac", "android", hide=True, hideAlways=False, cooldown=10)
def port(bot, trigger):
    info(bot, trigger, "Handmade Hero is being programmed on Windows at the moment but most likely will be ported to Mac OS, Linux, Raspberry Pi, and Android.")

@command("tablet", "wacom", "mouse", "blackboard", hide=False, cooldown=10)
def tablet(bot, trigger):
    info(bot, trigger, "Casey's handwriting is aided by the use of a Wacom Intuos 3 tablet. The 'blackboard' is the graphics program Mischief.")

@command("script", "scripting", hide=False, cooldown=10)
def scripting(bot, trigger):
    info(bot, trigger, "We will not be creating a scripting language for Handmade Hero because we have a hot-reloading feature! We can keep all the code in one language with all the benefits that scripting languages typically try to offer.")

@command("quotelist", "listquotes", "listquote", "listq", "lq", "ql", hide=False, cooldown=10)
def quotelist(bot, trigger):
    info(bot, trigger, "A list of all saved quotes is available here: https://goo.gl/YYT8rN.")

@command("rules", "chatrules", "chat", hide=False, cooldown=10)
def rules(bot, trigger):
    info(bot, trigger, "The Handmade Hero moderator team volunteers their time in order to keep chat civil and clean during stream time. Spamming, repetitive arguments that clog up the chat, or refusal to cooperate with a reasonable request from a moderator may result in a ban from the chat at the moderators' sole discretion.")

@command("userlist", "users", hide=False, cooldown=10)
def userlist(bot, trigger):
    info(bot, trigger, "Are you on IRC and missing a user list? Use the raw command in your IRC client (/raw or /quote usually, or just /cap) to issue the following command: CAP REQ :twitch.tv/membership For the change to take effect you will need to use /cycle (if supported) or /part and /join in that order. It is recommended to add this to your connect command.")

@command("never", "neverabout", hide=False, cooldown=10)
def never(bot, trigger):
    info(bot, trigger, "Programming is not really about the code. See moderator AbnerCoimbre's informal lecture on the subject here: http://y2u.be/Lzc3HcIgXis or a more extensive talk from Mike Acton here: http://y2u.be/rX0ItVEVjHc")

@command("design", "gamedesign", hide=False, cooldown=10)
def design(bot, trigger):
    info(bot, trigger, "Handmade Hero is primarily a demonstration of game _programming_, and the design of the game is intended only to facilitate that by employing complex mechanics and interesting interactions, and may not necessarily innovate in any particular direction. If you'd like to see a lecture on game design from moderator GarlandoBloom, see http://y2u.be/0zVjdEhHmGo")

@command("manifesto", hide=False, cooldown=10)
def manifesto(bot, trigger):
    info(bot, trigger, "You can read The Handmade Manifesto here: http://handmadedev.org/manifesto/")

@command("hmhcon", "con", "convention", hide=False, cooldown=10)
def hmhcon(bot, trigger):
    info(bot, trigger, "HandmadeCon 2015 will be held on Krampusnacht in Seattle. More specifically: Saturday, December 5th, 2015, from 10AM to 6PM PST, in the auditorium at the central branch of the Seattle Public Library. There are 275 tickets total, at $45/ticket (or $35/ticket if ordered before November 5th). Read the latest info at http://handmadecon.org")


#TODO(soul): Maybe we want to change the wording of this? What do you guys think?
@command("ask","question","a2a","asktoask","ask2ask", hide=False, cooldown=10)
def ask2ask(bot, trigger):
    info(bot, trigger, "Don't ask to ask a question, simply ask your question. Many regulars use IRC, so we will see your question eventually. If you can't stay long, you may also ask your question on the !forum")

@command("creative", "category", hide=False, cooldown=10)
def creativeAsk(bot, trigger):
    info(bot, trigger, "Handmade Hero is being streamed in the Creative section of twitch because twitch administration asked Casey to do so. It is unclear if there is a larger reason behind the decision.")
