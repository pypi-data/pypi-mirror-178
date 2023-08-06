from tdxpy.reader import TdxDailyBarReader


# logger.setLevel(level=logging.DEBUG)


def test_daily_bar_reader(shared_datadir):
    tdx_reader = TdxDailyBarReader(str(shared_datadir / "vipdoc"))

    for row in tdx_reader.get_kline_by_code("000001", "sz"):
        assert row

    assert not tdx_reader.get_df("000001", "sz").empty
