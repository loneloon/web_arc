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
            if db_response is not None and isinstance(db_response, list or tuple):
                result = list(dict((k, v)
                                   for k, v in obj.__dict__.items()
                                   if not k.startswith('_'))
                              for obj in db_response)
            elif not isinstance(db_response, list or tuple):
                result = db_response
        except Exception as e:
            print(e)
        finally:
            return result

    def slice_path(self, source):
        try:
            source = source.split('/')
            while '' in source:
                source.remove('')
                return source
        except Exception as e:
            print(e)
            return []

    def response(self, request, appendix=None):
        object_list = {'title': self.title,
                       'content': self.content,
                       'path': request['path'],
                       'user': request['user']}

        if appendix is not None:
            object_list.update(appendix)

        res = render(self.template, object_list=object_list)
        return '200 OK', [res]

    def redirect_302(self, url):
        return '302', url

    def get(self, request, db, site):
        return self.response(request)

    def post(self, request, db, site):
        return self.response(request)


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
        comments_list = self.harvest_db_obj(db.get_object(model=site.Comments, all=True))

        object_list = {'title': self.title, 'content': self.content, 'comments': comments_list}

        return self.response(request, object_list)

    def post(self, request, db, site):
        try:
            db.create_object(model=site.Comments,
                             **request['queries'])
            return self.redirect_302("/{0}/".format(self.slice_path(request['path'])[0]))
        except Exception as e:
            print(e)
            return bad_request(request)


class CategoryView(BaseView):

    def __init__(self):
        super().__init__()
        self.title = None
        self.content = 'Active categories will be displayed here'
        self.template = 'inspect.html'

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
                            obj['parent'] = 0
                return obj_list
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def fetch_courses(self, db, site, cat_list):
        if cat_list:
            for cat in cat_list:
                try:
                    cat['courses'] = self.harvest_db_obj(
                        db.get_object(model=site.Course, all=True, category_fk=cat['id']))
                except Exception as e:
                    print(e)
                    cat['courses'] = None
            return cat_list
        else:
            return None

    def get_categories(self, db, site, name=None):
        result = self.harvest_db_obj(
            db.get_object(model=site.Category, all=True))
        if name is not None:
            top_id = int(db.get_object(model=site.Category, name=name).id)
            result = list(obj for obj in result if int(obj['id']) >= top_id)
            print(result)

        result = self.pack_children(
            self.fetch_courses(
                db, site, result))

        try:
            if name is not None:
                result = list(obj for obj in result if obj['name'] == name)
        except Exception as e:
            print(e)
            result = None
        return result

    def get(self, request, db, site):
        search_name = self.slice_path(request['path'])[1]

        category = self.get_categories(db, site, name=search_name)

        if category:
            self.title = search_name
            path = '/{0}/'.format(self.slice_path(request['path'])[0])
            object_list = {'category': category[0], 'path': path}
            return self.response(request, object_list)
        else:
            return bad_request(request)

    def post(self, request, db, site):
        return self.get(request, db, site)


class Categories(CategoryView):

    def __init__(self):
        super().__init__()
        self.title = "Online Courses: Categories"
        self.content = 'Active categories will be displayed here'
        self.template = 'categories.html'

    def get(self, request, db, site):
        categories_list = self.get_categories(db, site)
        path = '/{0}/'.format(self.slice_path(request['path'])[0])
        object_list = {'categories': categories_list, 'path': path}

        return self.response(request, object_list)


class Course(BaseView):

    def __init__(self):
        super().__init__()
        self.title = None
        self.content = 'Short description of the course'
        self.template = 'inspect.html'

    def get(self, request, db, site):
        path = self.slice_path(request['path'])
        parent, name = path[1], path[2]
        link_is_valid = db.get_object(model=site.Category, name=parent).id == \
                        db.get_object(model=site.Course, name=name).category_fk
        if link_is_valid:
            course = self.harvest_db_obj(db.get_object(model=site.Course, name=name))
            if course:
                self.title = name
                object_list = {'course': course}
                return self.response(request, object_list)
            else:
                return bad_request(request)
        else:
            return bad_request(request)


class SignUp(BaseView):

    def __init__(self):
        super().__init__()
        self.title = "Sign Up"
        self.content = 'This is the sign up page...'
        self.template = 'registration.html'

    def get(self, request, db, site):

        fields = []
        exclude = ('id', 'is_active', 'registration_date', 'is_superuser')

        for field in site.User.__slots__:
            if field not in exclude:
                fields.append(field)

        object_list = {'path': request['path'], 'form': fields}

        return self.response(request, object_list)

    def post(self, request, db, site):

        fields = request['queries']

        if fields['password1'] == fields['password2']:
            fields['password'] = fields.pop('password1')
            del fields['password2']

            user = site.User.init_and_get_attrs(**fields)
            try:
                db.create_object(model=site.User, **user)
            except Exception as e:
                print(e)
            return self.redirect_302('/')
        else:
            return bad_request(request)


class SignIn(BaseView):

    def __init__(self):
        super().__init__()
        self.title = "Sign Up"
        self.content = 'This is the sign up page...'
        self.template = 'login.html'

    def get(self, request, db, site):

        fields = ['login', 'password']

        object_list = {'path': request['path'], 'form': fields}

        return self.response(request, object_list)

    def post(self, request, db, site):

        fields = request['queries']
        fields['name'] = fields.pop('login')
        csrf_token = request['cookie']

        user_input = site.User.init_and_get_attrs(**fields)
        user = db.get_object(model=site.User, name=user_input['name'])

        if user_input['password'] == user.password:

            user_session = site.Usersession.init_and_get_attrs(user_fk=user.id, cookie=csrf_token)

            current_session = db.get_object(model=site.Usersession, cookie=csrf_token)
            if not current_session:
                try:
                    db.create_object(model=site.Usersession, **user_session)
                except Exception as e:
                    print(e)

            return self.redirect_302('/')
        else:
            return bad_request(request)


class SignOut(BaseView):

    def get(self, request, db, site):

        result = db.delete_object(model=site.Usersession, cookie=request['cookie'])

        if result:
            return self.redirect_302('/')
        else:
            return bad_request(request)

    def post(self, request, db, site):
        return self.get(request, db, site)
