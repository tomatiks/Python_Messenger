from socket import *
import json
import time
import sys


def create_json_request_msg(action, **kwargs):
    '''Form json type message'''

    if len(action)>15:
        raise ValueError('Action must be less than 15 characters')
    obj={}
    obj['action']=action
    obj['time']=time.time()
    if action=='presence':
        obj['type'] = 'status'
        if kwargs.get('account_name'):
            obj['user']={'account_name' : kwargs.get('account_name'),'status' : 'I\'m here'}

    return json.JSONEncoder().encode(obj).encode('ascii')


def recieve_msg_from_server(msg):
    '''Recieve response from server and take information from it'''

    obj = json.JSONDecoder().decode(msg.decode('ascii'))
    if obj.get('response'):
        if obj['response'].startswith(('1', '2')):
            print('Response: {}'.format(obj.get('alert')))
            return obj.get('alert')
        if obj['response'].startswith(('4', '5')):
            print('Error: {}'.format(obj.get('error')))
            return obj.get('error')
    else:
        print('Response message has broken structure')
        return False


def main(argv):

    soc=socket()

    if len(argv)==2:
        soc.connect((argv[0], int(argv[1])))
    elif len(argv)==1:
        soc.connect((argv[0], 7777))
    elif len(argv)==0:
        print('ip-address is required')
        sys.exit(1)
    else:
        print('too much params')
        sys.exit(1)

    msg=create_json_request_msg('presence', account_name='Bob')
    soc.send(msg)
    response=soc.recv(1024)
    recieve_msg_from_server(response)
    soc.close()

if __name__=="__main__":
    main(sys.argv[1:])
