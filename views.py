from framework import render


def index_view(request):
    secret_key = request.get('secret_key', None)
    return '200 OK', render('index.html', secret=secret_key)


def about_view(request):
    return '200 OK', render('about.html')
