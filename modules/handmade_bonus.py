import random

import os, sys
sys.path.append(os.path.dirname(__file__))

from handmade import command, info


### NOTE:
# These functions are easter eggy, probably not good to keep on all the time. 

@command('makemeadmin', hide=True)
def makeAdmin(bot, trigger):
    bot.say("I'm sorry, %s, I'm afraid I can't do that." % trigger.nick)

@command('beep', 'boop', hide=True)
def beepBoop(bot, trigger):
    """Easter egg command that prints out some programming/robot joke type responses
    """
    responses = [
    "Don't speak of my mother that way!",
    "That command was deprecated as of version 1.6.7, please use 1.3.1 for a more updated API",
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

@command('hug', hide=True)
def hug(bot, trigger):
    """Easter egg info command that attempts to provide human warmth and empathy in times of 
        emotional trauma.
    """
    info(bot, trigger, "Were I not a transient being circling through an ether of intangible bits and bytes, I would hug you, with all the human emotional context it implies")

@command('why', hide=True)
def whyInfo(bot, trigger):
    """Easter egg command that answers one of the remaining basic questions. Could possibly be made
        more descriptive and/or actually useful
    """
    bot.say("Because he can.")

@command('random', hide=True)
def randomNumber(bot, trigger):
    """Easter egg info command that returns a randomly-selected number.
    """
    info(bot, trigger, "Your random number is %s" % (random.randint(100) if random.random() < 0.0001 else 4))

@command('roll', hide=True)
def rollNumber(bot, trigger):
    if (trigger and trigger.group(2)):
        args = trigger.group(2).split(" ")
        output = ""
        for arg in args:
            diceArgs = arg.split("d")
            diceAmt = diceArgs[0]
            try:
                diceAmt = int(diceAmt)
            except ValueError:
                bot.say("@%s: I can't roll %s dice" % (trigger.nick, diceAmt))
                return
            diceFaces = diceArgs[1]
            try:
                diceFaces = int(diceFaces)
            except ValueError:
                bot.say("@%s: I can't roll dice with %s faces!" % (trigger.nick, diceFaces))
                return

            if (diceAmt < 0):
                bot.say("@%s: We are currently out of negative dice, please check back before." % trigger.nick)
                return
            if (diceAmt == 0):
                bot.say("@%s: No dice." % trigger.nick)
                return
            if (diceAmt > 20):
                thing = "dice"
                if (diceFaces == 2):
                    thing = "coins"
                if (diceFaces == 1):
                    thing = "one dimensional constructs"
                bot.say("@%s: Do you think I have %d %s just lying around??" % (trigger.nick, diceAmt, thing))
                return
            if (diceFaces <= 0):
                bot.say("@%s: Find me a %d sided dice and I'll roll it." % (trigger.nick, diceFaces))
                return
            if (diceFaces > 100):
                bot.say("@%s: I rolled the sphere, and it rolled off the table." % (trigger.nick))
                return

            results = []
            for i in range(diceAmt):
                results.append(random.randint(1, diceFaces))

        
            for r in results:
                output += "[%d] " % r
            output = output[:-1]
            output += ", for a total of %d" % sum(results)
            if (len(args) > 1): output += " :: "

        if (len(args) > 1): output = output[:-3]
        bot.say("@%s: %s" % (trigger.nick, output))


@command('nn', hide=True)
def nightNight(bot, trigger):
    info(bot, trigger, "Night night <3")