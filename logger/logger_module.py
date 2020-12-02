import datetime


class Log:

    def __init__(self):
        pass

    def __call__(self, func, *args, **kwargs):
        def wrapper(_args, _kwargs):
            print(f"[{datetime.datetime.now()}] ({func.__class__.__name__}: {func.__name__})  ")
            return func(_args, _kwargs)
        return wrapper
