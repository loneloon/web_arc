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

    def response(self, request, appendix=None):
        object_list = {'title': self.title,
                       'content': self.content,
                       'path': request['path'],
                       'user': request['user']}

        if appendix is not None:
            object_list.update(appendix)

        if request['next']:
            if request['path'] == signin_link:
                object_list['next'] = request.pop('next')
            elif request['next'] == signin_link:
                return redirect_302(f"{request.pop('next')}?next={request['path']}")
            else:
                return redirect_302(f"{request.pop('next')}")

        res = render(self.template, object_list=object_list)
        return '200 OK', [res]

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
        comments_list = harvest_db_obj(db.get_object(model=site.Comments, all=True))

        object_list = {'title': self.title, 'content': self.content, 'comments': comments_list}

        return self.response(request, object_list)

    def post(self, request, db, site):
        try:
            db.create_object(model=site.Comments,
                             **request['queries'])
            return redirect_302("/{0}/".format(slice_path(request['path'])[0]))
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
                        if obj['parent'] != 0 and obj != obj_list[-1]:
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

    def get_parent(self, db, site, name):
        parent_id = db.get_object(model=site.Category, name=name).parent
        parent = db.get_object(model=site.Category, id=parent_id)
        if parent_id != 0 and parent:
            if int(parent.parent) != 0:
                return self.get_parent(db, site, parent.name)
            else:
                return parent
        else:
            return None

    def fetch_courses(self, db, site, cat_list):
        if cat_list:
            for cat in cat_list:
                try:
                    cat['courses'] = harvest_db_obj(
                        db.get_object(model=site.Course, all=True, category_fk=cat['id'], is_active=True))
                except Exception as e:
                    print(e)
                    cat['courses'] = None
            return cat_list
        else:
            return None

    def get_categories(self, db, site, name=None):
        result = harvest_db_obj(
            db.get_object(model=site.Category, all=True, is_active=True))

        if name is not None:
            try:
                top_id = int(db.get_object(model=site.Category, name=name).id)
                result = list(obj for obj in result if int(obj['id']) >= top_id)
            except Exception as e:
                print(e)
                result = None

        result = self.pack_children(
            self.fetch_courses(
                db, site, result))

        try:
            if name is not None:
                result = list(obj for obj in result if obj['name'] == name)

                parent = self.get_parent(db, site, name)
                if parent is not None:
                    if not parent.is_active:
                        result = []

        except Exception as e:
            print(e)
            result = None
        return result

    def get(self, request, db, site):
        search_name = slice_path(request['path'])[1]

        category = self.get_categories(db, site, name=search_name)

        if category:
            self.title = search_name
            path = '/{0}/'.format(slice_path(request['path'])[0])
            object_list = {'category': category[0], 'path': path}
            return self.response(request, object_list)
        else:
            return bad_request(request)

    def post(self, request, db, site):
        return self.get(request, db, site)


class CategoryCreate(BaseView):

    def __init__(self):
        super().__init__()
        self.title = "Create category"
        self.content = ''
        self.template = 'create_category.html'

    def get(self, request, db, site):

        exclude = ['id', 'is_']

        form = make_form_from_model(site.Category, exclude=exclude)
        categories = db.get_object(model=site.Category, all=True, is_active=True)
        object_list = {'categories': categories, 'form': form}

        return self.response(request, object_list)

    def post(self, request, db, site):

        fields = request['queries']

        try:
            db.create_object(model=site.Category, **fields)
        except Exception as e:
            print(e)
        return redirect_302('/online-courses/')


class CourseCreate(BaseView):

    def __init__(self):
        super().__init__()
        self.title = "Create course"
        self.content = ""
        self.template = 'create_course.html'

    def get(self, request, db, site):

        exclude = ['id', 'is_']

        form = make_form_from_model(site.Course, exclude=exclude)
        categories = db.get_object(model=site.Category, all=True, is_active=True)
        types = db.get_object(model=site.Coursetype, all=True)
        object_list = {'categories': categories, 'types': types, 'form': form}

        return self.response(request, object_list)

    def post(self, request, db, site):

        fields = request['queries']

        try:
            db.create_object(model=site.Course, **fields)
        except Exception as e:
            print(e)
        return redirect_302('/online-courses/')


class Categories(CategoryView):

    def __init__(self):
        super().__init__()
        self.title = "Online Courses: Categories"
        self.content = 'Active categories will be displayed here'
        self.template = 'categories.html'

    def get(self, request, db, site):
        categories_list = self.get_categories(db, site)
        path = '/{0}/'.format(slice_path(request['path'])[0])
        object_list = {'categories': categories_list, 'path': path}

        return self.response(request, object_list)


class Course(BaseView):

    def __init__(self):
        super().__init__()
        self.title = None
        self.content = 'Short description of the course'
        self.template = 'inspect.html'

    @login_required
    def get(self, request, db, site):
        path = slice_path(request['path'])
        parent, name = path[1], path[2]
        try:
            link_is_valid = db.get_object(model=site.Category, name=parent, is_active=True).id == \
                            db.get_object(model=site.Course, name=name, is_active=True).category_fk
            if link_is_valid:
                course = harvest_db_obj(db.get_object(model=site.Course, name=name, is_active=True))
                if course:
                    self.title = name
                    object_list = {'course': course}
                    return self.response(request, object_list)
                else:
                    return bad_request(request)
            else:
                return bad_request(request)
        except Exception as e:
            print(e)
            return bad_request(request)


class SignUp(BaseView):

    def __init__(self):
        super().__init__()
        self.title = "Sign Up"
        self.content = 'This is the sign up page...'
        self.template = 'registration.html'

    def get(self, request, db, site):
        if not request['user']:
            exclude = ['id', 'is_', '_date']

            fields = make_form_from_model(site.User, exclude=exclude)

            object_list = {'path': request['path'], 'form': fields}

            return self.response(request, object_list)
        else:
            return redirect_302('/')

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
            return redirect_302('/')
        else:
            return bad_request(request)


class SignIn(BaseView):

    def __init__(self):
        super().__init__()
        self.title = "Sign In"
        self.content = 'This is the sign up page...'
        self.template = 'login.html'

    def get(self, request, db, site):
        if not request['user']:
            fields = ['login', 'password']

            object_list = {'path': request['path'], 'form': fields}

            return self.response(request, object_list)
        else:
            return redirect_302('/')

    def post(self, request, db, site):
        next_url = None

        if 'next_url' in request['queries']:
            next_url = request['queries'].pop('next_url')

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

            if next_url:
                return redirect_302(next_url)
            else:
                return redirect_302('/')
        else:
            return bad_request(request)


class SignOut(BaseView):

    def get(self, request, db, site):

        result = db.delete_object(model=site.Usersession, cookie=request['cookie'])

        if result:
            return redirect_302('/')
        else:
            return bad_request(request)

    def post(self, request, db, site):
        return self.get(request, db, site)


class AdminView(BaseView):

    def __init__(self):
        super().__init__()
        self.title = "Admin"
        self.content = ''
        self.template = 'admin.html'

    @admin_required
    def get(self, request, db, site):

        page = slice_path(request['path'])

        if len(page) > 1:
            if page[1] == 'users':
                model = site.User
            elif page[1] == 'categories':
                model = site.Category
            elif page[1] == 'courses':
                model = site.Course
            else:
                model = None

            if model is not None:
                self.content = 'A list of entries will be displayed here...'
                items = harvest_db_obj(db.get_object(model=model, all=True))

                exclude = ['password']
                form = make_form_from_model(model=model, exclude=exclude)
                return self.response(request, appendix={'db_items': items, 'form': form})
            else:
                return bad_request(request)
        else:
            self.content = f'<h3>Edit entries:</h3>' \
                           f'<ul>' \
                           f'<li><a href="{request["path"]}users/">Users</a></li>' \
                           f'<li><a href="{request["path"]}categories/">Categories</a></li>' \
                           f'<li><a href="{request["path"]}courses/">Courses</a></li>' \
                           f'</ul>'
            return self.response(request)


    @admin_required
    def post(self, request, db, site):
        orig_path = slice_path(request['path'])[:-1]
        fields = request['queries']

        if len(orig_path) == 2:
            action = slice_path(request['path'])[-1]
        else:
            action = None

        if orig_path[1] == 'users':
            model = site.User
        elif orig_path[1] == 'categories':
            model = site.Category
        elif orig_path[1] == 'courses':
            model = site.Course
        else:
            model = None

        if action == 'save':
            for key, value in fields.items():
                if value == 'True':
                    fields[key] = True
                elif value == 'False':
                    fields[key] = False

            if model:
                instance = db.get_object(model=model, id=fields['id'])

                try:
                    for key, value in fields.items():
                        if "_date" not in key:
                            if instance.__getattribute__(key) != value:
                                instance.__setattr__(key, value)
                except Exception as e:
                    print(e)
                finally:
                    result = db.update_object(instance)

                    if result:
                        print('Object update successful.')
                        return redirect_302('/{0}/{1}/'.format(orig_path[0], orig_path[1]))
                    else:
                        print('Update unsuccessful.')
                        return redirect_302('/{0}/{1}/'.format(orig_path[0], orig_path[1]))
            else:
                return bad_request(request)
        elif action == 'delete':
            print(request['queries'])
            if model:
                result = db.delete_object(model=model, id=fields['id'])
                if result:
                    print('Object deletion successful.')
                    return redirect_302('/{0}/{1}/'.format(orig_path[0], orig_path[1]))
                else:
                    print('Deletion unsuccessful.')
                    return redirect_302('/{0}/{1}/'.format(orig_path[0], orig_path[1]))
            else:
                return bad_request(request)
        else:
            return bad_request(request)


class UserView(BaseView):

    def __init__(self):
        super().__init__()
        self.title = ""
        self.content = ""
        self.template = "user.html"

    @login_required
    def get(self, request, db, site):
        exclude = ['id', 'is_']

        if 'edit' not in slice_path(request['path']):
            exclude.append('password')

        form = make_form_from_model(model=site.User, exclude=exclude)
        user_details = harvest_db_obj(db.get_object(model=site.User,
                                                         name=request['user']['name']))
        return self.response(request, appendix={'user_details': user_details, 'form': form})

    @login_required
    def post(self, request, db, site):
        orig_path = slice_path(request['path'])
        fields = request['queries']

        if 'edit' == orig_path[1]:
            user = db.get_object(model=site.User, name=request['user']['name'])
            if user:
                if 'pass' in orig_path[-1]:
                    user_shell = site.User.init_and_get_attrs(name=fields['name'], password=fields['pass_check'])

                    if user_shell['password'] == user.password:
                        del user_shell

                        if fields['pass1'] != "" and (fields['pass1'] == fields['pass2']):
                            fields['password'] = site.User.init_and_get_attrs(name=fields['name'],
                                                                              password=fields['pass1'])['password']
                        else:
                            print("Passwords don't match!")
                            return redirect_302('/{0}/{1}/{2}/'.format(*orig_path))
                    else:
                        print('Wrong password!')
                        return redirect_302('/{0}/{1}/{2}/'.format(*orig_path))

                    del fields['pass_check']
                    del fields['pass1']
                    del fields['pass2']

            else:
                return bad_request(request)

            try:
                for key, value in fields.items():
                    if "_date" not in key:
                        if user.__getattribute__(key) != value:
                            user.__setattr__(key, value)
            except Exception as e:
                print(e)
            finally:
                result = db.update_object(user)

                if result:
                    print('Object update successful.')
                    return redirect_302('/{0}/'.format(orig_path[0]))
                else:
                    print('Update unsuccessful.')
                    return redirect_302('/{0}/{1}/'.format(orig_path[0], orig_path[1]))
        else:
            return bad_request(request)
