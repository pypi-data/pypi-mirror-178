import pytest

from tdxpy.exhq import TdxExHq_API


@pytest.mark.skip
def test_ex_get_markets():
    api = TdxExHq_API()
    with api.connect("61.152.107.141", 7727):
        x = api.to_df(api.get_markets())
        assert not x.empty
