from tdxpy.constants import TDXParams


def test_get_xdxr_info0(client):
    # 11 扩缩股
    assert client.get_xdxr_info(TDXParams.MARKET_SH, "600381")


def test_get_xdxr_info1(client):
    # 12 非流通股缩股
    assert client.get_xdxr_info(TDXParams.MARKET_SH, "600339")


def test_get_xdxr_info2(client):
    # 13 送认购权证
    assert client.get_xdxr_info(TDXParams.MARKET_SH, "600008")


def test_get_xdxr_info3(client):
    # 14 送认沽权证
    assert client.get_xdxr_info(0, "000932")
