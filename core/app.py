from core.utils import *
import datetime
import os
import sys


class WebApp:
    def __init__(self, routes, db_module=None, db_path=None, models=None):
        # url-view dictionary
        self.routes = routes

        self.db = db_module(db_path, models)
        self.site = models

        if 'Debug' not in self.__class__.__name__:
            sys.stdout = open(os.devnull, 'w')

    def __call__(self, environ, start_response):

        request = compile_request(environ)

        view = re_match_view(path=request['path'], routes=self.routes, alt=bad_request)

        code, body = view(request=request, db=self.db, site=self.site)

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

        code, body = view(request=request, db=self.db, site=self.site)

        if "OK" in code:
            color_code = '\033[92m'
        else:
            color_code = '\033[93m'
        end_color_code = '\033[0m'

        print("{0}[{1}]: {2} '{3}' {4}{5}".format(color_code,
                                                  datetime.datetime.now(),
                                                  request['method'],
                                                  request['path'],
                                                  code,
                                                  end_color_code))

        start_response(code, [('Content-Type', 'text/html')])

        return body


class FakeApp(WebApp):

    def __call__(self, environ, start_response):

        start_response("200 OK", [('Content-Type', 'text/html')])

        return [b"Hello from Fake"]
