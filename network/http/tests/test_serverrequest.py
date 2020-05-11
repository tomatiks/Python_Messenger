import json

import pytest

from datetime import datetime

from server import JSONRequest

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

    return {'time':time, 'to':to_client, 'from':from_client}


@pytest.fixture
def raw_request(startline, headers, body):

    data = {'startline':startline, 'headers':headers, 'body':body}

    str_data = json.dumps(data)

    return str_data.encode(settings.ENCODING)


@pytest.fixture
def request(raw_request):

    return JSONRequest(raw_request)


def test_uri(request, uri):

    assert request.uri == uri


def test_method(request, method):

    assert request.method == method


def test_headers(request, headers):

    request_headers = dict(request.headers)

    assert len(request_headers) == len(headers)


def test_time(request, time):

    request_headers = dict(request.headers)

    request_time = request_headers.get('time')

    assert request_time == time


def test_from(request, from_client):

    request_headers = dict(request.headers)

    request_from = request_headers.get('from')

    assert request_from == from_client


def test_to(request, to_client):

    request_headers = dict(request.headers)

    request_to = request_headers.get('to')

    assert request_to == to_client


def test_body(request, body):

    assert request.body == body
    