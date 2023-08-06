from tdxpy.reader import BlockReader
from tdxpy.reader import CustomerBlockReader
from tdxpy.reader.block_reader import BlockReader_TYPE_GROUP


def test_block_reader0(shared_datadir):
    df = BlockReader().get_df(str(shared_datadir / "block_zs.dat"))
    assert not df.empty

    df = BlockReader().get_df(str(shared_datadir / "block_fg.dat"))
    assert not df.empty

    df = BlockReader().get_df(str(shared_datadir / "block_gn.dat"))
    assert not df.empty


def test_block_reader1(shared_datadir):
    df2 = BlockReader().get_df(str(shared_datadir / "block_zs.dat"), BlockReader_TYPE_GROUP)
    print("")
    print(df2)
    assert not df2.empty


def test_block_reader2(shared_datadir):
    df3 = CustomerBlockReader().get_df(str(shared_datadir / "blocknew"))
    print("")
    print(df3)
    assert not df3.empty


def test_block_reader3(shared_datadir):
    df4 = CustomerBlockReader().get_df(str(shared_datadir / "blocknew"), BlockReader_TYPE_GROUP)
    print("")
    print(df4)
    assert not df4.empty
