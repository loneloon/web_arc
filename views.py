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

    def harvest_db_obj(self, db_response):
        result = None
        try:
            if db_response is not None:
                result = list(dict((k, v)
                                   for k, v in obj.__dict__.items()
                                   if not k.startswith('_'))
                              for obj in db_response)
        except Exception as e:
            print(e)
        finally:
            return result

    def response(self, appendix=None):
        object_list = {'title': self.title,
                       'content': self.content}

        if appendix is not None:
            object_list.update(appendix)

        res = render(self.template, object_list=object_list)
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
        comments_list = db.get_object(model=site.Comments)

        objects_list = {'title': self.title, 'content': self.content, 'comments': comments_list}

        return self.response(objects_list)

    def post(self, request, db, site):
        try:
            db.create_object(model=site.Comments,
                             **request['queries'])
            return self.get(request, db, site)
        except Exception as e:
            print(e)
            return bad_request(request)


class Categories(BaseView):

    def __init__(self):
        super().__init__()
        self.title = "Online Courses: Categories"
        self.content = 'Active categories will be displayed here'
        self.template = 'courses.html'

    def pack_children(self, obj_list):
        try:
            if obj_list is not None:
                for obj in obj_list:
                    obj['children'] = []
                    if obj['parent'] is None:
                        obj['parent'] = 0
                obj_list.sort(key=lambda x: x['parent'], reverse=True)

                no_orphans = False

                while not no_orphans:
                    no_orphans = True
                    for obj in obj_list:
                        if obj['parent'] != 0:
                            no_orphans = False
                            for parent in obj_list:
                                if parent['id'] == obj['parent']:
                                    parent['children'].append(obj)
                            del obj_list[obj_list.index(obj)]
                return obj_list
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def fetch_courses(self, db, site, cat_list, cat_id):
        for cat in cat_list:
            cat['courses'] = self.harvest_db_obj(db.get_object(model=site.Course, all=True))

    def get(self, request, db, site):
        categories_list = self.pack_children(self.harvest_db_obj(
            db.get_object(model=site.Category, all=True)))

        object_list = {'categories': categories_list}

        return self.response(object_list)

    def post(self, request, db, site):
        return self.get(request, db, site)


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
