import pandas as pd
import pytest

from tdxpy.constants import TDXParams
from tdxpy.exceptions import ValidationException


def test_get_security_quotes0(client):
    result = client.get_security_quotes(TDXParams.MARKET_SH, "600036")
    assert result
    print(result)


def test_get_security_quotes1(client):
    result = client.get_security_quotes((TDXParams.MARKET_SH, "600036"))
    assert result
    print(result)


def test_get_security_quotes2(client):
    result = client.get_security_quotes([(TDXParams.MARKET_SH, "600036"), (TDXParams.MARKET_SH, "600016")])
    assert result
    print(result)


def test_get_security_quotes3(client):
    with pytest.raises(ValidationException):
        client.get_security_quotes()


def test_get_security_quotes4(client):
    result = client.get_security_quotes([(TDXParams.MARKET_SH, "111004"), (TDXParams.MARKET_SZ, "127057")])
    assert result
    print(pd.DataFrame(result)[['code', 'price']])
