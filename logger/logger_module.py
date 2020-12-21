import datetime
import os
import sys


class Log:

    def __init__(self):
        if not os.path.exists(r"logs"):
            os.mkdir("logs")

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            with open(r"logs/logfile{0}".format(str(datetime.datetime.now())[0:10]), "a+") as lw:
                record = f"[{datetime.datetime.now()}] {func.__class__.__name__} called: {func.__name__} args=({args, kwargs})"
                print(record)
                lw.write(record+'\n')

            return func(*args, **kwargs)
        return wrapper
