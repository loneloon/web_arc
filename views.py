from core.utils import *
from core.render import page_render as render
from logger.logger_module import Log


@Log()
def index(request, site=None, db=None):
    title = 'Home'
    content = 'Welcome to the main page!'

    res = render('home.html', object_list={'title': title,
                                           'content': content})

    return '200 OK', [res]


@Log()
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


@Log()
def courses(request, site, db=None):
    title = 'Online Courses'
    content = 'Courses will be displayed here...'
    categories = site.all_categories

    res = render('courses.html', object_list={'title': title,
                                              'content': content,
                                              'categories': categories})

    return '200 OK', [res]


@Log()
def category_view(request, site, db=None):

    search_name = request['path'].split('/')
    while '' in search_name:
        search_name.remove('')
    search_name = search_name[1]

    category_obj = None

    for category in site.all_categories:
        if category.name == search_name:
            category_obj = category

    if category_obj is None:
        return bad_request(request)
    else:
        title = category_obj.name

        res = render('inspect.html', object_list={'title': title})

        return "200 OK", [res]


@Log()
def course_view(request, site, db=None):

    search_name = request['path'].split('/')
    while '' in search_name:
        search_name.remove('')
    category_name = search_name[1]
    course_name = search_name[2]

    course_obj = None

    for course in site.all_courses:
        if course.category.name == category_name and course.name == course_name:
            course_obj = course

    if course_obj is None:
        return bad_request(request)
    else:
        title = course_obj.name

        res = render('inspect.html', object_list={'title': title})

        return "200 OK", [res]
