import pytest

from tdxpy.exhq import TdxExHq_API


@pytest.mark.skip
def test_ex_get_transaction_data():
    api = TdxExHq_API()
    with api.connect("121.14.110.210", 7727):
        print(api.to_df(api.get_transaction_data(47, "IFL9")))
        # print(api.to_df(api.get_transaction_data(31, "00020")))
