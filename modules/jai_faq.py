import willie
import willie.module

from streambot import Cmd, command, info, whitelisted, adminonly, whitelisted_streamtime, adminonly_streamtime

@command("jai", "what", "lang")
def jai(bot, trigger):
	info(bot, trigger, "JAI is the codename for the language Jonathan Blow is creating to address common problems game programmers face using existing languages. To learn more about these problems in detail, check out http://goo.gl/dZ9QVe")

@command("jon", "who")
def jonbio(bot, trigger):
	info(bot, trigger, "Jonathan Blow is a game designer and programmer, previously of Braid (http://braid-game.com/), currently working on The Witness (http://the-witness.net/news) and a new programming language for games called JAI. For more info: !jai")

@command("!old", "!archive")
def archive(bot, trigger):
    info(bot, trigger, "YT Archive: http://goo.gl/2tXMSY")

@command('ide', 'emacs', 'editor')
def ideInfo(bot, trigger):
    """Info command that provides information about the editor (emacs) used by Casey.
    """
    info(bot, trigger, "Jon uses Emacs to edit his code, because that is what he is used to. There are a lot of editors out there, however, so you should use whatever you feel most comfortable with.")

@command('college', 'school')
def collegeInfo(bot, trigger):
    info(bot, trigger, "Jon did not finish college; he has been coding professionally in the gaming industry since 1996. You can read his thoughts here: http://number-none.com/blow")

@command('site')
def siteInfo(bot, trigger):
    """Info command that prints out the site/forum links.
    """
    info(bot, trigger, "Jon's Website: http://number-none.com/blow  ::  YT Archive: http://goo.gl/2tXMSY")

@command('chocolate')
def chocolateBar(bot, trigger):
    info(bot, trigger, "Jon always has chocolate bars handy during stream. It eases the tension of difficult compiler demos.")
