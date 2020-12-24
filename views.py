from core.utils import *
from core.render import page_render as render
from logger.logger_module import Log


class BaseView:
    __slots__ = 'title', 'content', 'template'

    @classmethod
    @Log()
    def view(cls, request, db=None, site=None):
        if request['method'] == 'GET':
            return cls().get(request, db, site)
        else:
            return cls().post(request, db, site)

    def response(self, template=None, object_list=None):
        if template is None:
            template = self.template

        if object_list is None:
            object_list = {'title': self.title,
                           'content': self.content}

        res = render(template, object_list=object_list)
        return '200 OK', [res]

    def get(self, request, db, site):
        return self.response()

    def post(self, request, db, site):
        return self.response()


class Index(BaseView):

    def __init__(self):
        super().__init__()
        self.title = 'Home'
        self.content = 'Welcome to the main page!'
        self.template = 'home.html'


class Comments(BaseView):

    def __init__(self):
        super().__init__()
        self.title = "Comments"
        self.content = 'New comments will appear here...'
        self.template = 'comments.html'

    def get(self, request, db, site):
        comments_list = db.get_object(model=Comments, all=True)

        objects_list = {'title': self.title, 'content': self.content, 'comments': comments_list}

        return self.response(self.template, objects_list)

    def post(self, request, db, site):
        try:
            db.create_object(model=site.Comments,
                             **request['queries'])
            return self.get(request, db, site)
        except Exception as e:
            print(e)
            return bad_request(request)


class Categories:

    def __init__(self):
        super().__init__()
        self.title = "Online Courses: Categories"
        self.content = 'Active categories will be displayed here'
        self.template = 'courses.html'


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
