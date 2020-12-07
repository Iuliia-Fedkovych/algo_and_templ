from framework import Application
import views

urls = {
    '/': views.index_view,
    '/about/': views.about_view,
}


def secret_front(request):
    request['secret_key'] = 'some secret'


front_controllers = [secret_front]

application = Application(urls, front_controllers)