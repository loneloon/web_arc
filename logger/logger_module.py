import datetime
import os
import sys


class Log:

    def __init__(self):
        if not os.path.exists(r"logs"):
            os.mkdir("logs")

        self.stdout_pipe = open(r"logs/logfile{0}".format(str(datetime.datetime.now())[0:10]), "a+")

    def __call__(self, func, *args, **kwargs):
        def wrapper(*args, **kwargs):
            with open(r"logs/logfile{0}".format(str(datetime.datetime.now())[0:10]), "a+") as lw:
                record = f"[{datetime.datetime.now()}] {func.__class__.__name__} called: {func.__name__} args=({args, kwargs})\n"
                lw.write(record)
            return func(*args, **kwargs)
        return wrapper
