import pytest

from tdxpy.reader import TdxMinBarReader


@pytest.mark.skip
def test_min_bar_reader(shared_datadir):
    df = TdxMinBarReader().get_df(str(shared_datadir / "sh600000.5"))

    assert df.empty
    assert df["2017-07-21"].sum()
