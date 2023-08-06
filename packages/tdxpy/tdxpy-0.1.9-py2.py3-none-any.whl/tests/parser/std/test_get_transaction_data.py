from tdxpy.constants import TDXParams


def test_get_transaction_data(client):
    """
    这个是通达信的行情数据本身就给乘了10倍吗？
    """
    assert client.get_transaction_data(market=TDXParams.MARKET_SH, code='600036', start=0, count=10)
