from tdxpy.constants import TDXParams


def test_get_security_count(client):
    data = client.get_security_count(market=TDXParams.MARKET_SH)
    print('')
    print('MARKET_SH', data)
    assert data

    data = client.get_security_count(market=TDXParams.MARKET_SZ)
    print('MARKET_SZ', data)
    assert data
