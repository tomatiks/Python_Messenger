import json

import jim.settings

import time


# Response-объект - используется для преобразования "сырых" данных (байтов) в python-объект
class JSONResponse():
    # Конструктор в качестве аргументов принимает исключительно "сырые" данные
    # Внутри конструктора "сырые" данные преобразуются в словарь
    def __init__(self, message_bytes):
        message_str = message_bytes.decode(jim.settings.ENCODING)

        self._envelope = json.loads(message_str)



    @property
    def response(self):
        # Read only свойство response
        response = self._envelope.get('response')

        return response

    @property
    def alert(self):
        # Read only свойство alert
        alert = self._envelope.get('alert')

        return alert

    @property
    def error(self):
        # Read only свойство error
        error = self._envelope.get('error')

        return error


# Request-объект - используется для приведения python-объекта в байтовый вид (для генерации "сырых" данных)
class JSONRequest_Presence:
    # Конструктор в качестве аргументов принимает основные данные о запросе
    def __init__(self,  account_name, type=None):
        self._account_name = account_name

        self._time = time.time()

        self._status = "I'm still here"

        self._action = 'presence'

        self._type=type


    # Метод to_bytes - используется для преобразования данных о запросе в байты
    def to_bytes(self):
        envelope = dict()

        envelope.update({'action': self._action})

        envelope.update({'time': self._time})

        if self._type:
            envelope.update({'type': self._type})

        envelope.update({'user': {'account_name': self._account_name, 'status': self._status}})

        data_str = json.dumps(envelope)

        return data_str.encode(jim.settings.ENCODING)

