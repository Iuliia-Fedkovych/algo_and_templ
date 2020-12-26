from framework import Application, render
from models import TrainingSite
from logging_mod import Logger, debug


site = TrainingSite()
logger = Logger('main')


def main_view(request):
    # logger.log('Список курсов')
    return '200 OK', render('index.html', objects_list=site.courses)


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
            site.courses.append(course)

        return '200 OK', render('create_course.html', categories=categories)
    else:
        return '200 OK', render('create_course.html', categories=categories)


def create_category(request):
    if request['method'] == 'POST':
        data = request['data']
        print(data)
        name = data['name']

        category = None

        new_category = site.create_category(name, category)
        site.categories.append(new_category)

        return '200 OK', render('create_category.html')
    else:
        categories = site.categories
        return '200 OK', render('create_category.html', categories=categories)


urls = {
    '/': main_view,
    '/create-course/': create_course,
    '/create-category/': create_category,
}


def secret_front(request):
    request['secret_key'] = 'some secret'


front_controllers = [secret_front]

application = Application(urls, front_controllers)
