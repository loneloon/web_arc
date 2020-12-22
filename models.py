import datetime


class TrainingSite:

    class Category:
        __slots__ = 'id', 'name', 'parent', 'description'

        def __init__(self, name, parent=None, description=None):
            self.id = None
            self.name = name
            self.parent = parent
            self.description = description

    class Course:
        __slots__ = 'id', 'name', 'coursetype_fk', 'category_fk', 'description'

        def __init__(self, name, coursetype_fk, category_fk, description=None):
            self.id = None
            self.name = name
            self.coursetype_fk = coursetype_fk
            self.category_fk = category_fk
            self.description = description

    class Coursetype:
        __slots__ = 'id', 'name'

        def __init__(self, name):
            self.id = None
            self.name = name

    class User:
        __slots__ = 'id', 'name', 'password', 'last_login_date', 'full_name', 'email', 'is_active'

        def __init__(self, username, password, full_name, email=None):
            self.id = None
            self.name = username
            self.password = password
            self.last_login_date = datetime.datetime.now()
            self.full_name = full_name
            self.email = email
            self.is_active = None

    class Student:
        __slots__ = 'id', 'user_fk', 'course_fk'

        def __init__(self, user, course):
            self.id = None
            self.user_fk = user
            self.course_fk = course

    class Curator(Student):
        pass

    class Teacher(Student):
        pass

    @classmethod
    def get_inner_classes(cls):
        return [cls_attribute for cls_attribute in cls.__dict__.values() if type(cls_attribute) is type]

