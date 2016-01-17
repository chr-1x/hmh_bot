Setup Information
============

This file is intended as a resource to help you get started should you want to spin up your own copy of the bot. Each of the settings here are ones you should check and edit if needed in the config. For more detailed explanations and additional settings please refer to the [Willie documentation](http://willie.dftba.net/).

##Config vars (and what they mean)

###[core]
* **nick** - Name that the bot will show up as in chat
* **user** - Username of the bot, needed for authentication with the IRC network
* **host** - Hostname of the IRC network, e.g. `irc.quakenet.org`, `irc.freenode.net`, `irc.twitch.tv`
* **use_ssl** - Some networks require SSL connections, you can specify that here (bool)
* **port** - Port on which to connect to the server. If your IRC network uses a different port, specify it here. Default for IRC is **6667**
* **owner** - Name of the user running the bot. Useful to tell multiple bots apart. <prefix>owner in chat to see who the bot's owner is.
* **channels** - Comma separated list of all channels to connect to. Remember that IRC channels are prefixed with **#**
* **server_password** - Some networks require authentication, you can specify that here
* **prefix** - Command prefix the bot will listen for. `\!` means the bot will listen for commands starting with `!` e.g. `!hello`
* **extra** - Path to the `modules` folder. One is included in this repository, so for example you would specify the path to that folder
* **exclude** - Modules **not** to be loaded by the bot
* **enable** - Modules **to** be loaded by the bot
* **admins** - Comma separated list of usernames who are authorized to use all commands in the bot
* **whitelist** - Comma separated list of usernames who are authorized to use most commands in the bot
* **logdir** - Where to put the bot's logs. Examples of the files that will go here are `exceptions.log`, `raw.log`, and `stdio.log`

###[db]
* **userdb_file** - File where the bot will read and store information from. *If the bot does not have read and write permissions, you may see errors in chat*. This is where we use `handmade.db`. If you would like a copy of that db file, [you can get it here](http://j.mp/hmh_db).

###[chanlogs]
* **dir** - Folder where the bot will log everything that happens in IRC channels.
* **by_day** - Rotate the log every day. Creates a new .log file for each channel every 24 hours. (bool)(recommended)

That's it! You're all set to run your own instance of the bot!

##Notes
* [Willie](http://willie.dftba.net/) will automatically create a database in the format `configname.db` in addition to what you specify for `userdb_file` e.g. if you have your config file named `myawesomeconfig.cfg`, when you start the bot it will create a database named `myawesomeconfig.db`.
* Timezone is set to PST (Casey's timezone). We are using this to avoid confusion elsewhere.
* Depending on your install, you *may* require absolute paths in your config instead of relative paths, else problems will arise. E.g. `/full/path/to/modules` instead of `./modules`
