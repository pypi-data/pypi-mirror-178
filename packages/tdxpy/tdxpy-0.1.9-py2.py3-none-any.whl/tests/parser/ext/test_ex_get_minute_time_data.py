import pytest

from tdxpy.exhq import TdxExHq_API


@pytest.mark.skip
def test_ex_get_minute_time_data():
    api = TdxExHq_API()
    with api.connect("61.152.107.141", 7727):
        x = api.to_df(api.get_minute_time_data(74, "BABA", 20170613, 20170620))
        assert not x.empty
