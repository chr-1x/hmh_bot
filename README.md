ChronalRobot
============

Python module for the Willie IRC bot used in the Handmade Hero twitch chat.

All custom commands are defined in `handmade.py`. (For now) please refer to the docstrings and comments for more specific information on commands and functions.

The config options used by the bot are available in `willie.cfg`. Please refer to the [Willie documentation](http://willie.dftba.net/) for where this file needs to be on locally deployed bots.

Also included in the repository is a light (read: very incomplete) shim of the willie framework for running tests. (NOTE: since 2014/12/15 this is broken, need to do some restructuring to get it working again)

Please refer to the [forum thread](https://forums.handmadehero.org/index.php/forum?view=topic&catid=5&id=65) and Issues page for discussion about features to add and updates.

Installation
----
Copy the contents of this repo to your ~/.willie folder if you're on linux, or to wherever the willie config folder is created on windows. 

Then run `willie` to start the bot.

Important: Please make sure that there is not already an instance of ChronalRobot running in chat. Twitch will not prevent multiple of them from running at a time, and all active instances will respond to queries. 
