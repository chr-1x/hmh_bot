import willie
import willie.module

from streambot import Cmd, command, info, whitelisted, adminonly, whitelisted_streamtime, adminonly_streamtime

@command("jai", "what", "lang")
def jai(bot, trigger):
	info(bot, trigger, "JAI is the codename for the language Jonathan Blow is creating to address common problems game programmers face using existing languages.")

@command("jon", "who")
def jonbio(bot, trigger):
	info(bot, trigger, "Jonathan Blow is a game developer and programmer who created Braid and The Witness, and is now developing a new language for game progrmaming.")

