from pprint import pprint

import pandas as pd

from tdxpy.constants import TDXParams


def test_get_minute_time_data(client):
    """
    这个是通达信的行情数据本身就给乘了10倍吗？
    """
    data = client.get_minute_time_data(market=TDXParams.MARKET_SH, code='600036')
    assert data
    assert len(data)
    pprint(pd.DataFrame(data))
