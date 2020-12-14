from framework import render


def index_view(request):
    secret_key = request.get('secret_key', None)
    return '200 OK', render('index.html', secret=secret_key)


def about_view(request):
    return '200 OK', render('about.html')


def contact_view(request):
    if request['method'] == 'POST':
        data = request['data']
        title = data['title']
        content = data['content']
        email = data['email']
        with open("message.txt", 'w', encoding='utf-8') as f:
            f.write(f'You get e-mail from {email}, with title "{title}" and content {content}')
        return '200 OK', render('contact.html')
    else:
        return '200 OK', render('contact.html')
