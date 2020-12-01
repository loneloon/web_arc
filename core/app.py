from core.utils import *
from db_assets.db_model import WebsiteDB
from models import CourseInterface


class WebApp:
    def __init__(self, routes, db_model, db_path, db_tables=None):
        # url-view dictionary
        self.routes = routes

        # app model instance
        self.site = CourseInterface()
        self.db = db_model(db_path, db_tables)

    def __call__(self, environ, start_response):
        request = {}

        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']
        query = environ['QUERY_STRING']

        request['method'] = method
        if method == 'GET':
            request['queries'] = parse_queries(query)
        else:
            request['queries'] = parse_queries(parse_input_data(get_input_data(environ)))

        try:
            view = self.routes[path]
        except:
            view = not_found_404_view

        code, body = view(request=request, site=self.site, db=self.db)

        start_response(code, [('Content-Type', 'text/html')])

        return body

    def add_route(self, url):
        def wrapped(view):
            self.routes[url] = view

        return wrapped
