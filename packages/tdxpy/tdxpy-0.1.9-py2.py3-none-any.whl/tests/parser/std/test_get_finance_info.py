from collections import OrderedDict
from pprint import pprint

from tdxpy.constants import TDXParams


def test_get_finance_info(client):
    data = client.get_finance_info(TDXParams.MARKET_SZ, "000001")

    assert isinstance(data, OrderedDict)
    assert len(data) > 0

    pprint(data)
