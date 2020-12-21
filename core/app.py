from core.utils import *
from models import CourseInterface
import datetime
import os
import sys


class WebApp:
    def __init__(self, routes, db_model, db_path, db_tables=None):
        # url-view dictionary
        self.routes = routes

        # app model instance
        self.site = CourseInterface()
        self.db = db_model(db_path, db_tables)

        if 'Debug' or 'Fake' not in self.__class__.__name__:
            sys.stdout = open(os.devnull, 'w')

    def __call__(self, environ, start_response):

        request = compile_request(environ)

        view = re_match_view(path=request['path'], routes=self.routes, alt=bad_request)

        code, body = view(request=request, site=self.site, db=self.db)

        start_response(code, [('Content-Type', 'text/html')])

        return body

    def add_route(self, url):
        def wrapped(view):
            self.routes[url] = view

        return wrapped


class DebugApp(WebApp):

    def __call__(self, environ, start_response):
        print('>')

        request = compile_request(environ)

        view = re_match_view(path=request['path'], routes=self.routes, alt=bad_request)

        code, body = view(request=request, site=self.site, db=self.db)

        if "OK" in code:
            color_code = '\033[92m'
        else:
            color_code = '\033[93m'
        end_color_code = '\033[0m'

        print("{0}[{1}]: {2} '{3}' {4}{5}".format(color_code, datetime.datetime.now(), request['method'], request['path'], code, end_color_code))

        start_response(code, [('Content-Type', 'text/html')])

        return body


class FakeApp(WebApp):

    def __call__(self, environ, start_response):

        start_response("200 OK", [('Content-Type', 'text/html')])

        return [b"Hello from Fake"]
