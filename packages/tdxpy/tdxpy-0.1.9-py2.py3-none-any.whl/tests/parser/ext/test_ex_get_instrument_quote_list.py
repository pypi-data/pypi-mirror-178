import pytest

from tdxpy.exhq import TdxExHq_API


@pytest.mark.skip
def test_ex_get_instrument_quote_list():
    api = TdxExHq_API()
    with api.connect("119.97.142.130", 7721):
        # print(api.to_df(api.get_instrument_quote_list(71, 2, 0, 10)))
        print(api.to_df(api.get_instrument_quote_list(29, 3, 0, 10)))
