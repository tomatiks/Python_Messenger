from socket import *
import json
import time
import sys
import jim.client as jimc
import settings

class Client():

    def __init__(self, host, port):

        # Создаем экземпляр сокет соединения
        self._sock = socket()

        # Связываем сокет соединение с хостом и портом сервера
        self._sock.connect((host, port))


    def read(self):

        # Получаем данные с сервера
        bytes_data = self._sock.recv(settings.BUFFER_SIZE)

        # Приводим полученные данные к строковому виду
        #str_data = bytes_data.decode(settings.ENCODING)

        response = jimc.JSONResponse(bytes_data)

        # Выводим полученные данные на экран
        print('response %s '% (response.response))

        #print('Response code {} with message {}'.format(response.response, response.alert if response.response < 300 else response.error))


    def write(self):

        # Вводим данные с клавиатуры
        #str_data = input('Enter data: ')

        # Приводим отправляемые данные к байтовому виду
        #bytes_data = str_data.encode(settings.ENCODING)
        presence = jimc.JSONRequest_Presence('Bob')

        # Отправляем данные на сервер
        self._sock.send(presence.to_bytes())


    def run(self):

        try:

            #while True:

            # Вводим данны и отправляем на сервер
            self.write()

            # Получаем ответ сервера
            self.read()

        except KeyboardInterrupt:

            # Обрабатываем сочетание клавишь Ctrl+C
            pass

#
# def create_json_request_msg(action, **kwargs):
#     '''Form json type message'''
#
#     if len(action)>15:
#         raise ValueError('Action must be less than 15 characters')
#     obj={}
#     obj['action']=action
#     obj['time']=time.time()
#     if action=='presence':
#         obj['type'] = 'status'
#         if kwargs.get('account_name'):
#             obj['user']={'account_name' : kwargs.get('account_name'),'status' : 'I\'m here'}
#
#     return json.JSONEncoder().encode(obj).encode('ascii')
#
#
# def recieve_msg_from_server(msg):
#     '''Recieve response from server and take information from it'''
#
#     obj = json.JSONDecoder().decode(msg.decode('ascii'))
#     if obj.get('response'):
#         if obj['response'].startswith(('1', '2')):
#             print('Response: {}'.format(obj.get('alert')))
#             return obj.get('alert')
#         if obj['response'].startswith(('4', '5')):
#             print('Error: {}'.format(obj.get('error')))
#             return obj.get('error')
#     else:
#         print('Response message has broken structure')
#         return False


def main(argv):

    if len(argv)==2:
        client = Client(argv[0], int(argv[1]))
    elif len(argv)==1:
        client = Client(argv[0], 7777)
    elif len(argv)==0:
        print('ip-address is required')
        sys.exit(1)
    else:
        print('too much params')
        sys.exit(1)

    client.run()


if __name__=="__main__":
    main(sys.argv[1:])
