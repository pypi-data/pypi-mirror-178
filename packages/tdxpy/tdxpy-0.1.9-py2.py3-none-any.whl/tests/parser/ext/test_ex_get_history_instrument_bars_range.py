import pytest

from tdxpy.exhq import TdxExHq_API


# 00000000  01 01 08 6A 01 01 16 00  16 00 FF 23 2F 49 46 4C   ...j.... ...#/IFL
# 00000010  30 00 F0 F4 94 13 07 00  01 00 00 00 00 00 F0 00   0....... ........

# 00000000: 01 01 08 6A 01 01 16 00  16 00 FF 23 4A 4E 56 44  ...j.......#JNVD
# 00000010: 41 00 C0 EC A3 13 07 00  01 00 00 00 00 00 C0 03  A...............

# 00000000  01 01 08 6A 01 01 16 00  16 00 FF 23 2F 49 46 31   ...j.... ...#/IF1
# 00000010  37 30 39 00 94 13 07 00  01 00 00 00 00 00 F0 00   709..... ........
@pytest.mark.skip
def test_ex_get_history_instrument_bars_range():
    api = TdxExHq_API()
    with api.connect("61.152.107.141", 7727):
        x = api.to_df(api.get_history_instrument_bars_range(74, "BABA", 20170613, 20170620))
        assert not x.empty
