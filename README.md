hmh_bot
============

Python module for the Willie IRC bot used in the Handmade Hero twitch chat.

Custom commands are defined in `handmade.py`, `handmade_faq.py`, `handmade_stream.py`, and `handmade_bonus.py`. `handmade.py` should be reserved commands related to the bot functionality, `handmade_faq.py` for common stream questions, `handmade_stream.py` for stream scheduling and timing based functions, and `handmade_bonus.py` for easter eggs and miscellaneous commands.

The config options used by the bot are available in `handmade.cfg`. Please refer to the [Willie documentation](http://willie.dftba.net/) for what the common configuration options mean.

`test.py` is currently deprecated, it might be useful at some point in the future to attempt to set up a series of tests to run to ensure the bot remains working.

Please refer to the [forum thread](https://forums.handmadehero.org/index.php/forum?view=topic&catid=5&id=65) and Issues page for discussion about features to add and updates.

Installation
============
* Clone the repository and cd into the directory.
* Read through `sampleconfig.txt` and fill in necessary information
* Rename the config file, e.g. `handmade.cfg`
* Run `willie -c handmade.cfg` to start the bot.

Important: Please make sure that there is not already an instance of ChronalRobot running in chat. Twitch will not prevent multiple of them from running at a time, and all active instances will attempt to respond to queries. An easy way to test for this is to use the `!hello` command, as this should always be available. (Note: as of recently, the default bot username is now **hmh_bot**. You can run your own instance alongside if you change the username, oauth, and command character for the bot.)

If you should need to find out who is running a particular instance of the bot, use `!owner` in chat.

For help setting up the config, have a look at `Setup.md`

Libraries
---
Robot requires the following libraries to be installed: willie, arrow, parsedatetime, and sqlobject

To install them, issue following command:

`sudo pip install willie arrow parsedatetime sqlobject`

NOTE: WILLIE became SOPAL(https://github.com/sopel-irc/sopel) we are not upgrading for the time being
