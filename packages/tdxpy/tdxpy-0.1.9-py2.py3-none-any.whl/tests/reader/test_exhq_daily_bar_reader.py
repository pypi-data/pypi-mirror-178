from tdxpy.reader import TdxExHqDailyBarReader


def test_exhq_daily_bar_reader(shared_datadir):
    assert TdxExHqDailyBarReader().parse_data_by_file(str(shared_datadir / "vipdoc" / "ds" / "lday" / "4#CF7D0LAO.day"))
    assert TdxExHqDailyBarReader().parse_data_by_file(str(shared_datadir / "vipdoc" / "ds" / "lday" / "4#CF7D0LLS.day"))
