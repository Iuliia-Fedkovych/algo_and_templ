class Application:
    def __init__(self, urls, fronts):
        self.urls = urls
        self.fronts = fronts

    def add_route(self, url):
        def inner(view):
            self.urls[url] = view

        return inner

    def parse_input_data(self, data):
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    def get_wsgi_input_data(self, env):
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data):
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']

        if path[-1] != '/':
            path = f"{path}/"
        method = environ['REQUEST_METHOD']
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)

        query_string = environ['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        if path in self.urls:
            view = self.urls[path]
            request = {'method': method, 'data': data, 'request_params': request_params}
            for controller in self.fronts:
                controller(request)
            code, text = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [text.encode('utf-8')]
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b"Not Found"]


class DebugApplication(Application):

    def __init__(self, urls, fronts):
        self.application = Application(urls, fronts)
        super().__init__(urls, fronts)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


class MockApplication(Application):

    def __init__(self, urls, fronts):
        self.application = Application(urls, fronts)
        super().__init__(urls, fronts)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Mock']