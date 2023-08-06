import pytest

from tdxpy.exhq import TdxExHq_API
from tdxpy.parser.ext.ex_get_history_minute_time_data import GetHistoryMinuteTimeData


@pytest.mark.skip
def test_ex_get_history_minute_time_data(client):
    api = TdxExHq_API()
    cmd = GetHistoryMinuteTimeData(api)
    cmd.setParams(8, "10000843", 20180811)
    print(cmd.send_pkg)
