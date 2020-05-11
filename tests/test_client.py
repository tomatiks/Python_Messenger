import pytest
import client
import json


def test_json_request_not_none():
    assert client.create_json_request_msg('tt') != None


def test_json_request_presence():
    msg=client.create_json_request_msg('presence', account_name='Bob')
    assert list(json.JSONDecoder().decode(msg.decode('ascii')).keys()) == ['action','time','type','user']


def test_json_request_without_user():
    msg=client.create_json_request_msg('presence')
    assert list(json.JSONDecoder().decode(msg.decode('ascii')).keys()) == ['action','time','type']



def test_json_requestt_more_than_15_char():
    with pytest.raises(ValueError):
        client.create_json_request_msg('ttdhdhsdhdshsdhhdsdhs')


def test_recieve_msg_error():
    with pytest.raises(AttributeError):
        client.recieve_msg_from_server('tt')


response_200=b'{"response": "200", "time": 1527331796.8094459, "alert": "OK"}'
response_400=b'{"response": "400", "time": 1527331796.8094459, "error": "OK"}'
response_300=b'{"response": "300", "time": 1527331796.8094459, "alert": "OK"}'
incorrect_msg=b'{"resp": "200", "time": 1527331796.8094459, "alert": "OK"}'


def test_recieve_msg_not_response():
    assert client.recieve_msg_from_server(incorrect_msg) == False


def test_recieve_msg_300_None():
    assert client.recieve_msg_from_server(response_300) == None


def test_recieve_msg_200_has_alert():
    assert client.recieve_msg_from_server(response_200)


def test_recieve_msg_400_has_error():
    assert client.recieve_msg_from_server(response_400)
