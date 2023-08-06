from pprint import pprint

import pandas as pd
import pytest


def test_get_block_info(client):
    data = client.get_and_parse_block_info("block.dat")
    assert data
    pprint(pd.DataFrame(data))


def test_get_block_df(client):
    data = client.get_and_parse_block_info("block.dat")
    assert data
    pprint(pd.DataFrame(data))


def test_get_block_null(client):
    with pytest.raises(TypeError):
        client.get_and_parse_block_info()
