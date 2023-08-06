from pprint import pprint

import pandas as pd

from tdxpy.constants import TDXParams


def test_get_history_minute_time_data(client):
    data = client.get_history_minute_time_data(market=TDXParams.MARKET_SH, code="600300", date='20161209')

    assert type(data) is list
    assert len(data) > 0

    pprint(pd.DataFrame(data))
