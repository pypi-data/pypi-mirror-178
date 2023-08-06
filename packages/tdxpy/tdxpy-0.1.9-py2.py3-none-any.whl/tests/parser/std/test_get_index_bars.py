from pprint import pprint

import pandas as pd

from tdxpy.constants import TDXParams


def test_get_index_bars(client):
    data = client.get_index_bars(category=9, market=TDXParams.MARKET_SH, code='000001', start=0, count=10)

    assert isinstance(data, list)
    assert len(data) == 10

    pprint(pd.DataFrame(data))
