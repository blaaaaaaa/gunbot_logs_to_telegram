from telegram.ext import Updater
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers.polling import PollingObserver as Observer
from telegram.ext import CommandHandler
import time
import logging
import Queue
import sys


telegram_bot_token = "ur_token_here"
folder_to_watch = "C:\Example\Folder\Here\GUNBOT_V...."


class MyHandler(PatternMatchingEventHandler):
    def __init__(self,queue):
        super(MyHandler, self).__init__()
        self.queue = queue
    patterns = ["*-trades.txt"]

    def process(self, event):
        if event.is_directory is False and event.event_type in ["modified","created","moved"]:
            print("Event in %s detected" % event.src_path)
            #line = subprocess.check_output(['tail', '-1', event.src_path])
            #print(line)
            with open(event.src_path, 'r') as f:
                lines = f.read().splitlines()
                last_line = lines[-1]
                self.queue.put(last_line)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


def watch_folder(folder,queue):
    observer = Observer()
    observer.schedule(MyHandler(queue), path=folder, recursive=True)
    observer.start()
    try:
        while True:
            observer.join()
            time.sleep(1)
    except:
        pass


def start(bot, update):
    global queue
    while True:
        message = queue.get()
        bot.send_message(chat_id=update.message.chat_id, text=message)


def main():
    global queue
    queue = Queue.Queue()
    updater = Updater(token=telegram_bot_token)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()
    watch_folder(folder_to_watch, queue)


if __name__ == "__main__":
    main()