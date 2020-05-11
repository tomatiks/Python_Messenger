import json

import jim.settings

import time


# Request-объект - используется для преобразования "сырых" данных (байтов) в python-объект
class JSONRequest():

    # Конструктор в качестве аргументов принимает исключительно "сырые" данные
    # Внутри конструктора "сырые" данные преобразуются в словарь
    def __init__(self, message_bytes):

        message_str = message_bytes.decode(jim.settings.ENCODING)

        self._envelope = json.loads(message_str)


    @property
    def action(self):

        # Read only свойство action
        action = self._envelope.get('action')

        return action



    @property
    def user_name(self):

        # Read only свойство user_name
        user_name=self._envelope.get('user').get('account_name')

        return user_name

    @property
    def user_status(self):

        # Read only свойство user_status
        user_status = self._envelope.get('user').get('status')

        return user_status


# Response-объект - используется для приведения python-объекта в байтовый вид (для генерации "сырых" данных)
class JSONResponse():

    # Конструктор в качестве аргументов принимает основные данные об ответе сервера
    def __init__(self, code):

        self._code = code

        self._time = time.time()

        if code == 100:
            self._msg = 'Basic notification'
        elif code == 200:
            self._msg = 'OK'
        elif code == 201:
            self._msg = 'Created'
        elif code == 202:
            self._msg = 'Accepted'
        elif code == 400:
            self._msg = 'Wrong JSON object'
        elif code == 401:
            self._msg = 'Not Authorized'
        elif code == 404:
            self._msg = 'Not found'
        elif code == 500:
            self._msg = 'Problems on server'


    # Метод to_bytes - используется для преобразования данных об ответе сервера в байты
    def to_bytes(self):

        envelope = dict()

        envelope.update({'code':self._code})

        envelope.update({'time': self._time})

        if self._code < 300:

            envelope.update({'alert': self._msg})
        else:

            envelope.update({'error': self._msg})

        data_str = json.dumps(envelope)

        return data_str.encode(jim.settings.ENCODING)
