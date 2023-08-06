import pandas as pd

from tdxpy.constants import TDXParams


def test_get_history_transaction_data(client):
    data = client.get_history_transaction_data(TDXParams.MARKET_SZ, "000001", 0, 10, 20170209)

    assert data is not None
    assert type(data) is list
    assert len(data) == 10
    print(pd.DataFrame(data))
