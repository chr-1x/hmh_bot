ChronalRobot
============

Python module for the Willie IRC bot used in the Handmade Hero twitch chat.

Custom commands are defined in `handmade.py`, `handmade_faq.py`, `handmade_stream.py`, and `handmade_bonus.py`. `handmade.py` should be reserved commands related to the bot functionality, `handmade_faq.py` for common stream questions, `handmade_stream.py` for stream scheduling and timing based functions, and `handmade_bonus.py` for easter eggs and miscellaneous commands.

The config options used by the bot are available in `default.cfg`. Please refer to the [Willie documentation](http://willie.dftba.net/) for what the common configuration options mean.

`test.py` is currently deprecated, it might be useful at some point in the future to attempt to set up a series of tests to run to ensure the bot remains working.

Please refer to the [forum thread](https://forums.handmadehero.org/index.php/forum?view=topic&catid=5&id=65) and Issues page for discussion about features to add and updates.

Installation
----
Copy the contents of this repo to your ~/.willie folder (`/home/user/.willie` on linux, `C:/Users/user/.willie` on windows)

Then run `willie` to start the bot.

Important: Please make sure that there is not already an instance of ChronalRobot running in chat. Twitch will not prevent multiple of them from running at a time, and all active instances will attempt to respond to queries. An easy way to test for this is to use the **!hello** command, as this should always be available. (Note: as of recently, the default bot username is now **hmh_bot**. You can run your own instance alongside if you change the username, oauth, and command character for the bot.)

Libraries
---
Robot requires the following libraries to be installed: pytz and parsedatetime

To install them, issue following commands:

sudo pip install pytz

sudo pip install parsedatetime
