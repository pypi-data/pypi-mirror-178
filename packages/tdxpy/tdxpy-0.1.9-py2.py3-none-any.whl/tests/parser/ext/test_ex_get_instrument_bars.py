import pytest

from tdxpy.constants import TDXParams
from tdxpy.exhq import TdxExHq_API


@pytest.mark.skip
def test_ex_get_instrument_bars():
    api = TdxExHq_API()
    # cmd = GetInstrumentBars(api)
    # cmd.setParams(4, 7, "10000843", 0, 10)
    # print(cmd.send_pkg)
    with api.connect("61.152.107.141", 7727):
        print(api.to_df(api.get_instrument_bars(TDXParams.KLINE_TYPE_EXHQ_1MIN, 74, "BABA")).tail())
        print(api.to_df(api.get_instrument_bars(TDXParams.KLINE_TYPE_DAILY, 31, "00001")).tail())
