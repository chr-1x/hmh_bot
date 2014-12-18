import willie
import willie.module
from willie.tools import stderr
import random
from datetime import datetime
from pytz import timezone

import os, sys
sys.path.append(os.path.dirname(__file__))


if not 'commands' in globals():
    commands = []

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

def command(*args, **kwargs):
    """Decorator that just passes it on to the built-in willie command decorator, but also adds it 
        to the module's command list (for !list function, etc)
    """
    global commands

    #stderr("Registered command %s, total %d commands" % (str(args), len(commands)))
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
    import handmade_stream as stream
    ###TODO(chronister): Can this be done as a decorator? (would have to give a custom bot 
    ###     or something?)
    streaming = stream.isCurrentlyStreaming(datetime.now(timezone("PST8PDT")))
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

@command('amIadmin', 'isAdmin', 'isWhitelisted', 'whitelisted', hide=True)
def isAdmin(bot, trigger):
    """Simple command that simply tells the user whether or not they are an admin. Mostly 
        implemented for debugging (double-checking case sensitivity and things)
    """
    if (trigger):
        args = trigger.group(2)
        if (args):
            args = args.split(" ") 
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
    global commands
    visibleCommands = [c.main for c in commands if not(c.hide==True)]
    bot.say("Here are all of the HH stream commands: !%s" % ", !".join(visibleCommands))