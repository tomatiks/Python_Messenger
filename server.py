from socket import *
import time
import json
import sys
import argparse


def recieve_msg_from_client(msg):
    '''Recieve request from client and handle it'''

    obj = json.JSONDecoder().decode(msg.decode('ascii'))
    if obj.get('action'):
        if obj['action'] == 'presence':
            if 'user' in obj.keys():
                if 'account_name' in obj['user'].keys():
                    print('User {} is still connected'.format(obj['user']['account_name']))
                    return True
    else:
        return False


def create_json_response_msg(number, message=''):
    '''Create json type message from given parameters'''

    obj = {}
    obj['response'] = number
    obj['time'] = time.time()
    if number.startswith(('1', '2')):
        obj['alert'] = message
    elif number.startswith(('4', '5')):
        obj['error'] = message

    return json.JSONEncoder().encode(obj).encode('ascii')


def main(argv):

    server_parser=argparse.ArgumentParser(description="Start server")
    server_parser.add_argument('-p',action='store',type=int,default=7777)
    params=server_parser.parse_args(argv)

    soc = socket()
    soc.bind(('', params.p))
    soc.listen(5)

    while True:
        client,addr=soc.accept()
        print('Получен запрос от %s ' % str(addr))
        request=client.recv(1024)
        if recieve_msg_from_client(request):
            client.send(create_json_response_msg('200','OK'))
        else:
            client.send(create_json_response_msg('400', 'JSON is incorrect'))
        client.close()

if __name__=="__main__":
    main(sys.argv[1:])
