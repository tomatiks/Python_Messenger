import json

import pytest

from datetime import datetime

from client import JSONRequest

import settings


@pytest.fixture
def uri():

    return 'localhost:8000/echo'


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
def startline(uri, method):

    return {'uri':uri, 'method':method, 'version':settings.VERSION}


@pytest.fixture
def headers(time, from_client, to_client):

    return {'time':time, 'to':to_client, 'frm':from_client}


@pytest.fixture
def raw_request(startline, headers, body):

    data = {'startline':startline, 'headers':headers, 'body':body}

    str_data = json.dumps(data)

    return str_data.encode(settings.ENCODING)


@pytest.fixture
def request(uri, method, time, to_client, from_client, body):

    return JSONRequest(uri, method, body, time=time, to=to_client, frm=from_client)


def test_add_header(request, from_client):

    request.add_header('from', from_client)

    request_from = request._headers.get('from')

    assert request_from == from_client


def test_remove_header(request, from_client):

    request.remove_header('frm')

    request_from = request._headers.get('from')

    assert not request_from


def test_to_bytes(request, raw_request):

    request_raw = request.to_bytes()

    assert len(request_raw) == len(raw_request)
