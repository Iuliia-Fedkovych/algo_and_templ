from framework import Application
import views

urls = {
    '/': views.index_view,
    '/about/': views.about_view,
}


def secret_front(request):
    request['secret_key'] = 'some secret'


def urls_handling(request):
    if request['PATH_INFO'][-1] != '/':
        request['PATH_INFO'] = f"{request['PATH_INFO']}/"


front_controllers = [secret_front, urls_handling]

application = Application(urls, front_controllers)
