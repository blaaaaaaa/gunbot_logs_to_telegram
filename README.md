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

Edit "telegram_your_id" to your telegram id (send "/my_id" to telegram user @get_id_bot to find out)

Edit "telegram_bot_token" to your telegram bot token you got from BotFather. (Talk to BotFather andd say "/newbot" to create a bot.)

Edit "folder_to_watch folder" to your GUNBOT Folder containg the *-trades.txt files. Or if you run several at once you can put in a parent folder.

Run: 
python gunbot_logs_to_telegram.py

Not tested alot, a little bit on windows. 

If you fancy a small donation for karma. BTC Address:
1F697gsLsajQR9kKvqzA5dh2Q23fRs4Z1R
