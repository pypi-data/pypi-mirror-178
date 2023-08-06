import pytest

from tdxpy.exhq import TdxExHq_API


@pytest.mark.skip
def test_ex_get_instrument_quote():
    api = TdxExHq_API()
    with api.connect("61.152.107.141", 7727):
        print(api.to_df(api.get_instrument_quote(47, "IF1709")))
