import socket

import settings


class EchoClient():

    def __init__(self):

        # Создаем экземпляр сокет соединения
        self._sock = socket.socket()

        # Связываем сокет соединение с хостом и портом сервера 
        self._sock.connect((settings.HOST, settings.PORT))


    def read(self, sock):

        # Получаем данные с сервера
        bytes_data = self._sock.recv(settings.BUFFER_SIZE)

        # Приводим полученные данные к строковому виду
        str_data = bytes_data.decode(settings.ENCODING)

        # Выводим полученные данные на экран
        print(str_data)


    def write(self):

        # Вводим данные с клавиатуры
        str_data = input('Enter data: ')

        # Приводим отправляемые данные к байтовому виду
        bytes_data = str_data.encode(settings.ENCODING)

        # Отправляем данные на сервер
        self._sock.send(bytes_data)


    def run(self):

        try:

            while True:

                # Вводим данны и отправляем на сервер
                self.write()

                # Получаем ответ сервера
                self.read(self._sock)

        except KeyboardInterrupt:

            # Обрабатываем сочетание клавишь Ctrl+C
            pass


if __name__ == '__main__':

     client = EchoClient()

     client.run()
