import re


def parse_queries(data: str):
    result = {}

    if data:
        if '&' in data:
            params = data.split('&')
        else:
            params = data.split('\r\n')
            params.remove('')
        for item in params:
            key, value = item.split('=')
            result[key] = value

    return result


def parse_input_data(data: bytes) -> str:
    if data:
        data_str = data.decode(encoding="utf-8")
        return data_str
    else:
        return ''


def get_input_data(env) -> bytes:
    content_length_data = env.get('CONTENT_LENGTH')

    content_length = int(content_length_data) if content_length_data else 0

    data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
    return data


def add_url(cls, path, view):
    try:
        cls.routes[path] = view
    except Exception as e:
        print(e)


def not_found_404_view(request, site=None, db=None):
    return '404 BAD', [b'404 Page Not Found']


def bad_request(request, site=None, db=None):
    return '404 BAD', [b'404 Bad Request, Buddy']


def re_match_view(path, routes, alt):
    view = alt
    for key, value in routes.items():
        if re.fullmatch(key, path):
            view = value

    return view


def compile_request(environ):
    request = {
        'path': environ['PATH_INFO'],
        'method': environ['REQUEST_METHOD']
    }

    if request['method'] == 'GET':
        request['queries'] = parse_queries(environ['QUERY_STRING'])
    else:
        request['queries'] = parse_queries(parse_input_data(get_input_data(environ)))

    return request
