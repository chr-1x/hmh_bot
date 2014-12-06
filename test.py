import handmade
import willie

bot = willie.Willie()

for cfp in willie.module.funcs:
	print(cfp.cmds)
	print("\n%s" % ", ".join(cfp.cmds))
	cfp.func(bot, None)


print("\nTotal Commands: %s" % len(handmade.commands))

