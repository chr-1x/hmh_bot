import willie
from datetime import datetime, timedelta
from pytz import timezone

@willie.module.commands('time', 'now', 'pst', 'PST')
def time(bot, trigger):
    now = datetime.now(timezone("PST8PDT"))
    bot.say("The current time in Seattle is %s:%s %s PST" % (now.strftime("%I"), now.minute, "PM" if now.hour > 11 else "AM"))

@willie.module.commands('timer', "when", "howlong")
def timer(bot, trigger):
    streamTime = datetime.now(timezone("PST8PDT"))
    
    if (((streamTime.hour == 20 or (streamTime.hour == 21 and streamTime.minute <= 30)) and streamTime.weekday() < 4)
        or
        ((streamTime.hour == 11 or (streamTime.hour == 12 and streamTime.minute <= 30)) and streamTime.weekday() == 4)):
        bot.say("The stream is currently running!")
        return
        #todo: how much time is left        

    while(not(streamTime.minute == 0 and 
        (streamTime.weekday() == 4 and streamTime.hour == 11) or
        (streamTime.weekday() < 4 and streamTime.hour == 20 ))):

        streamTime = streamTime + timedelta(minutes=1) #inc minutes


    nowTime = datetime.now(timezone("PST8PDT"))
    untilStream = streamTime - nowTime;

    untilHours = untilStream.seconds / 3600
    untilMinutes = (untilStream.seconds - untilHours * 3600) / 60

    if (untilStream.days != 0):
        bot.say('Next stream is in %d days, %d hours %d minutes' % (untilStream.days, untilHours, untilMinutes))
    else:
        bot.say('Next stream is in %d hours %d minutes' % (untilHours, untilMinutes))

@willie.module.commands('site')
def siteInfo(bot, trigger):
    bot.say('HH Website: http://handmadehero.org/  ::  HH Forums: http://forums.handmadehero.org/')

@willie.module.commands('old', 'archive')
def archiveInfo(bot, trigger):
    bot.say('YT Archive: https://www.youtube.com/user/handmadeheroarchive')

@willie.module.commands('wrist', 'braces')
def wristInfo(bot, trigger):
    bot.say('The wrist braces Casey wears help make typing more comfortable and prevent Repetitive Strain Injury.')

@willie.module.commands('milk', 'almondmilk')
def milkInfo(bot, trigger):
    bot.say("One of Casey's drinks of choice is Almond Milk, a delicious and refreshing beverage. Some common brands are Silk and Almond Breeze.")

@willie.module.commands('who', 'casey')
def caseyInfo(bot, trigger):
    bot.say("Casey Muratori is a software engineer who lives in Seattle. He has done work for various companies such as RAD game tools and on games such as The Witness, and has also done fiction writing and podcasting. He started Handmade Hero to give the general public a better idea of what coding a game from scratch in C is like based on his experiences in the industry.")

@willie.module.commands('thanks')
def thanksMessage(bot, trigger):
    bot.say("Thanks for streaming, Casey! <3")

@willie.module.commands('hello', 'hi')
def helloMessage(bot, trigger):
    bot.say("Hello, I am an IRC bot! Try some commands: !timer, !site, !google, !info")

@willie.module.commands('info')
def infoMessage(bot, trigger):
    bot.say("I am a Python IRC bot based on Willie (http://willie.dftba.net/). I am run by ChronalDragon, who can be contacted via https://tinyurl.com/ChronalDragon")

@willie.module.commands('buy', 'purchase')
def buyInfo(bot, trigger):
    bot.say("Handmade Hero, the compiled game with art assets and full source code, can be purchased at http://handmadehero.org/#buy_now")

@willie.module.commands('game', 'what')
def gameInfo(bot, trigger):
    bot.say("Handmade Hero is a project to build an entire game in C from scratch, no libraries. We don't know what kind of game it will be yet, but we know it will be 2D, cross-platform, and feature art by Yangtian Li as well as specially licensed music. For more information, visit http://handmadehero.org/")

@willie.module.commands('beep', 'boop')
def beepBoop(bot, trigger):
    bot.say("Don't speak of my mother that way!")

@willie.module.commands('why')
def whyInfo(bot, trigger):
    bot.say("Because he can.")

@willie.module.commands('random')
def randomNumber(bot, trigger):
    bot.say("Your random number is %s" % 4)

@willie.module.commands('lang', 'language', 'codedin')
def langInfo(bot, trigger):
    bot.say("The language we are using in Handmade Hero is C++ coded in a C-like style. We will most likely not be using classes, inheritance, or polymorphism to any significant degree.")

@willie.module.commands('ide', 'emacs', 'editor')
def ideInfo(bot, trigger):
    bot.say("Casey uses emacs to edit his code, because that is what he is used to. It is getting pretty old, so you should use whatever you feel most comfortable in.")

@willie.module.commands('keyboard', 'kb')
def keyboardInfo(bot, trigger):
    bot.say("The mechanical keyboard Casey uses is a Das Keyboard 4.")

@willie.module.commands('list', 'commands', 'cmds')
def commandList(bot, trigger): 
    bot.say("Here are all of my commands: %s" % "<TBD>")    
