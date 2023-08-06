from tdxpy.reader import TdxLCMinBarReader


def test_lc_min_bar_reader_lc5(shared_datadir):
    df = TdxLCMinBarReader().get_df(str(shared_datadir / "vipdoc" / "sh" / "fzline" / "sh688001.lc5"))
    assert not df.empty

    print("")
    print(df)


def test_lc_min_bar_reader_lc1(shared_datadir):
    df = TdxLCMinBarReader().get_df(str(shared_datadir / "vipdoc" / "sh" / "minline" / "sh688001.lc1"))
    assert not df.empty

    print("")
    print(df)
