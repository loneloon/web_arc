import datetime
from patterns.prototypes import ModelMixin
import hashlib


class TrainingSite:

    class Category(ModelMixin):
        __slots__ = 'id', 'name', 'parent', 'description'

        def __init__(self, name, parent=None, description=None):
            self.id = None
            self.name = name
            self.parent = parent
            self.description = description

    class Course(ModelMixin):
        __slots__ = 'id', 'name', 'coursetype_fk', 'category_fk', 'description'

        def __init__(self, name, coursetype_fk, category_fk, description=None):
            self.id = None
            self.name = name
            self.coursetype_fk = coursetype_fk
            self.category_fk = category_fk
            self.description = description

    class Coursetype(ModelMixin):
        __slots__ = 'id', 'name'

        def __init__(self, name):
            self.id = None
            self.name = name

    class User(ModelMixin):
        __slots__ = 'id', 'name', 'password', 'full_name', 'email', 'is_active', 'registration_date', 'is_superuser'

        def __init__(self, name, password, full_name=None, email=None):
            self.id = None
            self.name = name
            self.password = hashlib.md5(password.encode('utf-8')).hexdigest()
            self.full_name = full_name
            self.email = email
            self.is_active = False
            self.registration_date = datetime.datetime.now()
            self.is_superuser = False

    class Usersession(ModelMixin):
        __slots__ = 'id', 'cookie', 'last_login_date', 'user_fk'

        def __init__(self, user_fk, cookie):
            self.id = None
            self.cookie = cookie
            self.last_login_date = datetime.datetime.now()
            self.user_fk = user_fk

    class Student(ModelMixin):
        __slots__ = 'id', 'user_fk', 'course_fk'

        def __init__(self, user_fk, course_fk):
            self.id = None
            self.user_fk = user_fk
            self.course_fk = course_fk

    class Curator(Student):
        pass

    class Teacher(Student):
        pass

    class Comments(ModelMixin):
        __slots__ = 'id', 'name', 'email', 'subject', 'text'

        def __init__(self, name, email, subject, text):
            self.id = None
            self.name = name
            self.email = email
            self.subject = subject
            self.text = text

    @classmethod
    def get_inner_classes(cls):
        return [cls_attribute for cls_attribute in cls.__dict__.values() if type(cls_attribute) is type]
