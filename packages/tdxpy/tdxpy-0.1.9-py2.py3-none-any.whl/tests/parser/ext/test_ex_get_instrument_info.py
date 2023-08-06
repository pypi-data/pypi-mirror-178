import pytest

from tdxpy.exhq import TdxExHq_API


@pytest.mark.skip
def test_ex_get_instrument_info():
    api = TdxExHq_API()
    api.connect("121.14.110.210", 7727)
    ret = api.get_instrument_info(200, 100)
    print(ret)
