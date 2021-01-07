import re

signin_link = '/signin/'


def parse_queries(data: str):
    result = {}

    if data:
        if '&' in data:
            params = data.split('&')
        else:
            params = data.split('\r\n')
            while '' in params:
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


def bad_request(request=None, site=None, db=None):
    return '404 BAD', [b'404 Bad Request, Buddy']


def redirect_302(url):
    return '302', url


def is_logged_in(request, session_model, user_model, db):
    session = db.get_object(model=session_model, cookie=request['cookie'])

    if session:
        user = db.get_object(model=user_model, id=session.user_fk)
        if user:
            return {'name': user.name, 'super': user.is_superuser}
    else:
        return None


def make_form_from_model(model, exclude=None):

    items = []

    try:
        for key in model.__slots__:
            included = True

            if exclude is not None:
                for tag in exclude:
                    if '_' in tag:
                        if tag in key:
                            included = False
                    else:
                        if tag == key:
                            included = False
            if included:
                items.append(key)
    except Exception as e:
        print(e)

    return items


def harvest_db_obj(db_response):
    result = None
    try:
        if db_response is not None:
            if isinstance(db_response, list or tuple):
                result = list(dict((k, v)
                                   for k, v in obj.__dict__.items()
                                   if not k.startswith('_'))
                              for obj in db_response)
            else:
                result = dict((k, v)
                              for k, v in db_response.__dict__.items()
                              if not k.startswith('_'))
        else:
            result = None
    except Exception as e:
        print(e)
    finally:
        return result


def slice_path(source):
    try:
        source = source.split('/')
        while '' in source:
            source.remove('')
        return source
    except Exception as e:
        print(e)
        return []


def re_match_view(path, routes, alt):
    view = alt
    for key, value in routes.items():
        if re.fullmatch(key, path):
            view = value

    return view


def compile_request(environ):
    request = {
        'path': environ['PATH_INFO'],
        'method': environ['REQUEST_METHOD'],
        'cookie': environ['HTTP_COOKIE'].split('=')[-1],
        'next': ""
    }

    if request['method'] == 'GET':
        request['queries'] = parse_queries(environ['QUERY_STRING'])
    else:
        request['queries'] = parse_queries(parse_input_data(get_input_data(environ)))

    if 'next' in request['queries'].keys():
        request['next'] = request['queries'].pop('next')

    return request


def login_required(view):
    def wrapper(*args, **kwargs):
        if 'request' not in kwargs.keys():
            request = args[1]
        else:
            request = kwargs['request']

        if not request['user']:
            request['next'] = signin_link
        return view(*args, **kwargs)
    return wrapper


def admin_required(view):
    def wrapper(*args, **kwargs):
        if 'request' not in kwargs.keys():
            request = args[1]
        else:
            request = kwargs['request']

        if not request['user']:
            request['next'] = signin_link
        else:
            if not request['user']['super']:
                return redirect_302('/')

        return view(*args, **kwargs)
    return wrapper
