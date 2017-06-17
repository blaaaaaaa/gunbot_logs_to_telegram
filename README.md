# gunbot_logs_to_telegram
Gunbot trading bot trade logs send to telegram bot. 

Python 2 Script to send most recent GUNBOT trading logs changes (the most recent trade) to your telegram bot.

Dependencies:

python-telegram-bot
watchdog

https://pypi.python.org/pypi/watchdog
pip install watchdog

https://github.com/python-telegram-bot/python-telegram-bot
pip install python-telegram-bot --upgrade


HOWTO:

In gunbot_logs_to_telegram.py:

Edit "telegram_bot_token" to your telegram bot token you got from BotFather. (Talk to BotFather andd say "/newbot" to create a bot.)

Edit "folder_to_watch folder" to your GUNBOT Folder containg the *-trades.txt files. Or if you run several at once you can put in a parent folder.

Run: 
python gunbot_logs_to_telegram.py

Tested on windows so far.
