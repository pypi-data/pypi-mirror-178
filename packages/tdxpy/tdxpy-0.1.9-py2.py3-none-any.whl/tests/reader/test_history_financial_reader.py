from tdxpy.reader.history_financial_reader import HistoryFinancialReader


def test_history_financial_reader(shared_datadir):
    result = (HistoryFinancialReader().get_df(str(shared_datadir / "gpcw20220630.dat")))
    assert not result.empty, result
