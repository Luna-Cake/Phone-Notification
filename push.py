from notify_run import Notify
notify = Notify()

PUSH_CHANNEL = 'https://notify.run/jZbKmSjkEA0b7lQt'

def push(message):
    notify.send(message, PUSH_CHANNEL)