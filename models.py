from reusepatterns.prototypes import PrototypeMixin


class User:
    def __init__(self, name):
        self.name = name


class Tutor(User):
    pass


class Student(User):
    def __init__(self, name):
        self.course = []
        super().__init__(name)


class UserFactory:
    types = {
        'student': Student,
        'tutor': Tutor
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Course(PrototypeMixin):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class WebinarCourse(Course):
    pass


class RecordCourse(Course):
    pass


class PhotoCourse(Course):
    pass


class CourseFactory:
    types = {
        'webinar': WebinarCourse,
        'record': RecordCourse,
        'photo': PhotoCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class TrainingSite:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    def create_user(self, type_, name):
        return UserFactory.create(type_, name)

    def create_category(self, name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    def create_course(self, type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name) -> Course:
        for item in self.courses:
            if item.name == name:
                return item

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item
