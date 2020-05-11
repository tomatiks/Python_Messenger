from socket import *
import time
import json
import sys
import argparse
import jim.server as jims
import settings
import collections


class Server():

    def __init__(self, port):

        # Создаем список для хранения клиентских соединений
        self._connections = list()

        # Создаем список для хранения клиентских запросов
        self._requests = collections.deque()

        # Создаем экземпляр сокет соединения
        self._sock = socket()

        # Связываем сокет с хостом и портом
        self._sock.bind((settings.HOST, port))

        # Ждем обращений клиентов
        self._sock.listen(settings.NUM_CLIENTS)

        # Отпределяем время ожидания запроса клиента
        self._sock.settimeout(settings.TIMEOUT)


    def connect(self):

        try:

            # Получаем подключение клиента
            client, address = self._sock.accept()

            print('Получен запрос от %s ' % str(address))
            # Сохраняем подключение клиента
            self._connections.append(client)

        except OSError:

            # Обрабатываем timeout сервера
            pass


    def read(self, client):

        try:

            # Получаем данные от клиента
            data = client.recv(settings.BUFFER_SIZE)

            # Если полученные данные не являются пустой строкой
            if data:

                # Приводим полученные данные к строковому виду
                #str_data = data.decode(settings.ENCODING)
                json_data=jims.JSONRequest(data)

                # Сохраняем запрос на сервере
                self._requests.append(json_data)

        except ConnectionResetError:

            # В случае разрыва соединения с клиентом и наличии данного клиента в списке подключений
            if client in self._connections:

                # Удаляем соответствующего клиента из списка подключений
                self._connections.remove(client)


    def write(self, client, request):

        try:

            # Приводим отправляемые данные к байтовому виду
            #bytes_message = request.encode(settings.ENCODING)

            # Отправляем данные на клиент
            client.send(request.to_bytes())

        except (ConnectionResetError, BrokenPipeError):

            # В случае разрыва соединения с клиентом и наличии данного клиента в списке подключений
            if client in self._connections:

                # Удаляем соответствующего клиента из списка подключений
                self._connections.remove(client)

    def mainloop(self):

        try:

            while True:

                # Обрабатываем подключения к серверу
                self.connect()

                for client in self._connections:

                    # Сохраняем запрос клиента к серверу
                    self.read(client)

                    # Если клиентом были отправлены запросы к серверу
                    if self._requests:
                        # Извлекаем первый запрос
                        request = self._requests.popleft()

                        print('{} action with user {} in status {}'.format(request.action, request.user_name, request.user_status))

                        if request.action == 'presence':
                            response = jims.JSONResponse(201)
                        else:
                            response = jims.JSONResponse(400)
                        # Отправляем ответ клиенту
                        self.write(client, response)

        except KeyboardInterrupt:

            # Обрабатываем сочетание клавишь Ctrl+C
            pass


# def recieve_msg_from_client(msg):
#     '''Recieve request from client and handle it'''
#
#     obj = json.JSONDecoder().decode(msg.decode('ascii'))
#     if obj.get('action'):
#         if obj['action'] == 'presence':
#             if 'user' in obj.keys():
#                 if 'account_name' in obj['user'].keys():
#                     print('User {} is still connected'.format(obj['user']['account_name']))
#                     return True
#     else:
#         return False

#
# def create_json_response_msg(number, message=''):
#     '''Create json type message from given parameters'''
#
#     obj = {}
#     obj['response'] = number
#     obj['time'] = time.time()
#     if number.startswith(('1', '2')):
#         obj['alert'] = message
#     elif number.startswith(('4', '5')):
#         obj['error'] = message
#
#     return json.JSONEncoder().encode(obj).encode('ascii')


def main(argv):

    server_parser=argparse.ArgumentParser(description="Start server")
    server_parser.add_argument('-p',action='store',type=int,default=7777)
    params=server_parser.parse_args(argv)

    server = Server(params.p)
    server.mainloop()

if __name__=="__main__":
    main(sys.argv[1:])
