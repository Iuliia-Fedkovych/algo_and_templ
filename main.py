from framework import Application, render, MockApplication, DebugApplication, ListView, CreateView
from models import TrainingSite, EmailNotifier, SmsNotifier
from logging_mod import Logger, debug



site = TrainingSite()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


def main_view(request):
    return '200 OK', render('index.html', objects_list=site.categories)


@debug
def create_course(request):
    categories = site.categories
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        print(category_id)
        if category_id:
            category = site.find_category_by_id(int(category_id))

            course = site.create_course('record', name, category)
            course.observers.append(email_notifier)
            course.observers.append(sms_notifier)
            site.courses.append(course)

        return '200 OK', render('create_course.html', categories=categories)
    else:
        return '200 OK', render('create_course.html', categories=categories)


class CategoryCreateView(CreateView):
    template_name = 'create_category.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['categories'] = site.categories
        return context

    def create_obj(self, data: dict):
        name = data['name']
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.append(new_category)


# def create_category(request):
#     categories = site.categories
#     if request['method'] == 'POST':
#         data = request['data']
#         print(data)
#         name = data['name']
#         category_id = data.get('category_id')
#
#         category = None
#         if category_id:
#             category = site.find_category_by_id(int(category_id))
#
#         new_category = site.create_category(name, category)
#         site.categories.append(new_category)
#
#         return '200 OK', render('create_category.html', categories=categories)
#     else:
#         return '200 OK', render('create_category.html', categories=categories)


class CourseListView(ListView):
    queryset = site.courses
    template_name = 'course_list.html'


class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'


class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course = site.get_course(course_name)
        student_name = data['student_name']
        student = site.get_student(student_name)
        course.add_student(student)


urls = {
    '/': main_view,
    '/create-course/': create_course,
    '/create-category/': CategoryCreateView(),
    '/course-list/': CourseListView(),
    '/create-student/': StudentCreateView(),
    '/student-list/': StudentListView(),
    '/add-student/': AddStudentByCourseCreateView()
}


def secret_front(request):
    request['secret_key'] = 'some secret'


front_controllers = [secret_front]

application = Application(urls, front_controllers)


# @application.add_route('/course-list/')
# def category_list(request):
#     logger.log('Список курсов')
#     return '200 OK', render('course_list.html', objects_list=site.courses)
