import pytest
import server
import json


def test_json_response_300_not_full():
    msg = server.create_json_response_msg('300')
    assert list(json.JSONDecoder().decode(msg.decode('ascii')).keys()) == ['response', 'time']


def test_json_response_200_has_alert():
    msg = server.create_json_response_msg('200')
    assert list(json.JSONDecoder().decode(msg.decode('ascii')).keys()) == ['response', 'time', 'alert']


def test_json_response_400_has_error():
    msg = server.create_json_response_msg('400')
    assert list(json.JSONDecoder().decode(msg.decode('ascii')).keys()) == ['response', 'time', 'error']


wrong_request_without_action=b'{"acrr": "200", "time": 1527331796.8094459}'
wrong_request_with_action=b'{"action": "200", "time": 1527331796.8094459, "alert": "OK"}'
right_request=b'{"action": "presence", "time": 1527331796.8094459, "user": {"account_name" : "Bob" }}'


def test_msg_from_client_without_action():
    assert server.recieve_msg_from_client(wrong_request_without_action) == False


def test_msg_from_client_with_action():
    assert server.recieve_msg_from_client(wrong_request_with_action) == None


def test_msg_from_client_right():
    assert server.recieve_msg_from_client(right_request)