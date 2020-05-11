import socket

import select

import settings

import collections


class EchoServer():

    def __init__(self):

        # Создаем список для хранения клиентских соединений
        self._connections = list()

        # Создаем список для хранения клиентских запросов
        self._requests = collections.deque()

        # Создаем экземпляр сокет соединения
        self._sock = socket.socket()

        # Связываем сокет соединение с хостом и портом сервера 
        self._sock.bind((settings.HOST, settings.PORT))

        # Ждем обращений клиентов 
        self._sock.listen(settings.CLIENTS_NUM)

        # Отпределяем время ожидания запроса клиента 
        self._sock.settimeout(settings.TIMEOUT)


    def connect(self):

        try:

            # Получаем подключение клиента
            client, address = self._sock.accept()

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
                str_data = data.decode(settings.ENCODING)

                # Сохраняем запрос на сервере
                self._requests.append(str_data)

        except ConnectionResetError:

            # В случае разрыва соединения с клиентом и наличии данного клиента в списке подключений
            if client in self._connections:

                # Удаляем соответствующего клиента из списка подключений
                self._connections.remove(client)


    def write(self, client, request):

        try:

            # Приводим отправляемые данные к байтовому виду
            bytes_message = request.encode(settings.ENCODING)

            # Отправляем данные на клиент
            client.send(bytes_message)

        except (ConnectionResetError, BrokenPipeError):

            # В случае разрыва соединения с клиентом и наличии данного клиента в списке подключений
            if client in self._connections:

                # Удаляем соответствующего клиента из списка подключений
                self._connections.remove(client)


    def mainloop(self):

        try:

            while True:

                print('server wait for clients')

                # Обрабатываем подключения к серверу
                self.connect()

                for client in self._connections:
                
                    # Сохраняем запрос клиента к серверу
                    self.read(client)

                    # Если клиентом были отправлены запросы к серверу
                    if self._requests:

                        # Извлекаем первый запрос
                        request = self._requests.popleft()

                        print(request)

                        # Отправляем запрос слиенту
                        self.write(client, request)

        except KeyboardInterrupt:

            # Обрабатываем сочетание клавишь Ctrl+C
            pass


if __name__ == '__main__':

    server = EchoServer()

    server.mainloop()
