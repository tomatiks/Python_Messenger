import json

import settings


class JSONResponse():

    def __init__(self, message_bytes):

        message_str = message_bytes.decode(settings.ENCODING)

        self._envelope = json.loads(message_str)

        self._startline = self._envelope.get('startline')


    @property
    def code(self):

        code = self._startline.get('code')

        return code


    @property
    def method(self):

        method = self._startline.get('method')

        return method


    @property
    def headers(self):

        headers = self._envelope.get('headers')

        for key, value in headers.items():

            yield key, value


    @property
    def body(self):

        body = self._envelope.get('body')

        return body


class JSONRequest():

    def __init__(self, url, method, body, **headers):

        self._headers = headers

        self._url = url

        self._method = method

        self._body = body


    def add_header(self, key, value):

        self._headers.update({key:value})


    def remove_header(self, key):

        del self._headers[key]


    def to_bytes(self):

        envelope = dict()

        start_line = dict()

        start_line.update({'url':self._url})

        start_line.update({'method':self._method})

        start_line.update({'version':settings.VERSION})

        envelope.update({'startline':start_line})

        envelope.update({'headers':self._headers})

        envelope.update({'bydy':self._body})

        data_str = json.dumps(envelope)

        return data_str.encode(settings.ENCODING)
        

data = socket.read()

response = JSONResponse(data)

response['code']

response.get('uri')