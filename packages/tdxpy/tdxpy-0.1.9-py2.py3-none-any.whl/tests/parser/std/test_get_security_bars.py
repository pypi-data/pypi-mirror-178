import pandas as pd

from tdxpy.constants import TDXParams


def test_get_security_bars0(client):
    data = client.get_security_bars(9, 0, "000001", 4, 3)

    assert data, data
    assert type(data) is list
    assert len(data) == 3


def test_get_security_bars1(client):
    result = client.get_security_bars(9, 0, "184801", 4, 3)
    assert result
    print(result)
    print(pd.DataFrame(result))
