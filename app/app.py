import falcon

class PersonalDetailsResource():

    def on_get(self, request, response):
        response.status = '200 OK'
        response.set_header('Content-Type', 'text/plain')
        response.body = (
            'name: Honza\n'
            'surname: Javorek\n'
            'Socks_size: 42\n'
        )
