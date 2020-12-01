from core.utils import *
from core.render import page_render as render


def index(request, site=None, db=None):
    title = 'Home'
    content = 'Welcome to the main page!'

    res = render('home.html', object_list={'title': title,
                                           'content': content})

    return '200 OK', [res]


def comments(request, site=None, db=None):
    if request['method'] == 'POST':
        try:
            db.save_comment(request['queries']['name'],
                            request['queries']['email'],
                            request['queries']['subj'],
                            request['queries']['text'])
        except Exception as e:
            print(e)

    title = 'Comments'
    content = 'New comments will appear here...'

    comments = []

    try:
        loaded_comments = db.load_comments()
    except Exception as e:
        print(e)
        loaded_comments = []

    for comment in loaded_comments:
        comments.append({'name': comment[1], 'email': comment[2], 'subj': comment[3], 'text': comment[4]})

    res = render('comments.html', object_list={'title': title,
                                               'content': content,
                                               'comments': comments})

    return '200 OK', [res]


def courses(request, site, db=None):
    title = 'Online Courses'
    content = 'Courses will be displayed here...'
    categories = site.all_categories

    res = render('courses.html', object_list={'title': title,
                                              'content': content,
                                              'categories': categories})

    return '200 OK', [res]


def create_category(request, site, db=None):

    try:
        name = request['queries']['name']
        parent = None
        if 'parent' in request['queries']:
            parent = request['queries']['parent']

        site.create_category(name=name, parent=parent)

        return courses(request, site)
    except Exception as e:
        print(e)
        return bad_request(request)


def create_course(request, site, db=None):

    try:
        type_ = request['queries']['type']
        name = request['queries']['name']
        category = site.get_category_by_id_or_name(id=None, name=request['queries']['category'])

        site.create_course(type_=type_, name=name, category=category)

        return courses(request, site)
    except Exception as e:
        print(e)
        return bad_request(request)