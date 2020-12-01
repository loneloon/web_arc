class User:

    def __init__(self, name):
        self.name = name


class Trainee(User):
    pass


class Trainer(User):
    pass


class UserMaker:

    roles = {
        'trainer': Trainer,
        'trainee': Trainee
    }
    
    @classmethod
    def create(cls, name, role):
        return cls.roles[role](name)


class Category:

    primary_key = 0

    def __init__(self, name, parent=None):
        self.id = self.__class__.primary_key
        self.__class__.primary_key += 1
        self.name = name
        self.parent = parent
        self.courses = []

    def count_courses(self):
        result = self.courses.__len__()
        return result


class Course:

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class Interactive(Course):
    pass


class Tutorial(Course):
    pass


class CourseMaker:

    types = {
        'interactive': Interactive,
        'tutorial': Tutorial
    }

    def __init__(self, name, category):
        self.name = name
        self.category = category

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class CourseInterface:

    def __init__(self):
        self.all_trainers = []
        self.all_trainees = []
        self.all_categories = []
        self.all_courses = []

    def create_user(self, name, role):
        return UserMaker.create(name, role)

    def create_category(self, name, parent=None):
        result = Category(name, parent)
        self.all_categories.append(result)
        return result

    def create_course(self, type_, name, category):
        result = CourseMaker.create(type_, name, category)
        self.all_courses.append(result)
        return result

    def get_category_by_id_or_name(self, id=None, name=None):

        if name is None:
            for c in self.all_categories:
                if c.id == id:
                    return c
            raise Exception(f"[ERROR]: id={id}. No matching categories!")
        elif id is None:
            for c in self.all_categories:
                if c.name == name:
                    return c
            raise Exception(f"[ERROR]: id={id}. No matching categories!")
        else:
            raise Exception(f"[ERROR]: No search criteria set!")

    def get_course_by_name(self, name):
        for c in self.all_courses:
            if c.name == name:
                return c
        return None



