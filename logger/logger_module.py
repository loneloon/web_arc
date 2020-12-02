import datetime
import sys


class Log:

    def __init__(self):
        pass

    def __call__(self, func, *args, **kwargs):
        def wrapper(*args, **kwargs):
            print(f"[{datetime.datetime.now()}] ({func.__class__.__name__}: {func.__name__})  ")
            return func(*args, **kwargs)
        return wrapper
