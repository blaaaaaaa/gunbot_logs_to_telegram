from watchdog.events import PatternMatchingEventHandler
from watchdog.observers.polling import PollingObserver as Observer
import time
import Queue
import telegram
import threading
import os

telegram_bot_token = ""  # put in the bot id
telegram_your_id = ""  # put in your chat id
folder_to_watch = "C:\Users\Jens\Desktop"  # Your GUNBOT Folder or parent folder from multiple GUNBOTS e.g "C:\Users\Jens\Desktop\GUNBOT_3"  ; leave blank for directory where this file is.

if folder_to_watch == "":
    folder_to_watch = os.path.dirname(os.path.abspath(__file__))


class MyHandler(PatternMatchingEventHandler):
    def __init__(self, queue):
        super(MyHandler, self).__init__()
        self.queue = queue

    patterns = ["*-log.txt"]

    def process(self, event):
        if event.is_directory is False and event.event_type in ["modified", "created", "moved"]:
            print("Event in %s detected" % event.src_path)
            # line = subprocess.check_output(['tail', '-1', event.src_path])
            # print(line)
            with open(event.src_path, 'r') as f:
                last_lines = tail(f)
                for line in last_lines:
                    if "MARKET CALLBACK" in line:
                        data = get_attributes_from_logfilename(event.src_path)
                        self.queue.put((line, data))

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


def watch_folder(folder, queue):
    observer = Observer()
    observer.schedule(MyHandler(queue), path=folder, recursive=True)
    observer.start()
    try:
        while True:
            observer.join()
            time.sleep(1)
    except:
        pass


def bot_message_loop(bot, telegram_your_id):
    global queue
    messages_so_far = set()
    bot.send_message(chat_id=telegram_your_id, text="Bot started now!")
    while True:
        message, data = queue.get()
        if message not in messages_so_far:
            messages_so_far.add(message)
            print("Sending message %s" % message + "\nEstimate Total: %s %s\nExchange: %s" % (
                str(message_to_total_estimate(message)), data["primary_pair"], data["exchange"]))
            bot.send_message(chat_id=telegram_your_id, text=message + "\nEstimate Total: %s %s\nExchange: %s" % (
                str(message_to_total_estimate(message)), data["primary_pair"], data["exchange"]))


def tail(f, window=20):
    """
    Returns the last `window` lines of file `f` as a list.
    """
    if window == 0:
        return []
    BUFSIZ = 1024
    f.seek(0, 2)
    bytes = f.tell()
    size = window + 1
    block = -1
    data = []
    while size > 0 and bytes > 0:
        if bytes - BUFSIZ > 0:
            # Seek back one whole BUFSIZ
            f.seek(block * BUFSIZ, 2)
            # read BUFFER
            data.insert(0, f.read(BUFSIZ))
        else:
            # file too small, start from begining
            f.seek(0, 0)
            # only read what was not read
            data.insert(0, f.read(bytes))
        linesFound = data[0].count('\n')
        size -= linesFound
        bytes -= BUFSIZ
        block -= 1
    return ''.join(data).splitlines()[-window:]


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def message_to_total_estimate(message):
    words = message.split()
    counter = 0
    result = 1
    for word in words:
        if isfloat(word) is True:
            counter += 1
            result = result * float(word)
    if counter == 2:
        return result
    else:
        return -1


def get_attributes_from_logfilename(path):
    filename = os.path.basename(path)
    data = dict()
    data["primary_pair"] = ""
    data["secondary_pair"] = ""
    data["exchange"] = ""
    split_list = filename.split("-")
    if len(split_list) < 2:
        return data
    split_pairs = split_list[1].split("_")
    if split_pairs < 1:
        return data
    data["primary_pair"] = split_pairs[0]
    data["secondary_pair"] = split_pairs[1]
    data["exchange"] = split_list[0]
    return data


def main():
    global queue
    queue = Queue.Queue()
    bot = telegram.Bot(token=telegram_bot_token)
    message_thread = threading.Thread(target=bot_message_loop,
                                      kwargs={"bot": bot, "telegram_your_id": telegram_your_id})
    message_thread.start()
    watch_folder(folder_to_watch, queue)


if __name__ == "__main__":
    main()
