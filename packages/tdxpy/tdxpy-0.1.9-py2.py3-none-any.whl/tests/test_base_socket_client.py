import pytest

from tdxpy.base_socket_client import BaseSocketClient
from tdxpy.exceptions import ValidationException


@pytest.mark.parametrize('v,empty', [
    (('aaa', 'bbbb'), False),
    (['aaa', 'bbbb'], False),
    ({"adfafd": 'SDFSDF'}, False),
    ('N', False),
    ([], True),
    ({}, True),
    ('', True),
    (0, True),
])
def test_to_df(v, empty):
    result = BaseSocketClient().to_df(v)
    assert result.empty is empty, result


def tests_multithread_or_heartbeat():
    client = BaseSocketClient(multithread=True)
    assert client.lock

    client = BaseSocketClient(heartbeat=True)
    assert client.lock

    client = BaseSocketClient(heartbeat=False, multithread=False)
    assert not client.lock


def test_connect_ip_empty():
    with pytest.raises(ValidationException):
        client = BaseSocketClient(heartbeat=False, multithread=False)
        client.connect()
