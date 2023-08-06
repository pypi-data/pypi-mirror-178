from pprint import pprint

import pandas as pd

from tdxpy.constants import TDXParams


def test_get_security_list(client):
    data = client.get_security_list(market=TDXParams.MARKET_SZ, start=0)

    assert data
    assert len(data) > 0

    print('')
    pprint(pd.DataFrame(data))
