import json

import pytest

from datetime import datetime

from server import JSONResponse

import settings


@pytest.fixture
def code():

    return 200


@pytest.fixture
def method():

    return 'GET'


@pytest.fixture
def time():

    dt = datetime.now()

    return dt.strftime('%d/%m/%y')


@pytest.fixture
def from_client():

    return '@fromclientname'


@pytest.fixture
def to_client():

    return '@toclientname'


@pytest.fixture
def body():

    return 'Message body from one client to another'


@pytest.fixture
def startline(code, method):

    return {'code':code, 'method':method, 'version':settings.VERSION}


@pytest.fixture
def headers(time, from_client, to_client):

    return {'time':time, 'to':to_client, 'frm':from_client}


@pytest.fixture
def raw_response(startline, headers, body):

    data = {'startline':startline, 'headers':headers, 'body':body}

    str_data = json.dumps(data)

    return str_data.encode(settings.ENCODING)


@pytest.fixture
def response(code, method, time, to_client, from_client, body):

    return JSONResponse(code, method, body, time=time, to=to_client, frm=from_client)


def test_add_header(response, from_client):

    response.add_header('from', from_client)

    response_from = response._headers.get('from')

    assert response_from == from_client


def test_remove_header(response, from_client):

    response.remove_header('frm')

    response_from = response._headers.get('from')

    assert not response_from


def test_to_bytes(response, raw_response):

    response_raw = response.to_bytes()

    assert len(response_raw) == len(raw_response)

