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
        __slots__ = 'id', 'name', 'type_', 'category_fk', 'description'

        def __init__(self, name, type_, category, description=None):
            self.id = None
            self.name = name
            self.type_ = type_
            self.category_fk = category
            self.description = description

    class User:
        __slots__ = 'id', 'name', 'password', 'last_login_date', 'full_name', 'email'

        def __init__(self, username, password, full_name, email=None):
            self.id = None
            self.name = username
            self.password = password
            self.last_login_date = datetime.datetime.now()
            self.full_name = full_name
            self.email = email

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

