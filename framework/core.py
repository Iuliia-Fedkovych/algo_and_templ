class Application:
    def __init__(self, urls, fronts):
        self.urls = urls
        self.fronts = fronts

    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        if path in self.urls:
            view = self.urls[path]
            request = {}
            for controller in self.fronts:
                controller(request)
            code, text = view(request)
            start_response(code, [('Contrnt-Type', 'text/html')])
            return [text.encode('utf-8')]
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b"Not Found"]
